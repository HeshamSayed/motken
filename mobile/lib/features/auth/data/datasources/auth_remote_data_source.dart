import 'package:dio/dio.dart';
import '../models/user_model.dart';

abstract class AuthRemoteDataSource {
  Future<LoginResponse> login(String email, String password);
  Future<LoginResponse> register(Map<String, dynamic> data);
  Future<UserModel> getCurrentUser();
  Future<UserModel> updateProfile({
    required String firstName,
    required String lastName,
    String? phone,
    String? country,
    String? timezone,
    String? preferredLanguage,
  });
  Future<void> changePassword({
    required String currentPassword,
    required String newPassword,
  });
  Future<void> enableBiometric(String publicKey);
  Future<void> logout();
}

class AuthRemoteDataSourceImpl implements AuthRemoteDataSource {
  final Dio dio;

  AuthRemoteDataSourceImpl({required this.dio});

  @override
  Future<LoginResponse> login(String email, String password) async {
    try {
      final response = await dio.post(
        '/auth/login/',
        data: {
          'email': email,
          'password': password,
        },
      );

      return LoginResponse.fromJson(response.data);
    } on DioException catch (e) {
      throw Exception('Login failed: ${e.message}');
    }
  }

  @override
  Future<LoginResponse> register(Map<String, dynamic> data) async {
    try {
      final response = await dio.post(
        '/auth/register/',
        data: data,
      );

      return LoginResponse.fromJson(response.data);
    } on DioException catch (e) {
      throw Exception('Registration failed: ${e.message}');
    }
  }

  @override
  Future<UserModel> getCurrentUser() async {
    try {
      final response = await dio.get('/auth/users/me/');
      return UserModel.fromJson(response.data);
    } on DioException catch (e) {
      throw Exception('Failed to get user: ${e.message}');
    }
  }

  @override
  Future<UserModel> updateProfile({
    required String firstName,
    required String lastName,
    String? phone,
    String? country,
    String? timezone,
    String? preferredLanguage,
  }) async {
    try {
      final response = await dio.put(
        '/auth/users/update_profile/',
        data: {
          'first_name': firstName,
          'last_name': lastName,
          if (phone != null) 'phone': phone,
          if (country != null) 'country': country,
          if (timezone != null) 'timezone': timezone,
          if (preferredLanguage != null) 'preferred_language': preferredLanguage,
        },
      );
      return UserModel.fromJson(response.data);
    } on DioException catch (e) {
      throw Exception('Failed to update profile: ${e.message}');
    }
  }

  @override
  Future<void> changePassword({
    required String currentPassword,
    required String newPassword,
  }) async {
    try {
      await dio.post(
        '/auth/users/change_password/',
        data: {
          'current_password': currentPassword,
          'new_password': newPassword,
        },
      );
    } on DioException catch (e) {
      throw Exception('Failed to change password: ${e.message}');
    }
  }

  @override
  Future<void> enableBiometric(String publicKey) async {
    try {
      await dio.post(
        '/auth/users/enable_biometric/',
        data: {
          'public_key': publicKey,
        },
      );
    } on DioException catch (e) {
      throw Exception('Failed to enable biometric: ${e.message}');
    }
  }

  @override
  Future<void> logout() async {
    try {
      await dio.post('/auth/users/logout/');
    } on DioException catch (e) {
      throw Exception('Logout failed: ${e.message}');
    }
  }
}
