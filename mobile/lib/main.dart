import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:dio/dio.dart';
import 'package:flutter_localizations/flutter_localizations.dart';
import 'package:shared_preferences/shared_preferences.dart';

import 'core/config/app_config.dart';
import 'core/theme/app_theme.dart';
import 'generated/l10n.dart';

// Data sources
import 'features/auth/data/datasources/auth_remote_data_source.dart';
import 'features/teachers/data/datasources/teacher_remote_data_source.dart';
import 'features/sessions/data/datasources/session_remote_data_source.dart';
import 'features/payments/data/datasources/payment_remote_data_source.dart';

// BLoCs
import 'features/auth/presentation/bloc/auth_bloc.dart';
import 'features/teachers/presentation/bloc/teacher_bloc.dart';
import 'features/sessions/presentation/bloc/session_bloc.dart';
import 'features/payments/presentation/bloc/payment_bloc.dart';
import 'features/profile/presentation/bloc/profile_bloc.dart';
import 'core/language/bloc/language_bloc.dart';
import 'core/language/bloc/language_event.dart';
import 'core/language/bloc/language_state.dart';

// Pages
import 'features/auth/presentation/pages/login_page.dart';
import 'features/auth/presentation/pages/register_page.dart';
import 'features/auth/presentation/pages/change_password_page.dart';
import 'features/teachers/presentation/pages/teachers_list_page.dart';
import 'features/teachers/presentation/pages/teacher_details_page.dart';
import 'features/sessions/presentation/pages/book_session_page.dart';
import 'features/sessions/presentation/pages/my_sessions_page.dart';
import 'features/sessions/presentation/pages/session_details_page.dart';
import 'features/payments/presentation/pages/packages_page.dart';
import 'features/payments/presentation/pages/package_details_page.dart';
import 'features/payments/presentation/pages/subscription_page.dart';
import 'features/payments/presentation/pages/transactions_page.dart';
import 'features/profile/presentation/pages/profile_page.dart';
import 'features/profile/presentation/pages/edit_profile_page.dart';
import 'features/settings/presentation/pages/settings_page.dart';

void main() async {
  WidgetsFlutterBinding.ensureInitialized();

  // Initialize SharedPreferences
  final sharedPreferences = await SharedPreferences.getInstance();

  runApp(MotkenApp(sharedPreferences: sharedPreferences));
}

class MotkenApp extends StatelessWidget {
  final SharedPreferences sharedPreferences;

  const MotkenApp({super.key, required this.sharedPreferences});

  @override
  Widget build(BuildContext context) {
    // Setup Dio
    final dio = Dio(BaseOptions(
      baseUrl: AppConfig.apiBaseUrl,
      connectTimeout: const Duration(seconds: 30),
      receiveTimeout: const Duration(seconds: 30),
      headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
      },
    ));

    // Data sources
    final authDataSource = AuthRemoteDataSourceImpl(dio: dio);
    final teacherDataSource = TeacherRemoteDataSource(dio: dio);
    final sessionDataSource = SessionRemoteDataSource(dio: dio);
    final paymentDataSource = PaymentRemoteDataSource(dio: dio);

    return MultiBlocProvider(
      providers: [
        BlocProvider(
          create: (_) => LanguageBloc(sharedPreferences: sharedPreferences)
            ..add(const LoadLanguageEvent()),
        ),
        BlocProvider(create: (_) => AuthBloc(remoteDataSource: authDataSource)),
        BlocProvider(create: (_) => TeacherBloc(remoteDataSource: teacherDataSource)),
        BlocProvider(create: (_) => SessionBloc(remoteDataSource: sessionDataSource)),
        BlocProvider(create: (_) => PaymentBloc(remoteDataSource: paymentDataSource)),
        BlocProvider(create: (_) => ProfileBloc(remoteDataSource: authDataSource)),
      ],
      child: BlocBuilder<LanguageBloc, LanguageState>(
        builder: (context, languageState) {
          return MaterialApp(
            title: 'Motken',
            debugShowCheckedModeBanner: false,
            theme: AppTheme.lightTheme,
            darkTheme: AppTheme.darkTheme,
            themeMode: ThemeMode.light,
            locale: languageState.locale,
            localizationsDelegates: const [
              S.delegate,
              GlobalMaterialLocalizations.delegate,
              GlobalWidgetsLocalizations.delegate,
              GlobalCupertinoLocalizations.delegate,
            ],
            supportedLocales: S.delegate.supportedLocales,
            localeResolutionCallback: (locale, supportedLocales) {
              if (locale == null) return supportedLocales.first;
              for (var supportedLocale in supportedLocales) {
                if (supportedLocale.languageCode == locale.languageCode) {
                  return supportedLocale;
                }
              }
              return supportedLocales.first;
            },
            initialRoute: '/login',
            routes: {
              '/login': (_) => const LoginPage(),
              '/register': (_) => const RegisterPage(),
              '/home': (_) => const MainNavigationPage(),
              '/teachers': (_) => const TeachersListPage(),
              '/my-sessions': (_) => const MySessionsPage(),
              '/packages': (_) => const PackagesPage(),
              '/subscription': (_) => const SubscriptionPage(),
              '/transactions': (_) => const TransactionsPage(),
              '/profile': (_) => const ProfilePage(),
              '/edit-profile': (_) => const EditProfilePage(),
              '/change-password': (_) => const ChangePasswordPage(),
              '/settings': (_) => const SettingsPage(),
            },
            onGenerateRoute: (settings) {
              // Handle routes with arguments
              if (settings.name == '/book-session') {
                final teacherId = settings.arguments as String;
                return MaterialPageRoute(
                  builder: (_) => BookSessionPage(teacherId: teacherId),
                );
              }
              if (settings.name == '/teacher-details') {
                final teacherId = settings.arguments as String;
                return MaterialPageRoute(
                  builder: (_) => TeacherDetailsPage(teacherId: teacherId),
                );
              }
              if (settings.name == '/session-details') {
                final sessionId = settings.arguments as String;
                return MaterialPageRoute(
                  builder: (_) => SessionDetailsPage(sessionId: sessionId),
                );
              }
              if (settings.name == '/package-details') {
                final packageId = settings.arguments as String;
                return MaterialPageRoute(
                  builder: (_) => PackageDetailsPage(packageId: packageId),
                );
              }
              return null;
            },
          );
        },
      ),
    );
  }
}

class MainNavigationPage extends StatefulWidget {
  const MainNavigationPage({super.key});

  @override
  State<MainNavigationPage> createState() => _MainNavigationPageState();
}

class _MainNavigationPageState extends State<MainNavigationPage> {
  int _selectedIndex = 0;

  @override
  Widget build(BuildContext context) {
    final pages = [
      const HomePage(),
      const TeachersListPage(),
      const MySessionsPage(),
      const ProfilePage(),
    ];

    return Scaffold(
      body: pages[_selectedIndex],
      bottomNavigationBar: NavigationBar(
        selectedIndex: _selectedIndex,
        onDestinationSelected: (i) => setState(() => _selectedIndex = i),
        destinations: [
          NavigationDestination(icon: const Icon(Icons.home), label: S.of(context).home),
          NavigationDestination(icon: const Icon(Icons.school), label: S.of(context).teachers),
          NavigationDestination(icon: const Icon(Icons.event), label: S.of(context).sessions),
          NavigationDestination(icon: const Icon(Icons.person), label: S.of(context).profile),
        ],
      ),
    );
  }
}

class HomePage extends StatelessWidget {
  const HomePage({super.key});

  @override
  Widget build(BuildContext context) {
    final s = S.of(context);
    return Scaffold(
      appBar: AppBar(title: Text(s.appName)),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Card(
              child: Padding(
                padding: const EdgeInsets.all(20),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(s.welcomeTitle, style: const TextStyle(fontSize: 24, fontWeight: FontWeight.bold)),
                    const SizedBox(height: 8),
                    Text(s.welcomeSubtitle),
                    const SizedBox(height: 16),
                    ElevatedButton(
                      onPressed: () => Navigator.pushNamed(context, '/teachers'),
                      child: Text(s.findATeacher),
                    ),
                  ],
                ),
              ),
            ),
            const SizedBox(height: 24),
            Text(s.quickActions, style: const TextStyle(fontSize: 20, fontWeight: FontWeight.bold)),
            const SizedBox(height: 16),
            GridView.count(
              crossAxisCount: 2,
              shrinkWrap: true,
              physics: const NeverScrollableScrollPhysics(),
              mainAxisSpacing: 16,
              crossAxisSpacing: 16,
              children: [
                _QuickActionCard(icon: Icons.school, title: s.findTeachers, onTap: () => Navigator.pushNamed(context, '/teachers')),
                _QuickActionCard(icon: Icons.event, title: s.mySessions, onTap: () => Navigator.pushNamed(context, '/my-sessions')),
                _QuickActionCard(icon: Icons.card_membership, title: s.packages, onTap: () => Navigator.pushNamed(context, '/packages')),
                _QuickActionCard(icon: Icons.receipt_long, title: s.subscription, onTap: () => Navigator.pushNamed(context, '/subscription')),
              ],
            ),
          ],
        ),
      ),
    );
  }
}

class _QuickActionCard extends StatelessWidget {
  final IconData icon;
  final String title;
  final VoidCallback onTap;

  const _QuickActionCard({required this.icon, required this.title, required this.onTap});

  @override
  Widget build(BuildContext context) {
    return Card(
      child: InkWell(
        onTap: onTap,
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Icon(icon, size: 48, color: Theme.of(context).primaryColor),
            const SizedBox(height: 12),
            Text(title, textAlign: TextAlign.center, style: const TextStyle(fontSize: 16, fontWeight: FontWeight.w500)),
          ],
        ),
      ),
    );
  }
}
