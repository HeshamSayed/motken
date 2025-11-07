import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:equatable/equatable.dart';
import '../../data/models/user_model.dart';

// Events
abstract class AuthEvent extends Equatable {
  @override
  List<Object?> get props => [];
}

class LoginEvent extends AuthEvent {
  final String email;
  final String password;

  LoginEvent({required this.email, required this.password});

  @override
  List<Object?> get props => [email, password];
}

class RegisterEvent extends AuthEvent {
  final Map<String, dynamic> userData;

  RegisterEvent({required this.userData});

  @override
  List<Object?> get props => [userData];
}

class LogoutEvent extends AuthEvent {}

class CheckAuthStatusEvent extends AuthEvent {}

class RefreshTokenEvent extends AuthEvent {
  final String refreshToken;

  RefreshTokenEvent({required this.refreshToken});

  @override
  List<Object?> get props => [refreshToken];
}

// States
abstract class AuthState extends Equatable {
  @override
  List<Object?> get props => [];
}

class AuthInitial extends AuthState {}

class AuthLoading extends AuthState {}

class Authenticated extends AuthState {
  final UserModel user;
  final String accessToken;
  final String refreshToken;

  Authenticated({
    required this.user,
    required this.accessToken,
    required this.refreshToken,
  });

  @override
  List<Object?> get props => [user, accessToken, refreshToken];
}

class Unauthenticated extends AuthState {}

class AuthError extends AuthState {
  final String message;

  AuthError({required this.message});

  @override
  List<Object?> get props => [message];
}

// BLoC
class AuthBloc extends Bloc<AuthEvent, AuthState> {
  // final AuthRepository authRepository;

  AuthBloc(/*{required this.authRepository}*/) : super(AuthInitial()) {
    on<LoginEvent>(_onLogin);
    on<RegisterEvent>(_onRegister);
    on<LogoutEvent>(_onLogout);
    on<CheckAuthStatusEvent>(_onCheckAuthStatus);
    on<RefreshTokenEvent>(_onRefreshToken);
  }

  Future<void> _onLogin(LoginEvent event, Emitter<AuthState> emit) async {
    emit(AuthLoading());
    try {
      // TODO: Implement actual login
      // final response = await authRepository.login(event.email, event.password);
      await Future.delayed(const Duration(seconds: 1)); // Simulate API call

      // Mock response
      final user = UserModel(
        id: '123',
        email: event.email,
        firstName: 'John',
        lastName: 'Doe',
        userType: 'student',
      );

      emit(Authenticated(
        user: user,
        accessToken: 'mock_access_token',
        refreshToken: 'mock_refresh_token',
      ));
    } catch (e) {
      emit(AuthError(message: e.toString()));
    }
  }

  Future<void> _onRegister(RegisterEvent event, Emitter<AuthState> emit) async {
    emit(AuthLoading());
    try {
      // TODO: Implement actual registration
      // final response = await authRepository.register(event.userData);
      await Future.delayed(const Duration(seconds: 1));

      emit(Unauthenticated());
    } catch (e) {
      emit(AuthError(message: e.toString()));
    }
  }

  Future<void> _onLogout(LogoutEvent event, Emitter<AuthState> emit) async {
    try {
      // TODO: Clear tokens from storage
      // await authRepository.logout();
      emit(Unauthenticated());
    } catch (e) {
      emit(AuthError(message: e.toString()));
    }
  }

  Future<void> _onCheckAuthStatus(
      CheckAuthStatusEvent event, Emitter<AuthState> emit) async {
    try {
      // TODO: Check if user is logged in
      // final tokens = await storage.getTokens();
      // if (tokens != null) {
      //   final user = await authRepository.getCurrentUser();
      //   emit(Authenticated(user: user, ...));
      // } else {
      emit(Unauthenticated());
      // }
    } catch (e) {
      emit(Unauthenticated());
    }
  }

  Future<void> _onRefreshToken(
      RefreshTokenEvent event, Emitter<AuthState> emit) async {
    try {
      // TODO: Refresh token
      // final newTokens = await authRepository.refreshToken(event.refreshToken);
      // emit(Authenticated(...));
    } catch (e) {
      emit(Unauthenticated());
    }
  }
}
