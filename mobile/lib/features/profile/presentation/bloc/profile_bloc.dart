import 'package:flutter_bloc/flutter_bloc.dart';
import '../../../auth/data/datasources/auth_remote_data_source.dart';
import 'profile_event.dart';
import 'profile_state.dart';

class ProfileBloc extends Bloc<ProfileEvent, ProfileState> {
  final AuthRemoteDataSource remoteDataSource;

  ProfileBloc({required this.remoteDataSource}) : super(ProfileInitial()) {
    on<LoadProfileEvent>(_onLoadProfile);
    on<UpdateProfileEvent>(_onUpdateProfile);
    on<ChangePasswordEvent>(_onChangePassword);
    on<EnableBiometricEvent>(_onEnableBiometric);
    on<LogoutEvent>(_onLogout);
  }

  Future<void> _onLoadProfile(
    LoadProfileEvent event,
    Emitter<ProfileState> emit,
  ) async {
    emit(ProfileLoading());
    try {
      final user = await remoteDataSource.getCurrentUser();
      emit(ProfileLoaded(user));
    } catch (e) {
      emit(ProfileError(e.toString()));
    }
  }

  Future<void> _onUpdateProfile(
    UpdateProfileEvent event,
    Emitter<ProfileState> emit,
  ) async {
    emit(ProfileUpdating());
    try {
      final user = await remoteDataSource.updateProfile(
        firstName: event.firstName,
        lastName: event.lastName,
        phone: event.phone,
        country: event.country,
        timezone: event.timezone,
        preferredLanguage: event.preferredLanguage,
      );
      emit(ProfileUpdated(user));
      emit(ProfileLoaded(user));
    } catch (e) {
      emit(ProfileError(e.toString()));
    }
  }

  Future<void> _onChangePassword(
    ChangePasswordEvent event,
    Emitter<ProfileState> emit,
  ) async {
    emit(PasswordChanging());
    try {
      await remoteDataSource.changePassword(
        currentPassword: event.currentPassword,
        newPassword: event.newPassword,
      );
      emit(PasswordChanged());

      // Reload profile
      final user = await remoteDataSource.getCurrentUser();
      emit(ProfileLoaded(user));
    } catch (e) {
      emit(ProfileError(e.toString()));
    }
  }

  Future<void> _onEnableBiometric(
    EnableBiometricEvent event,
    Emitter<ProfileState> emit,
  ) async {
    try {
      await remoteDataSource.enableBiometric(event.publicKey);
      emit(BiometricEnabled());

      // Reload profile
      final user = await remoteDataSource.getCurrentUser();
      emit(ProfileLoaded(user));
    } catch (e) {
      emit(ProfileError(e.toString()));
    }
  }

  Future<void> _onLogout(
    LogoutEvent event,
    Emitter<ProfileState> emit,
  ) async {
    try {
      await remoteDataSource.logout();
      emit(ProfileInitial());
    } catch (e) {
      emit(ProfileError(e.toString()));
    }
  }
}
