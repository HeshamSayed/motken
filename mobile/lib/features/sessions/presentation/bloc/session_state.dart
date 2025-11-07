import '../../data/models/session_model.dart';

abstract class SessionState {}

class SessionInitial extends SessionState {}

class SessionLoading extends SessionState {}

class SessionsLoaded extends SessionState {
  final List<SessionModel> sessions;
  SessionsLoaded(this.sessions);
}

class SessionDetailsLoaded extends SessionState {
  final SessionModel session;
  SessionDetailsLoaded(this.session);
}

class SessionBooked extends SessionState {
  final SessionModel session;
  SessionBooked(this.session);
}

class SessionJoinReady extends SessionState {
  final String joinUrl;
  final String sessionId;
  SessionJoinReady(this.joinUrl, this.sessionId);
}

class SessionCancelled extends SessionState {
  final SessionModel session;
  SessionCancelled(this.session);
}

class SessionCompleted extends SessionState {
  final SessionModel session;
  SessionCompleted(this.session);
}

class SessionError extends SessionState {
  final String message;
  SessionError(this.message);
}
