abstract class ProfileEvent {}

class LoadProfileEvent extends ProfileEvent {}

class UpdateProfileEvent extends ProfileEvent {
  final String firstName;
  final String lastName;
  final String? phone;
  final String? country;
  final String? timezone;
  final String? preferredLanguage;

  UpdateProfileEvent({
    required this.firstName,
    required this.lastName,
    this.phone,
    this.country,
    this.timezone,
    this.preferredLanguage,
  });
}

class ChangePasswordEvent extends ProfileEvent {
  final String currentPassword;
  final String newPassword;

  ChangePasswordEvent({
    required this.currentPassword,
    required this.newPassword,
  });
}

class EnableBiometricEvent extends ProfileEvent {
  final String publicKey;
  EnableBiometricEvent(this.publicKey);
}

class LogoutEvent extends ProfileEvent {}
