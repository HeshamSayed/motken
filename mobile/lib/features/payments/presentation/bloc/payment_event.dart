abstract class PaymentEvent {}

class LoadPackagesEvent extends PaymentEvent {}

class SelectPackageEvent extends PaymentEvent {
  final String packageId;
  SelectPackageEvent(this.packageId);
}

class ValidateCouponEvent extends PaymentEvent {
  final String couponCode;
  ValidateCouponEvent(this.couponCode);
}

class InitiatePaymentEvent extends PaymentEvent {
  final String packageId;
  final String? couponCode;
  InitiatePaymentEvent(this.packageId, {this.couponCode});
}

class LoadSubscriptionEvent extends PaymentEvent {}

class LoadTransactionsEvent extends PaymentEvent {}

class ClearCouponEvent extends PaymentEvent {}
