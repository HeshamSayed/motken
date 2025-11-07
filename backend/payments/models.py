"""
Payment models for Motken platform.
Handles packages, subscriptions, transactions, and teacher payouts.
"""

from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from users.models import User
from teachers.models import TeacherProfile
from sessions.models import Session
import uuid


class Package(models.Model):
    """Session packages/plans."""

    PACKAGE_TYPE_CHOICES = (
        ('trial', 'Trial Package'),
        ('basic', 'Basic Package'),
        ('standard', 'Standard Package'),
        ('premium', 'Premium Package'),
        ('custom', 'Custom Package'),
    )

    DURATION_CHOICES = (
        (30, '30 minutes'),
        (45, '45 minutes'),
        (60, '60 minutes'),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    package_type = models.CharField(max_length=20, choices=PACKAGE_TYPE_CHOICES)
    description = models.TextField()

    # Package Details
    session_count = models.IntegerField(validators=[MinValueValidator(1)])
    session_duration = models.IntegerField(choices=DURATION_CHOICES)
    validity_days = models.IntegerField(help_text="Package validity in days")

    # Pricing
    price = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, default='USD')
    discount_percent = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
    final_price = models.DecimalField(max_digits=10, decimal_places=2)

    # Price per session
    price_per_session = models.DecimalField(max_digits=8, decimal_places=2)

    # Features
    features = models.JSONField(default=list, help_text="List of package features")
    includes_recordings = models.BooleanField(default=False)
    includes_materials = models.BooleanField(default=False)
    priority_support = models.BooleanField(default=False)

    # Availability
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    display_order = models.IntegerField(default=0)

    # Restrictions
    min_age = models.IntegerField(null=True, blank=True)
    max_age = models.IntegerField(null=True, blank=True)
    for_new_students_only = models.BooleanField(default=False)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'packages'
        verbose_name = 'Package'
        verbose_name_plural = 'Packages'
        ordering = ['display_order', 'price']

    def __str__(self):
        return f"{self.name} - {self.session_count} sessions"

    def save(self, *args, **kwargs):
        """Calculate final price and price per session."""
        if self.discount_percent:
            self.final_price = self.price * (1 - self.discount_percent / 100)
        else:
            self.final_price = self.price

        if self.session_count:
            self.price_per_session = self.final_price / self.session_count

        super().save(*args, **kwargs)


class Subscription(models.Model):
    """Student subscriptions/purchased packages."""

    STATUS_CHOICES = (
        ('active', 'Active'),
        ('expired', 'Expired'),
        ('cancelled', 'Cancelled'),
        ('suspended', 'Suspended'),
        ('completed', 'Completed'),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='subscriptions')
    package = models.ForeignKey(Package, on_delete=models.PROTECT)

    # Subscription Details
    total_sessions = models.IntegerField()
    sessions_used = models.IntegerField(default=0)
    sessions_remaining = models.IntegerField()

    # Validity
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')

    # Pricing
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, default='USD')

    # Auto-renewal
    auto_renew = models.BooleanField(default=False)
    renewal_date = models.DateField(null=True, blank=True)

    # Cancellation
    cancelled_at = models.DateTimeField(null=True, blank=True)
    cancellation_reason = models.TextField(blank=True)

    # Payment reference
    payment_transaction = models.ForeignKey('PaymentTransaction', on_delete=models.SET_NULL, null=True, blank=True)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'subscriptions'
        verbose_name = 'Subscription'
        verbose_name_plural = 'Subscriptions'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['student', 'status']),
            models.Index(fields=['end_date']),
        ]

    def __str__(self):
        return f"{self.student.get_full_name()} - {self.package.name}"

    @property
    def is_valid(self):
        """Check if subscription is still valid."""
        return (self.status == 'active' and
                self.sessions_remaining > 0 and
                self.end_date >= timezone.now().date())

    @property
    def usage_percent(self):
        """Calculate usage percentage."""
        if self.total_sessions:
            return (self.sessions_used / self.total_sessions) * 100
        return 0

    def use_session(self):
        """Decrease sessions remaining."""
        if self.sessions_remaining > 0:
            self.sessions_used += 1
            self.sessions_remaining -= 1
            if self.sessions_remaining == 0:
                self.status = 'completed'
            self.save()


class PaymentTransaction(models.Model):
    """Payment transactions."""

    TRANSACTION_TYPE_CHOICES = (
        ('package_purchase', 'Package Purchase'),
        ('session_payment', 'Session Payment'),
        ('refund', 'Refund'),
        ('teacher_payout', 'Teacher Payout'),
    )

    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('refunded', 'Refunded'),
        ('cancelled', 'Cancelled'),
    )

    PAYMENT_METHOD_CHOICES = (
        ('paymob_card', 'Paymob Card'),
        ('paymob_wallet', 'Paymob Wallet'),
        ('paymob_kiosk', 'Paymob Kiosk'),
        ('stripe', 'Stripe'),
        ('paypal', 'PayPal'),
        ('bank_transfer', 'Bank Transfer'),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='transactions')

    # Transaction Details
    transaction_type = models.CharField(max_length=30, choices=TRANSACTION_TYPE_CHOICES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, default='USD')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    # Payment Gateway
    payment_method = models.CharField(max_length=30, choices=PAYMENT_METHOD_CHOICES)
    gateway_transaction_id = models.CharField(max_length=255, blank=True)
    gateway_response = models.JSONField(default=dict, blank=True)

    # Paymob specific fields
    paymob_order_id = models.CharField(max_length=100, blank=True)
    paymob_payment_id = models.CharField(max_length=100, blank=True)
    paymob_hmac = models.CharField(max_length=255, blank=True)

    # Related Objects
    package = models.ForeignKey(Package, on_delete=models.SET_NULL, null=True, blank=True)
    session = models.ForeignKey(Session, on_delete=models.SET_NULL, null=True, blank=True)

    # Fee Breakdown
    platform_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    gateway_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    net_amount = models.DecimalField(max_digits=10, decimal_places=2)

    # Refund
    refund_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    refund_reason = models.TextField(blank=True)
    refunded_at = models.DateTimeField(null=True, blank=True)

    # Receipt
    receipt_url = models.URLField(blank=True)
    invoice_number = models.CharField(max_length=50, unique=True, blank=True)

    # Metadata
    metadata = models.JSONField(default=dict, blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'payment_transactions'
        verbose_name = 'Payment Transaction'
        verbose_name_plural = 'Payment Transactions'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', '-created_at']),
            models.Index(fields=['status']),
            models.Index(fields=['gateway_transaction_id']),
            models.Index(fields=['invoice_number']),
        ]

    def __str__(self):
        return f"{self.transaction_type} - {self.amount} {self.currency} - {self.status}"

    def save(self, *args, **kwargs):
        """Generate invoice number if not exists."""
        if not self.invoice_number:
            self.invoice_number = f"INV-{timezone.now().strftime('%Y%m%d')}-{str(self.id)[:8]}"
        super().save(*args, **kwargs)


class TeacherPayout(models.Model):
    """Teacher payouts."""

    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('cancelled', 'Cancelled'),
    )

    PAYOUT_METHOD_CHOICES = (
        ('bank_transfer', 'Bank Transfer'),
        ('paypal', 'PayPal'),
        ('paymob', 'Paymob'),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    teacher = models.ForeignKey(TeacherProfile, on_delete=models.CASCADE, related_name='payouts')

    # Payout Details
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, default='USD')
    payout_method = models.CharField(max_length=30, choices=PAYOUT_METHOD_CHOICES)

    # Status
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    # Period
    period_start = models.DateField()
    period_end = models.DateField()

    # Related Sessions
    sessions = models.ManyToManyField(Session, related_name='payouts')
    session_count = models.IntegerField(default=0)

    # Payment Details
    bank_account = models.CharField(max_length=100, blank=True)
    paypal_email = models.EmailField(blank=True)
    transaction_reference = models.CharField(max_length=255, blank=True)

    # Processing
    processed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='processed_payouts')
    processed_at = models.DateTimeField(null=True, blank=True)
    notes = models.TextField(blank=True)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'teacher_payouts'
        verbose_name = 'Teacher Payout'
        verbose_name_plural = 'Teacher Payouts'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['teacher', 'status']),
            models.Index(fields=['period_start', 'period_end']),
        ]

    def __str__(self):
        return f"Payout to {self.teacher.user.get_full_name()} - {self.amount} {self.currency}"


class Coupon(models.Model):
    """Discount coupons."""

    DISCOUNT_TYPE_CHOICES = (
        ('percentage', 'Percentage'),
        ('fixed', 'Fixed Amount'),
    )

    code = models.CharField(max_length=50, unique=True, db_index=True)
    description = models.TextField(blank=True)

    # Discount
    discount_type = models.CharField(max_length=20, choices=DISCOUNT_TYPE_CHOICES)
    discount_value = models.DecimalField(max_digits=10, decimal_places=2)
    max_discount_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    # Currency
    currency = models.CharField(max_length=3, default='USD')

    # Usage Limits
    max_uses = models.IntegerField(null=True, blank=True, help_text="Null = unlimited")
    times_used = models.IntegerField(default=0)
    max_uses_per_user = models.IntegerField(default=1)

    # Validity
    valid_from = models.DateTimeField()
    valid_until = models.DateTimeField()
    is_active = models.BooleanField(default=True)

    # Restrictions
    min_purchase_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    applicable_packages = models.ManyToManyField(Package, blank=True)
    for_new_users_only = models.BooleanField(default=False)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'coupons'
        verbose_name = 'Coupon'
        verbose_name_plural = 'Coupons'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.code} - {self.discount_value}{'%' if self.discount_type == 'percentage' else self.currency}"

    @property
    def is_valid(self):
        """Check if coupon is currently valid."""
        now = timezone.now()
        return (self.is_active and
                self.valid_from <= now <= self.valid_until and
                (self.max_uses is None or self.times_used < self.max_uses))

    def calculate_discount(self, amount):
        """Calculate discount amount for given purchase amount."""
        if not self.is_valid:
            return 0

        if self.min_purchase_amount and amount < self.min_purchase_amount:
            return 0

        if self.discount_type == 'percentage':
            discount = amount * (self.discount_value / 100)
            if self.max_discount_amount:
                discount = min(discount, self.max_discount_amount)
        else:
            discount = self.discount_value

        return min(discount, amount)


class CouponUsage(models.Model):
    """Track coupon usage."""

    coupon = models.ForeignKey(Coupon, on_delete=models.CASCADE, related_name='usage_records')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='coupon_usages')
    transaction = models.ForeignKey(PaymentTransaction, on_delete=models.CASCADE)

    discount_amount = models.DecimalField(max_digits=10, decimal_places=2)
    original_amount = models.DecimalField(max_digits=10, decimal_places=2)
    final_amount = models.DecimalField(max_digits=10, decimal_places=2)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'coupon_usage'
        verbose_name = 'Coupon Usage'
        verbose_name_plural = 'Coupon Usages'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.coupon.code} used by {self.user.get_full_name()}"
