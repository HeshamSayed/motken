/// App configuration and constants
class AppConfig {
  // API Configuration
  static const String apiBaseUrl = String.fromEnvironment(
    'API_BASE_URL',
    defaultValue: 'http://localhost:8000/api/v1/',
  );

  static const String apiTimeout = '30';

  // App Configuration
  static const String appName = 'Motken';
  static const String appVersion = '1.0.0';

  // Storage Keys
  static const String accessTokenKey = 'access_token';
  static const String refreshTokenKey = 'refresh_token';
  static const String userDataKey = 'user_data';
  static const String languageKey = 'language';
  static const String themeKey = 'theme_mode';

  // Zoom SDK Configuration
  static const String zoomSdkKey = String.fromEnvironment('ZOOM_SDK_KEY');
  static const String zoomSdkSecret = String.fromEnvironment('ZOOM_SDK_SECRET');

  // Paymob Configuration
  static const String paymobApiKey = String.fromEnvironment('PAYMOB_API_KEY');
  static const String paymobIntegrationId = String.fromEnvironment('PAYMOB_INTEGRATION_ID');
  static const String paymobIframeId = String.fromEnvironment('PAYMOB_IFRAME_ID');

  // Pagination
  static const int defaultPageSize = 20;

  // Session Configuration
  static const List<int> sessionDurations = [30, 45, 60]; // minutes

  // Cache Duration
  static const Duration cacheDuration = Duration(hours: 1);

  // Supported Languages
  static const List<String> supportedLanguages = ['en', 'ar'];

  // Date Formats
  static const String dateFormat = 'yyyy-MM-dd';
  static const String timeFormat = 'HH:mm';
  static const String dateTimeFormat = 'yyyy-MM-dd HH:mm';
}
