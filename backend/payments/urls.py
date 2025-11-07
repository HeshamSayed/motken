"""
URLs for Payments app.
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    PackageViewSet, SubscriptionViewSet, PaymentTransactionViewSet,
    CouponViewSet, TeacherPayoutViewSet
)

app_name = 'payments'

router = DefaultRouter()
router.register(r'packages', PackageViewSet, basename='package')
router.register(r'subscriptions', SubscriptionViewSet, basename='subscription')
router.register(r'transactions', PaymentTransactionViewSet, basename='transaction')
router.register(r'coupons', CouponViewSet, basename='coupon')
router.register(r'payouts', TeacherPayoutViewSet, basename='payout')

urlpatterns = [
    path('', include(router.urls)),
]
