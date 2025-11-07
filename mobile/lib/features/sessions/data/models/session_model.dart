import 'package:json_annotation/json_annotation.dart';

part 'session_model.g.dart';

@JsonSerializable()
class SessionModel {
  final String id;
  @JsonKey(name: 'student')
  final String studentId;
  @JsonKey(name: 'teacher')
  final String teacherId;
  @JsonKey(name: 'teacher_name')
  final String? teacherName;
  @JsonKey(name: 'student_name')
  final String? studentName;
  @JsonKey(name: 'scheduled_date')
  final String scheduledDate;
  @JsonKey(name: 'scheduled_time')
  final String scheduledTime;
  final int duration;
  final String? curriculum;
  @JsonKey(name: 'lesson_topic')
  final String? lessonTopic;
  final String status;
  @JsonKey(name: 'zoom_meeting_id')
  final String? zoomMeetingId;
  @JsonKey(name: 'zoom_join_url')
  final String? zoomJoinUrl;
  @JsonKey(name: 'zoom_start_url')
  final String? zoomStartUrl;
  @JsonKey(name: 'session_price')
  final String? sessionPrice;
  @JsonKey(name: 'teacher_payout')
  final String? teacherPayout;
  @JsonKey(name: 'cancellation_reason')
  final String? cancellationReason;
  @JsonKey(name: 'cancelled_at')
  final String? cancelledAt;
  @JsonKey(name: 'completed_at')
  final String? completedAt;
  @JsonKey(name: 'recording_url')
  final String? recordingUrl;
  @JsonKey(name: 'created_at')
  final String createdAt;

  SessionModel({
    required this.id,
    required this.studentId,
    required this.teacherId,
    this.teacherName,
    this.studentName,
    required this.scheduledDate,
    required this.scheduledTime,
    required this.duration,
    this.curriculum,
    this.lessonTopic,
    required this.status,
    this.zoomMeetingId,
    this.zoomJoinUrl,
    this.zoomStartUrl,
    this.sessionPrice,
    this.teacherPayout,
    this.cancellationReason,
    this.cancelledAt,
    this.completedAt,
    this.recordingUrl,
    required this.createdAt,
  });

  factory SessionModel.fromJson(Map<String, dynamic> json) =>
      _$SessionModelFromJson(json);

  Map<String, dynamic> toJson() => _$SessionModelToJson(this);

  bool get isScheduled => status == 'scheduled';
  bool get isCompleted => status == 'completed';
  bool get isCancelled =>
      status.contains('cancelled') || status == 'no_show_student';

  String get statusDisplay {
    switch (status) {
      case 'scheduled':
        return 'Scheduled';
      case 'in_progress':
        return 'In Progress';
      case 'completed':
        return 'Completed';
      case 'cancelled_by_student':
        return 'Cancelled by Student';
      case 'cancelled_by_teacher':
        return 'Cancelled by Teacher';
      case 'no_show_student':
        return 'No Show';
      case 'no_show_teacher':
        return 'Teacher No Show';
      default:
        return status;
    }
  }

  DateTime get scheduledDateTime {
    return DateTime.parse('$scheduledDate $scheduledTime');
  }

  bool get canJoin {
    if (!isScheduled) return false;
    final now = DateTime.now();
    final sessionTime = scheduledDateTime;
    // Can join 10 minutes before session
    return now.isAfter(sessionTime.subtract(const Duration(minutes: 10)));
  }

  bool get canCancel {
    if (!isScheduled) return false;
    final now = DateTime.now();
    final sessionTime = scheduledDateTime;
    // Can cancel up to 24 hours before
    return now.isBefore(sessionTime.subtract(const Duration(hours: 24)));
  }
}
