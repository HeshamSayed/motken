import 'package:json_annotation/json_annotation.dart';

part 'student_progress_model.g.dart';

@JsonSerializable()
class StudentProgressModel {
  final String id;
  @JsonKey(name: 'student')
  final String studentId;
  @JsonKey(name: 'curriculum')
  final String curriculumId;
  @JsonKey(name: 'curriculum_name')
  final String? curriculumName;
  @JsonKey(name: 'current_lesson')
  final String? currentLessonId;
  @JsonKey(name: 'lessons_completed')
  final int lessonsCompleted;
  @JsonKey(name: 'total_lessons')
  final int totalLessons;
  @JsonKey(name: 'completion_percentage')
  final double completionPercentage;
  @JsonKey(name: 'total_study_time_minutes')
  final int totalStudyTimeMinutes;
  @JsonKey(name: 'average_score')
  final double? averageScore;
  @JsonKey(name: 'last_activity')
  final String? lastActivity;
  @JsonKey(name: 'enrolled_at')
  final String enrolledAt;
  @JsonKey(name: 'completed_at')
  final String? completedAt;

  StudentProgressModel({
    required this.id,
    required this.studentId,
    required this.curriculumId,
    this.curriculumName,
    this.currentLessonId,
    required this.lessonsCompleted,
    required this.totalLessons,
    required this.completionPercentage,
    required this.totalStudyTimeMinutes,
    this.averageScore,
    this.lastActivity,
    required this.enrolledAt,
    this.completedAt,
  });

  factory StudentProgressModel.fromJson(Map<String, dynamic> json) =>
      _$StudentProgressModelFromJson(json);

  Map<String, dynamic> toJson() => _$StudentProgressModelToJson(this);

  bool get isCompleted => completedAt != null;

  String get studyTimeDisplay {
    final hours = totalStudyTimeMinutes ~/ 60;
    final minutes = totalStudyTimeMinutes % 60;
    if (hours > 0) {
      return '$hours h $minutes min';
    }
    return '$minutes min';
  }
}
