import 'package:json_annotation/json_annotation.dart';

part 'teacher_model.g.dart';

@JsonSerializable()
class TeacherModel {
  final String id;
  final UserInfo user;
  final List<String> specializations;
  @JsonKey(name: 'years_of_experience')
  final int yearsOfExperience;
  @JsonKey(name: 'average_rating')
  final double averageRating;
  @JsonKey(name: 'total_ratings')
  final int totalRatings;
  @JsonKey(name: 'session_30min_rate')
  final double session30minRate;
  @JsonKey(name: 'session_45min_rate')
  final double session45minRate;
  @JsonKey(name: 'session_60min_rate')
  final double session60minRate;
  @JsonKey(name: 'is_available')
  final bool isAvailable;
  @JsonKey(name: 'is_featured')
  final bool isFeatured;
  final String bio;

  TeacherModel({
    required this.id,
    required this.user,
    required this.specializations,
    required this.yearsOfExperience,
    required this.averageRating,
    required this.totalRatings,
    required this.session30minRate,
    required this.session45minRate,
    required this.session60minRate,
    required this.isAvailable,
    required this.isFeatured,
    required this.bio,
  });

  factory TeacherModel.fromJson(Map<String, dynamic> json) =>
      _$TeacherModelFromJson(json);

  Map<String, dynamic> toJson() => _$TeacherModelToJson(this);

  String get fullName => '${user.firstName} ${user.lastName}';

  String get priceRange =>
      '\$${session30minRate.toStringAsFixed(0)} - \$${session60minRate.toStringAsFixed(0)}';
}

@JsonSerializable()
class UserInfo {
  @JsonKey(name: 'first_name')
  final String firstName;
  @JsonKey(name: 'last_name')
  final String lastName;
  @JsonKey(name: 'profile_picture')
  final String? profilePicture;

  UserInfo({
    required this.firstName,
    required this.lastName,
    this.profilePicture,
  });

  factory UserInfo.fromJson(Map<String, dynamic> json) =>
      _$UserInfoFromJson(json);

  Map<String, dynamic> toJson() => _$UserInfoToJson(this);
}

@JsonSerializable()
class TeacherAvailability {
  @JsonKey(name: 'day_of_week')
  final int dayOfWeek;
  @JsonKey(name: 'start_time')
  final String startTime;
  @JsonKey(name: 'end_time')
  final String endTime;

  TeacherAvailability({
    required this.dayOfWeek,
    required this.startTime,
    required this.endTime,
  });

  factory TeacherAvailability.fromJson(Map<String, dynamic> json) =>
      _$TeacherAvailabilityFromJson(json);

  Map<String, dynamic> toJson() => _$TeacherAvailabilityToJson(this);

  String get dayName {
    const days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'];
    return days[dayOfWeek];
  }
}
