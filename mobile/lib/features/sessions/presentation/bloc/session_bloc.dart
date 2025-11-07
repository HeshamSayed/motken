import 'package:flutter_bloc/flutter_bloc.dart';
import '../../data/datasources/session_remote_data_source.dart';
import 'session_event.dart';
import 'session_state.dart';

class SessionBloc extends Bloc<SessionEvent, SessionState> {
  final SessionRemoteDataSource remoteDataSource;

  SessionBloc({required this.remoteDataSource}) : super(SessionInitial()) {
    on<LoadMySessionsEvent>(_onLoadMySessions);
    on<LoadSessionDetailsEvent>(_onLoadSessionDetails);
    on<BookSessionEvent>(_onBookSession);
    on<JoinSessionEvent>(_onJoinSession);
    on<CancelSessionEvent>(_onCancelSession);
    on<CompleteSessionEvent>(_onCompleteSession);
  }

  Future<void> _onLoadMySessions(
    LoadMySessionsEvent event,
    Emitter<SessionState> emit,
  ) async {
    emit(SessionLoading());
    try {
      final sessions = await remoteDataSource.getMySessions(
        status: event.status,
        ordering: event.ordering,
      );
      emit(SessionsLoaded(sessions));
    } catch (e) {
      emit(SessionError(e.toString()));
    }
  }

  Future<void> _onLoadSessionDetails(
    LoadSessionDetailsEvent event,
    Emitter<SessionState> emit,
  ) async {
    emit(SessionLoading());
    try {
      final session = await remoteDataSource.getSessionDetails(event.sessionId);
      emit(SessionDetailsLoaded(session));
    } catch (e) {
      emit(SessionError(e.toString()));
    }
  }

  Future<void> _onBookSession(
    BookSessionEvent event,
    Emitter<SessionState> emit,
  ) async {
    emit(SessionLoading());
    try {
      final session = await remoteDataSource.bookSession(
        teacherId: event.teacherId,
        scheduledDate: event.scheduledDate,
        scheduledTime: event.scheduledTime,
        duration: event.duration,
        curriculum: event.curriculum,
        lessonTopic: event.lessonTopic,
      );
      emit(SessionBooked(session));
    } catch (e) {
      emit(SessionError(e.toString()));
    }
  }

  Future<void> _onJoinSession(
    JoinSessionEvent event,
    Emitter<SessionState> emit,
  ) async {
    emit(SessionLoading());
    try {
      final result = await remoteDataSource.getJoinUrl(event.sessionId);
      final joinUrl = result['join_url'] as String;
      emit(SessionJoinReady(joinUrl, event.sessionId));
    } catch (e) {
      emit(SessionError(e.toString()));
    }
  }

  Future<void> _onCancelSession(
    CancelSessionEvent event,
    Emitter<SessionState> emit,
  ) async {
    emit(SessionLoading());
    try {
      final session = await remoteDataSource.cancelSession(
        event.sessionId,
        event.cancellationReason,
      );
      emit(SessionCancelled(session));
    } catch (e) {
      emit(SessionError(e.toString()));
    }
  }

  Future<void> _onCompleteSession(
    CompleteSessionEvent event,
    Emitter<SessionState> emit,
  ) async {
    emit(SessionLoading());
    try {
      final session = await remoteDataSource.completeSession(event.sessionId);
      emit(SessionCompleted(session));
    } catch (e) {
      emit(SessionError(e.toString()));
    }
  }
}
