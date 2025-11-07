"""
Admin configuration for Payments app.
"""

from django.contrib import admin
from django.utils.html import format_html
from .models import (
    Package, Subscription, PaymentTransaction, TeacherPayout,
    Coupon, CouponUsage
)


@admin.register(Package)
class PackageAdmin(admin.ModelAdmin):
    """Admin interface for Packages."""

    list_display = ['name', 'package_type', 'session_count', 'session_duration', 'final_price', 'is_active', 'is_featured']
    list_filter = ['package_type', 'is_active', 'is_featured', 'session_duration']
    search_fields = ['name', 'description']
    readonly_fields = ['id', 'created_at', 'updated_at']

    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'package_type', 'description')
        }),
        ('Package Details', {
            'fields': ('session_count', 'session_duration', 'validity_days')
        }),
        ('Pricing', {
            'fields': ('price', 'currency', 'discount_percent', 'final_price', 'price_per_session')
        }),
        ('Features', {
            'fields': ('features', 'includes_recordings', 'includes_materials', 'priority_support')
        }),
        ('Availability', {
            'fields': ('is_active', 'is_featured', 'display_order')
        }),
        ('Restrictions', {
            'fields': ('min_age', 'max_age', 'for_new_students_only')
        }),
    )

    actions = ['activate_packages', 'deactivate_packages', 'feature_packages']

    def activate_packages(self, request, queryset):
        updated = queryset.update(is_active=True)
        self.message_user(request, f'{updated} package(s) activated.')
    activate_packages.short_description = 'Activate selected packages'

    def deactivate_packages(self, request, queryset):
        updated = queryset.update(is_active=False)
        self.message_user(request, f'{updated} package(s) deactivated.')
    deactivate_packages.short_description = 'Deactivate selected packages'

    def feature_packages(self, request, queryset):
        updated = queryset.update(is_featured=True)
        self.message_user(request, f'{updated} package(s) featured.')
    feature_packages.short_description = 'Feature selected packages'


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    """Admin interface for Subscriptions."""

    list_display = ['student', 'package', 'status', 'sessions_used', 'sessions_remaining', 'end_date']
    list_filter = ['status', 'auto_renew', 'created_at']
    search_fields = ['student__email', 'package__name']
    readonly_fields = ['id', 'created_at', 'updated_at']
    date_hierarchy = 'created_at'

    fieldsets = (
        ('Subscription Information', {
            'fields': ('student', 'package', 'payment_transaction')
        }),
        ('Session Details', {
            'fields': ('total_sessions', 'sessions_used', 'sessions_remaining')
        }),
        ('Validity', {
            'fields': ('start_date', 'end_date', 'status')
        }),
        ('Pricing', {
            'fields': ('amount_paid', 'currency')
        }),
        ('Auto-Renewal', {
            'fields': ('auto_renew', 'renewal_date')
        }),
        ('Cancellation', {
            'fields': ('cancelled_at', 'cancellation_reason')
        }),
    )

    actions = ['activate_subscriptions', 'cancel_subscriptions']

    def activate_subscriptions(self, request, queryset):
        updated = queryset.update(status='active')
        self.message_user(request, f'{updated} subscription(s) activated.')
    activate_subscriptions.short_description = 'Activate selected subscriptions'

    def cancel_subscriptions(self, request, queryset):
        from django.utils import timezone
        updated = queryset.update(status='cancelled', cancelled_at=timezone.now())
        self.message_user(request, f'{updated} subscription(s) cancelled.')
    cancel_subscriptions.short_description = 'Cancel selected subscriptions'


@admin.register(PaymentTransaction)
class PaymentTransactionAdmin(admin.ModelAdmin):
    """Admin interface for Payment Transactions."""

    list_display = ['invoice_number', 'user', 'transaction_type', 'amount', 'status', 'payment_method', 'created_at']
    list_filter = ['status', 'transaction_type', 'payment_method', 'created_at']
    search_fields = ['invoice_number', 'user__email', 'gateway_transaction_id']
    readonly_fields = ['id', 'created_at', 'updated_at', 'completed_at']
    date_hierarchy = 'created_at'

    fieldsets = (
        ('Transaction Information', {
            'fields': ('user', 'transaction_type', 'amount', 'currency', 'status')
        }),
        ('Payment Gateway', {
            'fields': ('payment_method', 'gateway_transaction_id', 'gateway_response')
        }),
        ('Paymob Details', {
            'fields': ('paymob_order_id', 'paymob_payment_id', 'paymob_hmac')
        }),
        ('Related Objects', {
            'fields': ('package', 'session')
        }),
        ('Fee Breakdown', {
            'fields': ('platform_fee', 'gateway_fee', 'net_amount')
        }),
        ('Refund', {
            'fields': ('refund_amount', 'refund_reason', 'refunded_at')
        }),
        ('Receipt', {
            'fields': ('receipt_url', 'invoice_number')
        }),
        ('Metadata', {
            'fields': ('metadata', 'ip_address')
        }),
    )

    actions = ['mark_completed', 'process_refunds']

    def mark_completed(self, request, queryset):
        from django.utils import timezone
        updated = queryset.update(status='completed', completed_at=timezone.now())
        self.message_user(request, f'{updated} transaction(s) marked as completed.')
    mark_completed.short_description = 'Mark selected transactions as completed'

    def process_refunds(self, request, queryset):
        from django.utils import timezone
        updated = queryset.update(status='refunded', refunded_at=timezone.now())
        self.message_user(request, f'{updated} transaction(s) refunded.')
    process_refunds.short_description = 'Process refunds for selected transactions'


@admin.register(TeacherPayout)
class TeacherPayoutAdmin(admin.ModelAdmin):
    """Admin interface for Teacher Payouts."""

    list_display = ['teacher', 'amount', 'status', 'payout_method', 'period_start', 'period_end']
    list_filter = ['status', 'payout_method', 'created_at']
    search_fields = ['teacher__user__email', 'transaction_reference']
    readonly_fields = ['id', 'created_at', 'updated_at']

    fieldsets = (
        ('Payout Information', {
            'fields': ('teacher', 'amount', 'currency', 'payout_method', 'status')
        }),
        ('Period', {
            'fields': ('period_start', 'period_end', 'session_count')
        }),
        ('Payment Details', {
            'fields': ('bank_account', 'paypal_email', 'transaction_reference')
        }),
        ('Processing', {
            'fields': ('processed_by', 'processed_at', 'notes')
        }),
    )

    actions = ['mark_as_processing', 'mark_as_completed']

    def mark_as_processing(self, request, queryset):
        updated = queryset.update(status='processing')
        self.message_user(request, f'{updated} payout(s) marked as processing.')
    mark_as_processing.short_description = 'Mark selected payouts as processing'

    def mark_as_completed(self, request, queryset):
        from django.utils import timezone
        updated = queryset.update(status='completed', processed_by=request.user, processed_at=timezone.now())
        self.message_user(request, f'{updated} payout(s) completed.')
    mark_as_completed.short_description = 'Mark selected payouts as completed'


@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    """Admin interface for Coupons."""

    list_display = ['code', 'discount_type', 'discount_value', 'times_used', 'max_uses', 'is_active', 'valid_until']
    list_filter = ['discount_type', 'is_active', 'created_at']
    search_fields = ['code', 'description']
    readonly_fields = ['times_used', 'created_at', 'updated_at']

    fieldsets = (
        ('Coupon Information', {
            'fields': ('code', 'description')
        }),
        ('Discount', {
            'fields': ('discount_type', 'discount_value', 'max_discount_amount', 'currency')
        }),
        ('Usage Limits', {
            'fields': ('max_uses', 'times_used', 'max_uses_per_user')
        }),
        ('Validity', {
            'fields': ('valid_from', 'valid_until', 'is_active')
        }),
        ('Restrictions', {
            'fields': ('min_purchase_amount', 'applicable_packages', 'for_new_users_only')
        }),
    )

    actions = ['activate_coupons', 'deactivate_coupons']

    def activate_coupons(self, request, queryset):
        updated = queryset.update(is_active=True)
        self.message_user(request, f'{updated} coupon(s) activated.')
    activate_coupons.short_description = 'Activate selected coupons'

    def deactivate_coupons(self, request, queryset):
        updated = queryset.update(is_active=False)
        self.message_user(request, f'{updated} coupon(s) deactivated.')
    deactivate_coupons.short_description = 'Deactivate selected coupons'


@admin.register(CouponUsage)
class CouponUsageAdmin(admin.ModelAdmin):
    """Admin interface for Coupon Usage."""

    list_display = ['coupon', 'user', 'discount_amount', 'original_amount', 'final_amount', 'created_at']
    list_filter = ['created_at']
    search_fields = ['coupon__code', 'user__email']
    readonly_fields = ['created_at']
