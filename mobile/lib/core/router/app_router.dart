import 'package:go_router/go_router.dart';
import 'package:flutter/material.dart';

/// App routing configuration
class AppRouter {
  static final GoRouter router = GoRouter(
    initialLocation: '/splash',
    routes: [
      // Splash Screen
      GoRoute(
        path: '/splash',
        name: 'splash',
        builder: (context, state) => const SplashScreen(),
      ),

      // Auth Routes
      GoRoute(
        path: '/login',
        name: 'login',
        builder: (context, state) => const LoginScreen(),
      ),
      GoRoute(
        path: '/register',
        name: 'register',
        builder: (context, state) => const RegisterScreen(),
      ),

      // Main App Routes
      GoRoute(
        path: '/',
        name: 'home',
        builder: (context, state) => const HomeScreen(),
      ),

      // Student Routes
      GoRoute(
        path: '/teachers',
        name: 'teachers',
        builder: (context, state) => const TeachersScreen(),
      ),
      GoRoute(
        path: '/teacher/:id',
        name: 'teacher_detail',
        builder: (context, state) {
          final id = state.pathParameters['id']!;
          return TeacherDetailScreen(teacherId: id);
        },
      ),

      // Sessions Routes
      GoRoute(
        path: '/sessions',
        name: 'sessions',
        builder: (context, state) => const SessionsScreen(),
      ),
      GoRoute(
        path: '/book-session',
        name: 'book_session',
        builder: (context, state) => const BookSessionScreen(),
      ),

      // Learning Routes
      GoRoute(
        path: '/learning',
        name: 'learning',
        builder: (context, state) => const LearningScreen(),
      ),

      // Profile Routes
      GoRoute(
        path: '/profile',
        name: 'profile',
        builder: (context, state) => const ProfileScreen(),
      ),
    ],

    // Error handling
    errorBuilder: (context, state) => const ErrorScreen(),
  );
}

// Placeholder screens - to be implemented
class SplashScreen extends StatelessWidget {
  const SplashScreen({super.key});
  @override
  Widget build(BuildContext context) => const Scaffold(body: Center(child: CircularProgressIndicator()));
}

class LoginScreen extends StatelessWidget {
  const LoginScreen({super.key});
  @override
  Widget build(BuildContext context) => const Scaffold(body: Center(child: Text('Login Screen')));
}

class RegisterScreen extends StatelessWidget {
  const RegisterScreen({super.key});
  @override
  Widget build(BuildContext context) => const Scaffold(body: Center(child: Text('Register Screen')));
}

class HomeScreen extends StatelessWidget {
  const HomeScreen({super.key});
  @override
  Widget build(BuildContext context) => const Scaffold(body: Center(child: Text('Home Screen')));
}

class TeachersScreen extends StatelessWidget {
  const TeachersScreen({super.key});
  @override
  Widget build(BuildContext context) => const Scaffold(body: Center(child: Text('Teachers Screen')));
}

class TeacherDetailScreen extends StatelessWidget {
  final String teacherId;
  const TeacherDetailScreen({super.key, required this.teacherId});
  @override
  Widget build(BuildContext context) => Scaffold(body: Center(child: Text('Teacher Detail: $teacherId')));
}

class SessionsScreen extends StatelessWidget {
  const SessionsScreen({super.key});
  @override
  Widget build(BuildContext context) => const Scaffold(body: Center(child: Text('Sessions Screen')));
}

class BookSessionScreen extends StatelessWidget {
  const BookSessionScreen({super.key});
  @override
  Widget build(BuildContext context) => const Scaffold(body: Center(child: Text('Book Session Screen')));
}

class LearningScreen extends StatelessWidget {
  const LearningScreen({super.key});
  @override
  Widget build(BuildContext context) => const Scaffold(body: Center(child: Text('Learning Screen')));
}

class ProfileScreen extends StatelessWidget {
  const ProfileScreen({super.key});
  @override
  Widget build(BuildContext context) => const Scaffold(body: Center(child: Text('Profile Screen')));
}

class ErrorScreen extends StatelessWidget {
  const ErrorScreen({super.key});
  @override
  Widget build(BuildContext context) => const Scaffold(body: Center(child: Text('Error Screen')));
}
