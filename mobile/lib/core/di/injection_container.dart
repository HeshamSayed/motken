import 'package:dio/dio.dart';
import 'package:shared_preferences/shared_preferences.dart';
import 'package:flutter_secure_storage/flutter_secure_storage.dart';

import '../config/app_config.dart';

/// Dependency injection container
/// This is a placeholder - implement with GetIt or your preferred DI solution

Future<void> init() async {
  // Initialize dependencies here

  // Core
  // sl.registerLazySingleton<Dio>(() => createDio());
  // sl.registerLazySingleton(() => const FlutterSecureStorage());
  // final sharedPreferences = await SharedPreferences.getInstance();
  // sl.registerLazySingleton(() => sharedPreferences);

  // Data sources
  // Register remote and local data sources

  // Repositories
  // Register repositories

  // Use cases
  // Register use cases

  // BLoCs
  // Register BLoCs
}

/// Create Dio instance with interceptors
Dio createDio() {
  final dio = Dio(
    BaseOptions(
      baseUrl: AppConfig.apiBaseUrl,
      connectTimeout: const Duration(seconds: 30),
      receiveTimeout: const Duration(seconds: 30),
      headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
      },
    ),
  );

  // Add interceptors
  dio.interceptors.add(LogInterceptor(
    requestBody: true,
    responseBody: true,
  ));

  // Add auth interceptor
  // dio.interceptors.add(AuthInterceptor());

  return dio;
}
