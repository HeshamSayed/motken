import 'package:json_annotation/json_annotation.dart';

part 'transaction_model.g.dart';

@JsonSerializable()
class TransactionModel {
  final String id;
  @JsonKey(name: 'student')
  final String studentId;
  @JsonKey(name: 'package')
  final String? packageId;
  @JsonKey(name: 'session')
  final String? sessionId;
  @JsonKey(name: 'transaction_type')
  final String transactionType;
  final String amount;
  @JsonKey(name: 'currency')
  final String currency;
  final String status;
  @JsonKey(name: 'payment_method')
  final String? paymentMethod;
  @JsonKey(name: 'paymob_order_id')
  final String? paymobOrderId;
  @JsonKey(name: 'paymob_transaction_id')
  final String? paymobTransactionId;
  @JsonKey(name: 'coupon_code')
  final String? couponCode;
  @JsonKey(name: 'discount_amount')
  final String? discountAmount;
  @JsonKey(name: 'created_at')
  final String createdAt;
  @JsonKey(name: 'completed_at')
  final String? completedAt;

  TransactionModel({
    required this.id,
    required this.studentId,
    this.packageId,
    this.sessionId,
    required this.transactionType,
    required this.amount,
    required this.currency,
    required this.status,
    this.paymentMethod,
    this.paymobOrderId,
    this.paymobTransactionId,
    this.couponCode,
    this.discountAmount,
    required this.createdAt,
    this.completedAt,
  });

  factory TransactionModel.fromJson(Map<String, dynamic> json) =>
      _$TransactionModelFromJson(json);

  Map<String, dynamic> toJson() => _$TransactionModelToJson(this);

  double get amountValue => double.tryParse(amount) ?? 0.0;
  double get discountValue => double.tryParse(discountAmount ?? '0') ?? 0.0;

  bool get isPending => status == 'pending';
  bool get isCompleted => status == 'completed';
  bool get isFailed => status == 'failed';
}
