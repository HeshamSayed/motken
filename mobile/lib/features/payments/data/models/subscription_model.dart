import 'package:json_annotation/json_annotation.dart';

part 'subscription_model.g.dart';

@JsonSerializable()
class SubscriptionModel {
  final String id;
  @JsonKey(name: 'student')
  final String studentId;
  @JsonKey(name: 'package')
  final String packageId;
  @JsonKey(name: 'package_name')
  final String? packageName;
  @JsonKey(name: 'sessions_total')
  final int sessionsTotal;
  @JsonKey(name: 'sessions_used')
  final int sessionsUsed;
  @JsonKey(name: 'sessions_remaining')
  final int sessionsRemaining;
  final String status;
  @JsonKey(name: 'start_date')
  final String startDate;
  @JsonKey(name: 'end_date')
  final String endDate;
  @JsonKey(name: 'auto_renew')
  final bool autoRenew;
  @JsonKey(name: 'created_at')
  final String createdAt;

  SubscriptionModel({
    required this.id,
    required this.studentId,
    required this.packageId,
    this.packageName,
    required this.sessionsTotal,
    required this.sessionsUsed,
    required this.sessionsRemaining,
    required this.status,
    required this.startDate,
    required this.endDate,
    required this.autoRenew,
    required this.createdAt,
  });

  factory SubscriptionModel.fromJson(Map<String, dynamic> json) =>
      _$SubscriptionModelFromJson(json);

  Map<String, dynamic> toJson() => _$SubscriptionModelToJson(this);

  double get usagePercentage {
    if (sessionsTotal == 0) return 0.0;
    return (sessionsUsed / sessionsTotal) * 100;
  }

  bool get isActive => status == 'active';
  bool get isExpired => status == 'expired';
}
