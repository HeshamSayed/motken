abstract class SessionEvent {}

class LoadMySessionsEvent extends SessionEvent {
  final String? status;
  final String? ordering;
  LoadMySessionsEvent({this.status, this.ordering});
}

class LoadSessionDetailsEvent extends SessionEvent {
  final String sessionId;
  LoadSessionDetailsEvent(this.sessionId);
}

class BookSessionEvent extends SessionEvent {
  final String teacherId;
  final String scheduledDate;
  final String scheduledTime;
  final int duration;
  final String? curriculum;
  final String? lessonTopic;

  BookSessionEvent({
    required this.teacherId,
    required this.scheduledDate,
    required this.scheduledTime,
    required this.duration,
    this.curriculum,
    this.lessonTopic,
  });
}

class JoinSessionEvent extends SessionEvent {
  final String sessionId;
  JoinSessionEvent(this.sessionId);
}

class CancelSessionEvent extends SessionEvent {
  final String sessionId;
  final String cancellationReason;
  CancelSessionEvent(this.sessionId, this.cancellationReason);
}

class CompleteSessionEvent extends SessionEvent {
  final String sessionId;
  CompleteSessionEvent(this.sessionId);
}
