import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import '../../../../generated/l10n.dart';
import '../../../../core/language/bloc/language_bloc.dart';
import '../../../../core/language/bloc/language_event.dart';
import '../../../../core/language/bloc/language_state.dart';

class SettingsPage extends StatefulWidget {
  const SettingsPage({super.key});

  @override
  State<SettingsPage> createState() => _SettingsPageState();
}

class _SettingsPageState extends State<SettingsPage> {
  bool _darkMode = false;
  bool _notifications = true;
  bool _sessionReminders = true;
  bool _paymentNotifications = true;

  @override
  Widget build(BuildContext context) {
    final s = S.of(context);
    return BlocBuilder<LanguageBloc, LanguageState>(
      builder: (context, languageState) {
        final currentLanguage = languageState.locale.languageCode == 'en'
            ? s.english
            : s.arabic;

        return Scaffold(
          appBar: AppBar(
            title: Text(s.settings),
          ),
          body: ListView(
            children: [
              _SectionHeader(title: s.appearance),
              SwitchListTile(
                title: Text(s.darkMode),
                subtitle: const Text('Use dark theme'),
                value: _darkMode,
                onChanged: (value) {
                  setState(() => _darkMode = value);
                  // TODO: Implement theme switching
                  ScaffoldMessenger.of(context).showSnackBar(
                    const SnackBar(content: Text('Theme switching coming soon')),
                  );
                },
                secondary: Icon(
                  _darkMode ? Icons.dark_mode : Icons.light_mode,
                ),
              ),
              ListTile(
                leading: const Icon(Icons.language),
                title: Text(s.language),
                subtitle: Text(currentLanguage),
                trailing: const Icon(Icons.chevron_right),
                onTap: () => _showLanguageDialog(),
              ),
              const Divider(height: 32),
              _SectionHeader(title: s.notificationSettings),
              SwitchListTile(
                title: Text(s.notifications),
                subtitle: const Text('Receive push notifications'),
                value: _notifications,
                onChanged: (value) {
                  setState(() => _notifications = value);
                },
                secondary: const Icon(Icons.notifications),
              ),
              SwitchListTile(
                title: Text(s.sessionReminders),
                subtitle: const Text('Get reminded before sessions'),
                value: _sessionReminders,
                onChanged: _notifications
                    ? (value) {
                        setState(() => _sessionReminders = value);
                      }
                    : null,
                secondary: const Icon(Icons.event),
              ),
              SwitchListTile(
                title: Text(s.paymentNotifications),
                subtitle: const Text('Receive payment updates'),
                value: _paymentNotifications,
                onChanged: _notifications
                    ? (value) {
                        setState(() => _paymentNotifications = value);
                      }
                    : null,
                secondary: const Icon(Icons.payment),
              ),
              const Divider(height: 32),
              _SectionHeader(title: 'Support'),
              ListTile(
                leading: const Icon(Icons.help),
                title: Text(s.helpSupport),
                subtitle: const Text('Get help with the app'),
                trailing: const Icon(Icons.chevron_right),
                onTap: () {
                  // TODO: Implement help page
                },
              ),
              ListTile(
                leading: const Icon(Icons.privacy_tip),
                title: Text(s.privacyPolicy),
                trailing: const Icon(Icons.chevron_right),
                onTap: () {
                  // TODO: Implement privacy policy
                },
              ),
              ListTile(
                leading: const Icon(Icons.description),
                title: Text(s.termsOfService),
                trailing: const Icon(Icons.chevron_right),
                onTap: () {
                  // TODO: Implement terms of service
                },
              ),
              ListTile(
                leading: const Icon(Icons.info),
                title: Text(s.aboutApp),
                subtitle: Text('${s.version} 1.0.0'),
                onTap: () => _showAboutDialog(),
              ),
            ],
          ),
        );
      },
    );
  }

  void _showLanguageDialog() {
    final s = S.of(context);
    final currentLocale = context.read<LanguageBloc>().state.locale.languageCode;

    showDialog(
      context: context,
      builder: (dialogContext) => AlertDialog(
        title: Text(s.selectLanguage),
        content: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            RadioListTile<String>(
              title: Text(s.english),
              value: 'en',
              groupValue: currentLocale,
              onChanged: (value) {
                if (value != null) {
                  context.read<LanguageBloc>().add(
                        ChangeLanguageEvent(Locale(value)),
                      );
                  Navigator.pop(dialogContext);
                }
              },
            ),
            RadioListTile<String>(
              title: Text(s.arabic),
              value: 'ar',
              groupValue: currentLocale,
              onChanged: (value) {
                if (value != null) {
                  context.read<LanguageBloc>().add(
                        ChangeLanguageEvent(Locale(value)),
                      );
                  Navigator.pop(dialogContext);
                }
              },
            ),
          ],
        ),
      ),
    );
  }

  void _showAboutDialog() {
    final s = S.of(context);
    showAboutDialog(
      context: context,
      applicationName: s.appName,
      applicationVersion: '1.0.0',
      applicationIcon: const FlutterLogo(size: 48),
      children: [
        Text(
          '${s.appTagline}\n\n'
          'Connect with qualified Quran teachers for personalized online sessions.',
        ),
      ],
    );
  }
}

class _SectionHeader extends StatelessWidget {
  final String title;

  const _SectionHeader({required this.title});

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.fromLTRB(16, 16, 16, 8),
      child: Text(
        title,
        style: TextStyle(
          fontSize: 14,
          fontWeight: FontWeight.bold,
          color: Theme.of(context).primaryColor,
        ),
      ),
    );
  }
}
