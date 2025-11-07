import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:shared_preferences/shared_preferences.dart';
import '../../../core/config/app_config.dart';
import 'language_event.dart';
import 'language_state.dart';

class LanguageBloc extends Bloc<LanguageEvent, LanguageState> {
  final SharedPreferences sharedPreferences;

  LanguageBloc({required this.sharedPreferences})
      : super(LanguageState.initial()) {
    on<LoadLanguageEvent>(_onLoadLanguage);
    on<ChangeLanguageEvent>(_onChangeLanguage);
    on<ToggleLanguageEvent>(_onToggleLanguage);
  }

  /// Load saved language preference from SharedPreferences
  Future<void> _onLoadLanguage(
    LoadLanguageEvent event,
    Emitter<LanguageState> emit,
  ) async {
    try {
      final languageCode =
          sharedPreferences.getString(AppConfig.languageKey) ?? 'en';
      final locale = Locale(languageCode);
      final isRTL = languageCode == 'ar';

      emit(state.copyWith(
        locale: locale,
        isRTL: isRTL,
      ));
    } catch (e) {
      // If loading fails, keep the default language
      debugPrint('Error loading language: $e');
    }
  }

  /// Change language to a specific locale
  Future<void> _onChangeLanguage(
    ChangeLanguageEvent event,
    Emitter<LanguageState> emit,
  ) async {
    try {
      final languageCode = event.locale.languageCode;

      // Validate language is supported
      if (!AppConfig.supportedLanguages.contains(languageCode)) {
        debugPrint('Language $languageCode is not supported');
        return;
      }

      // Save to SharedPreferences
      await sharedPreferences.setString(AppConfig.languageKey, languageCode);

      // Determine if RTL
      final isRTL = languageCode == 'ar';

      // Emit new state
      emit(state.copyWith(
        locale: event.locale,
        isRTL: isRTL,
      ));

      debugPrint('Language changed to: $languageCode (RTL: $isRTL)');
    } catch (e) {
      debugPrint('Error changing language: $e');
    }
  }

  /// Toggle between English and Arabic
  Future<void> _onToggleLanguage(
    ToggleLanguageEvent event,
    Emitter<LanguageState> emit,
  ) async {
    final currentLanguage = state.locale.languageCode;
    final newLanguage = currentLanguage == 'en' ? 'ar' : 'en';

    add(ChangeLanguageEvent(Locale(newLanguage)));
  }
}
