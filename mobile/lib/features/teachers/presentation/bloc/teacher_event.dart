abstract class TeacherEvent {}

class LoadTeachersEvent extends TeacherEvent {
  final String? specialization;
  final String? country;
  final double? minRating;
  final String? search;

  LoadTeachersEvent({
    this.specialization,
    this.country,
    this.minRating,
    this.search,
  });
}

class LoadTeacherDetailsEvent extends TeacherEvent {
  final String teacherId;
  LoadTeacherDetailsEvent(this.teacherId);
}

class LoadTeacherReviewsEvent extends TeacherEvent {
  final String teacherId;
  LoadTeacherReviewsEvent(this.teacherId);
}

class SubmitReviewEvent extends TeacherEvent {
  final String teacherId;
  final int overallRating;
  final int teachingQuality;
  final int communication;
  final int punctuality;
  final int patience;
  final String reviewText;

  SubmitReviewEvent({
    required this.teacherId,
    required this.overallRating,
    required this.teachingQuality,
    required this.communication,
    required this.punctuality,
    required this.patience,
    required this.reviewText,
  });
}
