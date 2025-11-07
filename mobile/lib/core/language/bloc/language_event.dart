import 'package:equatable/equatable.dart';
import 'package:flutter/material.dart';

abstract class LanguageEvent extends Equatable {
  const LanguageEvent();

  @override
  List<Object?> get props => [];
}

/// Event to load the saved language preference
class LoadLanguageEvent extends LanguageEvent {
  const LoadLanguageEvent();
}

/// Event to change the language
class ChangeLanguageEvent extends LanguageEvent {
  final Locale locale;

  const ChangeLanguageEvent(this.locale);

  @override
  List<Object?> get props => [locale];
}

/// Event to toggle between English and Arabic
class ToggleLanguageEvent extends LanguageEvent {
  const ToggleLanguageEvent();
}
