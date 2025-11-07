import 'package:dio/dio.dart';
import '../models/teacher_model.dart';

class TeacherRemoteDataSource {
  final Dio dio;

  TeacherRemoteDataSource({required this.dio});

  Future<List<TeacherModel>> getTeachers({
    String? specialization,
    String? country,
    double? minRating,
    String? search,
  }) async {
    final queryParams = <String, dynamic>{};
    if (specialization != null) queryParams['specializations'] = specialization;
    if (country != null) queryParams['country'] = country;
    if (minRating != null) queryParams['min_rating'] = minRating;
    if (search != null) queryParams['search'] = search;

    final response = await dio.get(
      '/teachers/profiles/',
      queryParameters: queryParams,
    );

    final List<dynamic> results = response.data['results'] ?? response.data;
    return results.map((json) => TeacherModel.fromJson(json)).toList();
  }

  Future<TeacherModel> getTeacherDetails(String teacherId) async {
    final response = await dio.get('/teachers/profiles/$teacherId/');
    return TeacherModel.fromJson(response.data);
  }

  Future<List<dynamic>> getTeacherReviews(String teacherId) async {
    final response = await dio.get('/teachers/profiles/$teacherId/reviews/');
    return response.data['results'] ?? response.data;
  }

  Future<void> submitReview({
    required String teacherId,
    required int overallRating,
    required int teachingQuality,
    required int communication,
    required int punctuality,
    required int patience,
    required String reviewText,
  }) async {
    await dio.post(
      '/teachers/reviews/',
      data: {
        'teacher': teacherId,
        'overall_rating': overallRating,
        'teaching_quality': teachingQuality,
        'communication': communication,
        'punctuality': punctuality,
        'patience': patience,
        'review_text': reviewText,
      },
    );
  }
}
