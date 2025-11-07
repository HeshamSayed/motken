"""
Payment serializers for API.
"""

from rest_framework import serializers
from .models import Package, Subscription, PaymentTransaction, TeacherPayout, Coupon, CouponUsage
from users.serializers import UserSerializer


class PackageSerializer(serializers.ModelSerializer):
    """Serializer for Packages."""

    class Meta:
        model = Package
        fields = [
            'id', 'name', 'package_type', 'description', 'session_count',
            'session_duration', 'validity_days', 'price', 'currency',
            'discount_percent', 'final_price', 'price_per_session', 'features',
            'includes_recordings', 'includes_materials', 'priority_support',
            'is_active', 'is_featured', 'min_age', 'max_age', 'for_new_students_only'
        ]
        read_only_fields = ['final_price', 'price_per_session']


class SubscriptionSerializer(serializers.ModelSerializer):
    """Serializer for Subscriptions."""

    package = PackageSerializer(read_only=True)
    student = UserSerializer(read_only=True)
    is_valid = serializers.BooleanField(read_only=True)
    usage_percent = serializers.FloatField(read_only=True)

    class Meta:
        model = Subscription
        fields = [
            'id', 'student', 'package', 'total_sessions', 'sessions_used',
            'sessions_remaining', 'start_date', 'end_date', 'status',
            'amount_paid', 'currency', 'auto_renew', 'renewal_date',
            'created_at', 'is_valid', 'usage_percent'
        ]
        read_only_fields = ['sessions_used', 'sessions_remaining', 'created_at']


class PaymentTransactionSerializer(serializers.ModelSerializer):
    """Serializer for Payment Transactions."""

    user = UserSerializer(read_only=True)
    package = PackageSerializer(read_only=True)

    class Meta:
        model = PaymentTransaction
        fields = [
            'id', 'user', 'transaction_type', 'amount', 'currency', 'status',
            'payment_method', 'gateway_transaction_id', 'package', 'session',
            'platform_fee', 'gateway_fee', 'net_amount', 'invoice_number',
            'created_at', 'completed_at'
        ]
        read_only_fields = ['id', 'user', 'gateway_transaction_id', 'invoice_number', 'created_at']


class InitiatePaymentSerializer(serializers.Serializer):
    """Serializer for initiating payment."""

    package_id = serializers.UUIDField()
    payment_method = serializers.ChoiceField(choices=['paymob_card', 'paymob_wallet', 'paymob_kiosk'])
    coupon_code = serializers.CharField(required=False, allow_blank=True)


class CouponSerializer(serializers.ModelSerializer):
    """Serializer for Coupons."""

    is_valid = serializers.BooleanField(read_only=True)

    class Meta:
        model = Coupon
        fields = [
            'id', 'code', 'description', 'discount_type', 'discount_value',
            'max_discount_amount', 'currency', 'max_uses', 'times_used',
            'valid_from', 'valid_until', 'is_active', 'min_purchase_amount',
            'for_new_users_only', 'is_valid'
        ]
        read_only_fields = ['times_used']


class TeacherPayoutSerializer(serializers.ModelSerializer):
    """Serializer for Teacher Payouts."""

    from teachers.serializers import TeacherListSerializer
    teacher = TeacherListSerializer(read_only=True)

    class Meta:
        model = TeacherPayout
        fields = [
            'id', 'teacher', 'amount', 'currency', 'payout_method', 'status',
            'period_start', 'period_end', 'session_count', 'bank_account',
            'paypal_email', 'transaction_reference', 'created_at'
        ]
        read_only_fields = ['id', 'status', 'session_count', 'created_at']
