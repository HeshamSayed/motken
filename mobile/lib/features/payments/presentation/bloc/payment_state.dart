import '../../data/models/package_model.dart';
import '../../data/models/subscription_model.dart';
import '../../data/models/transaction_model.dart';

abstract class PaymentState {}

class PaymentInitial extends PaymentState {}

class PaymentLoading extends PaymentState {}

class PackagesLoaded extends PaymentState {
  final List<PackageModel> packages;
  final PackageModel? selectedPackage;
  final Map<String, dynamic>? couponData;

  PackagesLoaded(
    this.packages, {
    this.selectedPackage,
    this.couponData,
  });

  PackagesLoaded copyWith({
    List<PackageModel>? packages,
    PackageModel? selectedPackage,
    Map<String, dynamic>? couponData,
    bool clearCoupon = false,
  }) {
    return PackagesLoaded(
      packages ?? this.packages,
      selectedPackage: selectedPackage ?? this.selectedPackage,
      couponData: clearCoupon ? null : (couponData ?? this.couponData),
    );
  }
}

class CouponValidating extends PaymentState {}

class CouponValid extends PaymentState {
  final Map<String, dynamic> couponData;
  CouponValid(this.couponData);
}

class CouponInvalid extends PaymentState {
  final String message;
  CouponInvalid(this.message);
}

class PaymentInitiated extends PaymentState {
  final String paymentUrl;
  final String transactionId;
  PaymentInitiated(this.paymentUrl, this.transactionId);
}

class SubscriptionLoaded extends PaymentState {
  final SubscriptionModel subscription;
  SubscriptionLoaded(this.subscription);
}

class TransactionsLoaded extends PaymentState {
  final List<TransactionModel> transactions;
  TransactionsLoaded(this.transactions);
}

class PaymentError extends PaymentState {
  final String message;
  PaymentError(this.message);
}
