"""
Payment views and API endpoints.
"""

from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.utils import timezone

from .models import Package, Subscription, PaymentTransaction, Coupon, TeacherPayout
from .serializers import (
    PackageSerializer, SubscriptionSerializer, PaymentTransactionSerializer,
    InitiatePaymentSerializer, CouponSerializer, TeacherPayoutSerializer
)


class PackageViewSet(viewsets.ReadOnlyModelViewSet):
    """Package ViewSet - Read only for users."""

    queryset = Package.objects.filter(is_active=True)
    serializer_class = PackageSerializer
    permission_classes = [permissions.AllowAnyPermission]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['package_type', 'session_duration']

    def get_queryset(self):
        queryset = super().get_queryset()

        # Filter by user age if provided
        user_age = self.request.query_params.get('user_age')
        if user_age:
            user_age = int(user_age)
            queryset = queryset.filter(
                min_age__lte=user_age,
                max_age__gte=user_age
            ) | queryset.filter(min_age__isnull=True, max_age__isnull=True)

        return queryset.order_by('display_order', 'price')


class SubscriptionViewSet(viewsets.ModelViewSet):
    """Subscription ViewSet."""

    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_staff:
            return Subscription.objects.all()
        return Subscription.objects.filter(student=self.request.user)

    @action(detail=False, methods=['get'])
    def my_subscription(self, request):
        """Get current active subscription."""
        subscription = Subscription.objects.filter(
            student=request.user,
            status='active'
        ).first()

        if not subscription:
            return Response({
                'message': 'No active subscription found'
            }, status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(subscription)
        return Response(serializer.data)


class PaymentTransactionViewSet(viewsets.ModelViewSet):
    """Payment Transaction ViewSet."""

    queryset = PaymentTransaction.objects.all()
    serializer_class = PaymentTransactionSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['status', 'transaction_type']

    def get_queryset(self):
        if self.request.user.is_staff:
            return PaymentTransaction.objects.all()
        return PaymentTransaction.objects.filter(user=self.request.user)

    @action(detail=False, methods=['post'])
    def initiate(self, request):
        """Initiate payment process."""
        serializer = InitiatePaymentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        package = Package.objects.get(id=serializer.validated_data['package_id'])

        # Apply coupon if provided
        discount_amount = 0
        coupon = None
        final_amount = float(package.final_price)

        coupon_code = serializer.validated_data.get('coupon_code')
        if coupon_code:
            try:
                coupon = Coupon.objects.get(code=coupon_code)
                if coupon.is_valid:
                    discount_amount = coupon.calculate_discount(final_amount)
                    final_amount -= discount_amount
            except Coupon.DoesNotExist:
                pass

        # Calculate fees (2.9% gateway fee)
        gateway_fee = final_amount * 0.029
        platform_fee = final_amount * 0.10
        net_amount = final_amount - gateway_fee

        # Create transaction
        transaction = PaymentTransaction.objects.create(
            user=request.user,
            transaction_type='package_purchase',
            amount=final_amount,
            currency=package.currency,
            status='pending',
            payment_method=serializer.validated_data['payment_method'],
            package=package,
            platform_fee=platform_fee,
            gateway_fee=gateway_fee,
            net_amount=net_amount
        )

        # TODO: Integrate with Paymob to get payment URL
        payment_url = f"https://paymob.com/payment/{transaction.id}"

        return Response({
            'transaction_id': str(transaction.id),
            'amount': final_amount,
            'discount_amount': discount_amount,
            'payment_url': payment_url,
            'status': 'pending'
        }, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['post'])
    def webhook(self, request):
        """Webhook for payment gateway callbacks."""
        # TODO: Verify webhook signature
        # TODO: Process payment confirmation

        transaction_id = request.data.get('transaction_id')
        status_update = request.data.get('status')

        try:
            transaction = PaymentTransaction.objects.get(id=transaction_id)
            transaction.status = status_update
            transaction.gateway_response = request.data
            transaction.completed_at = timezone.now()
            transaction.save()

            # If successful, create subscription
            if status_update == 'completed':
                Subscription.objects.create(
                    student=transaction.user,
                    package=transaction.package,
                    total_sessions=transaction.package.session_count,
                    sessions_remaining=transaction.package.session_count,
                    start_date=timezone.now().date(),
                    end_date=timezone.now().date() + timezone.timedelta(days=transaction.package.validity_days),
                    amount_paid=transaction.amount,
                    currency=transaction.currency,
                    payment_transaction=transaction,
                    status='active'
                )

            return Response({'status': 'success'})
        except PaymentTransaction.DoesNotExist:
            return Response({'error': 'Transaction not found'}, status=status.HTTP_404_NOT_FOUND)


class CouponViewSet(viewsets.ReadOnlyModelViewSet):
    """Coupon ViewSet."""

    queryset = Coupon.objects.filter(is_active=True)
    serializer_class = CouponSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=False, methods=['post'])
    def validate(self, request):
        """Validate a coupon code."""
        code = request.data.get('code')
        package_id = request.data.get('package_id')

        try:
            coupon = Coupon.objects.get(code=code)
            package = Package.objects.get(id=package_id)

            if not coupon.is_valid:
                return Response({
                    'valid': False,
                    'error': 'Coupon is not valid'
                }, status=status.HTTP_400_BAD_REQUEST)

            discount_amount = coupon.calculate_discount(float(package.final_price))
            final_amount = float(package.final_price) - discount_amount

            return Response({
                'valid': True,
                'discount_amount': discount_amount,
                'final_amount': final_amount,
                'coupon': CouponSerializer(coupon).data
            })
        except (Coupon.DoesNotExist, Package.DoesNotExist):
            return Response({
                'valid': False,
                'error': 'Invalid coupon or package'
            }, status=status.HTTP_400_BAD_REQUEST)


class TeacherPayoutViewSet(viewsets.ModelViewSet):
    """Teacher Payout ViewSet."""

    queryset = TeacherPayout.objects.all()
    serializer_class = TeacherPayoutSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_staff:
            return TeacherPayout.objects.all()
        elif self.request.user.user_type == 'teacher':
            return TeacherPayout.objects.filter(teacher__user=self.request.user)
        return TeacherPayout.objects.none()

    @action(detail=False, methods=['get'])
    def my_earnings(self, request):
        """Get teacher's earnings summary."""
        if request.user.user_type != 'teacher':
            return Response({
                'error': 'Only teachers can view earnings'
            }, status=status.HTTP_403_FORBIDDEN)

        from teachers.models import TeacherProfile
        teacher = TeacherProfile.objects.get(user=request.user)

        return Response({
            'total_earnings': float(teacher.total_earnings),
            'pending_earnings': float(teacher.pending_earnings),
            'paid_earnings': float(teacher.paid_earnings),
            'recent_payouts': TeacherPayoutSerializer(
                teacher.payouts.order_by('-created_at')[:5],
                many=True
            ).data
        })
