import 'package:equatable/equatable.dart';
import 'package:flutter/material.dart';

class LanguageState extends Equatable {
  final Locale locale;
  final bool isRTL;

  const LanguageState({
    required this.locale,
    required this.isRTL,
  });

  factory LanguageState.initial() {
    return const LanguageState(
      locale: Locale('en'),
      isRTL: false,
    );
  }

  LanguageState copyWith({
    Locale? locale,
    bool? isRTL,
  }) {
    return LanguageState(
      locale: locale ?? this.locale,
      isRTL: isRTL ?? this.isRTL,
    );
  }

  @override
  List<Object?> get props => [locale, isRTL];
}
