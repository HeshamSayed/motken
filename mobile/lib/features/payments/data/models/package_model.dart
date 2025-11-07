import 'package:json_annotation/json_annotation.dart';

part 'package_model.g.dart';

@JsonSerializable()
class PackageModel {
  final String id;
  final String name;
  @JsonKey(name: 'package_type')
  final String packageType;
  final String description;
  @JsonKey(name: 'session_count')
  final int sessionCount;
  @JsonKey(name: 'session_duration')
  final int sessionDuration;
  @JsonKey(name: 'validity_days')
  final int validityDays;
  final String price;
  @JsonKey(name: 'discount_percent')
  final int discountPercent;
  final List<String> features;
  @JsonKey(name: 'is_featured')
  final bool isFeatured;
  @JsonKey(name: 'priority_support')
  final bool prioritySupport;
  @JsonKey(name: 'display_order')
  final int displayOrder;
  @JsonKey(name: 'is_active')
  final bool isActive;

  PackageModel({
    required this.id,
    required this.name,
    required this.packageType,
    required this.description,
    required this.sessionCount,
    required this.sessionDuration,
    required this.validityDays,
    required this.price,
    required this.discountPercent,
    required this.features,
    required this.isFeatured,
    required this.prioritySupport,
    required this.displayOrder,
    required this.isActive,
  });

  factory PackageModel.fromJson(Map<String, dynamic> json) =>
      _$PackageModelFromJson(json);

  Map<String, dynamic> toJson() => _$PackageModelToJson(this);

  double get priceValue => double.tryParse(price) ?? 0.0;

  double get discountedPrice {
    if (discountPercent > 0) {
      return priceValue * (1 - discountPercent / 100);
    }
    return priceValue;
  }

  String get pricePerSession {
    final perSession = discountedPrice / sessionCount;
    return perSession.toStringAsFixed(2);
  }
}
