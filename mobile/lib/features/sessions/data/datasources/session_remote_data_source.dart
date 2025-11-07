import 'package:dio/dio.dart';
import '../models/session_model.dart';

class SessionRemoteDataSource {
  final Dio dio;

  SessionRemoteDataSource({required this.dio});

  Future<SessionModel> bookSession({
    required String teacherId,
    required String scheduledDate,
    required String scheduledTime,
    required int duration,
    String? curriculum,
    String? lessonTopic,
  }) async {
    final response = await dio.post(
      '/sessions/book/',
      data: {
        'teacher': teacherId,
        'scheduled_date': scheduledDate,
        'scheduled_time': scheduledTime,
        'duration': duration,
        if (curriculum != null) 'curriculum': curriculum,
        if (lessonTopic != null) 'lesson_topic': lessonTopic,
      },
    );
    return SessionModel.fromJson(response.data['session']);
  }

  Future<List<SessionModel>> getMySessions({
    String? status,
    String? ordering,
  }) async {
    final response = await dio.get(
      '/sessions/my_sessions/',
      queryParameters: {
        if (status != null) 'status': status,
        if (ordering != null) 'ordering': ordering,
      },
    );
    final List<dynamic> results = response.data['results'] ?? response.data;
    return results.map((json) => SessionModel.fromJson(json)).toList();
  }

  Future<SessionModel> getSessionDetails(String sessionId) async {
    final response = await dio.get('/sessions/$sessionId/');
    return SessionModel.fromJson(response.data);
  }

  Future<Map<String, dynamic>> getJoinUrl(String sessionId) async {
    final response = await dio.get('/sessions/$sessionId/join/');
    return response.data;
  }

  Future<SessionModel> cancelSession(
    String sessionId,
    String cancellationReason,
  ) async {
    final response = await dio.post(
      '/sessions/$sessionId/cancel/',
      data: {'cancellation_reason': cancellationReason},
    );
    return SessionModel.fromJson(response.data['session']);
  }

  Future<SessionModel> completeSession(String sessionId) async {
    final response = await dio.post('/sessions/$sessionId/complete/');
    return SessionModel.fromJson(response.data['session']);
  }
}
