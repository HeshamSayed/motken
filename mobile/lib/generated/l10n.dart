// GENERATED FILE - DO NOT EDIT
// This file was generated from ARB files

import 'dart:async';

import 'package:flutter/material.dart';
import 'package:intl/intl.dart';
import 'intl/messages_all.dart' as messages_all;

class S {
  S();

  static S? _current;

  static S get current {
    assert(_current != null,
        'No instance of S was loaded. Try to initialize the S delegate before accessing S.current.');
    return _current!;
  }

  static const AppLocalizationDelegate delegate = AppLocalizationDelegate();

  static Future<S> load(Locale locale) {
    final name = (locale.countryCode?.isEmpty ?? false)
        ? locale.languageCode
        : locale.toString();
    final localeName = Intl.canonicalizedLocale(name);
    return messages_all.initializeMessages(localeName).then((_) {
      Intl.defaultLocale = localeName;
      final instance = S();
      S._current = instance;
      return instance;
    });
  }

  static S of(BuildContext context) {
    final instance = Localizations.of<S>(context, S);
    assert(instance != null,
        'No instance of S present in the widget tree. Did you add S.delegate in localizationsDelegates?');
    return instance!;
  }

  // App Name and Branding
  String get appName => Intl.message('Motken', name: 'appName');
  String get appTagline =>
      Intl.message('Learn Quran Online', name: 'appTagline');
  String get welcomeTitle =>
      Intl.message('Welcome to Motken', name: 'welcomeTitle');
  String get welcomeSubtitle => Intl.message(
      'Start your Quran learning journey today',
      name: 'welcomeSubtitle');

  // Authentication
  String get login => Intl.message('Login', name: 'login');
  String get register => Intl.message('Register', name: 'register');
  String get email => Intl.message('Email', name: 'email');
  String get password => Intl.message('Password', name: 'password');
  String get confirmPassword =>
      Intl.message('Confirm Password', name: 'confirmPassword');
  String get forgotPassword =>
      Intl.message('Forgot Password?', name: 'forgotPassword');
  String get dontHaveAccount =>
      Intl.message('Don\'t have an account?', name: 'dontHaveAccount');
  String get alreadyHaveAccount =>
      Intl.message('Already have an account?', name: 'alreadyHaveAccount');
  String get signUp => Intl.message('Sign Up', name: 'signUp');
  String get signIn => Intl.message('Sign In', name: 'signIn');
  String get createAccount =>
      Intl.message('Create Account', name: 'createAccount');
  String get joinMotken => Intl.message('Join Motken', name: 'joinMotken');
  String get startJourneyToday => Intl.message(
      'Start your Quran learning journey today',
      name: 'startJourneyToday');
  String get firstName => Intl.message('First Name', name: 'firstName');
  String get lastName => Intl.message('Last Name', name: 'lastName');
  String get phone => Intl.message('Phone Number', name: 'phone');
  String get phoneOptional =>
      Intl.message('Phone Number (Optional)', name: 'phoneOptional');
  String get iAmA => Intl.message('I am a:', name: 'iAmA');
  String get student => Intl.message('Student', name: 'student');
  String get teacher => Intl.message('Teacher', name: 'teacher');
  String get currentPassword =>
      Intl.message('Current Password', name: 'currentPassword');
  String get newPassword => Intl.message('New Password', name: 'newPassword');
  String get changePassword =>
      Intl.message('Change Password', name: 'changePassword');
  String get updatePassword =>
      Intl.message('Update Password', name: 'updatePassword');

  // Validation
  String get pleaseEnterEmail =>
      Intl.message('Please enter your email', name: 'pleaseEnterEmail');
  String get pleaseEnterValidEmail => Intl.message(
      'Please enter a valid email address',
      name: 'pleaseEnterValidEmail');
  String get pleaseEnterPassword =>
      Intl.message('Please enter your password', name: 'pleaseEnterPassword');
  String get passwordTooShort => Intl.message(
      'Password must be at least 6 characters',
      name: 'passwordTooShort');
  String get passwordsDoNotMatch =>
      Intl.message('Passwords do not match', name: 'passwordsDoNotMatch');
  String get pleaseEnterFirstName =>
      Intl.message('Please enter your first name', name: 'pleaseEnterFirstName');
  String get pleaseEnterLastName =>
      Intl.message('Please enter your last name', name: 'pleaseEnterLastName');
  String get pleaseSelectUserType =>
      Intl.message('Please select a user type', name: 'pleaseSelectUserType');
  String get pleaseEnterCurrentPassword => Intl.message(
      'Please enter your current password',
      name: 'pleaseEnterCurrentPassword');
  String get pleaseEnterNewPassword => Intl.message(
      'Please enter your new password',
      name: 'pleaseEnterNewPassword');

  // Home
  String get home => Intl.message('Home', name: 'home');
  String get quickActions => Intl.message('Quick Actions', name: 'quickActions');
  String get findATeacher =>
      Intl.message('Find a Teacher', name: 'findATeacher');
  String get findTeachers => Intl.message('Find Teachers', name: 'findTeachers');
  String get mySessions => Intl.message('My Sessions', name: 'mySessions');
  String get packages => Intl.message('Packages', name: 'packages');
  String get subscription => Intl.message('Subscription', name: 'subscription');
  String get mySubscription =>
      Intl.message('My Subscription', name: 'mySubscription');

  // Navigation
  String get teachers => Intl.message('Teachers', name: 'teachers');
  String get sessions => Intl.message('Sessions', name: 'sessions');
  String get profile => Intl.message('Profile', name: 'profile');

  // Teachers
  String get allTeachers => Intl.message('All', name: 'allTeachers');
  String get tajweed => Intl.message('Tajweed', name: 'tajweed');
  String get memorization => Intl.message('Memorization', name: 'memorization');
  String get reading => Intl.message('Reading', name: 'reading');
  String get noTeachersFound =>
      Intl.message('No teachers found', name: 'noTeachersFound');
  String get tryAdjustingFilters =>
      Intl.message('Try adjusting your filters', name: 'tryAdjustingFilters');
  String get clearFilters => Intl.message('Clear Filters', name: 'clearFilters');
  String get filterTeachers =>
      Intl.message('Filter Teachers', name: 'filterTeachers');
  String get specialization =>
      Intl.message('Specialization', name: 'specialization');
  String get all => Intl.message('All', name: 'all');
  String get maxPrice => Intl.message('Max Price', name: 'maxPrice');
  String get minRating => Intl.message('Min Rating', name: 'minRating');
  String get applyFilters => Intl.message('Apply Filters', name: 'applyFilters');
  String yearsExperience(int years) =>
      Intl.message('$years years experience', name: 'yearsExperience', args: [years]);
  String get perSession => Intl.message('per session', name: 'perSession');
  String get bookNow => Intl.message('Book Now', name: 'bookNow');
  String get viewProfile => Intl.message('View Profile', name: 'viewProfile');
  String get teacherDetails =>
      Intl.message('Teacher Details', name: 'teacherDetails');
  String get about => Intl.message('About', name: 'about');
  String get reviews => Intl.message('Reviews', name: 'reviews');
  String get specializations =>
      Intl.message('Specializations', name: 'specializations');
  String get teachingStyle =>
      Intl.message('Teaching Style', name: 'teachingStyle');
  String get availability => Intl.message('Availability', name: 'availability');
  String get pricingTiers => Intl.message('Pricing Tiers', name: 'pricingTiers');
  String sessionPrice(int duration, String price) =>
      Intl.message('$duration min - \$$price', name: 'sessionPrice', args: [duration, price]);
  String get bookSession => Intl.message('Book Session', name: 'bookSession');
  String get noReviewsYet =>
      Intl.message('No reviews yet', name: 'noReviewsYet');
  String get beFirstToReview => Intl.message(
      'Be the first to leave a review for this teacher',
      name: 'beFirstToReview');

  // Sessions
  String get upcomingSessions =>
      Intl.message('Upcoming', name: 'upcomingSessions');
  String get completedSessions =>
      Intl.message('Completed', name: 'completedSessions');
  String get cancelledSessions =>
      Intl.message('Cancelled', name: 'cancelledSessions');
  String get noSessionsFound =>
      Intl.message('No sessions found', name: 'noSessionsFound');
  String get noSessionsInCategory =>
      Intl.message('No sessions in this category', name: 'noSessionsInCategory');
  String get sessionDetails =>
      Intl.message('Session Details', name: 'sessionDetails');
  String get duration => Intl.message('Duration', name: 'duration');
  String get minutes => Intl.message('minutes', name: 'minutes');
  String get min => Intl.message('min', name: 'min');
  String get price => Intl.message('Price', name: 'price');
  String get status => Intl.message('Status', name: 'status');
  String get scheduledFor => Intl.message('Scheduled for', name: 'scheduledFor');
  String get joinSession => Intl.message('Join Session', name: 'joinSession');
  String get cancelSession => Intl.message('Cancel Session', name: 'cancelSession');
  String get rescheduleSession =>
      Intl.message('Reschedule Session', name: 'rescheduleSession');
  String get selectDate => Intl.message('Select Date', name: 'selectDate');
  String get selectTime => Intl.message('Select Time', name: 'selectTime');
  String get selectDuration =>
      Intl.message('Select Duration', name: 'selectDuration');
  String get notes => Intl.message('Notes', name: 'notes');
  String get notesOptional => Intl.message(
      'Add any notes for the teacher (optional)',
      name: 'notesOptional');
  String get confirmBooking =>
      Intl.message('Confirm Booking', name: 'confirmBooking');
  String bookingFor(String teacherName) =>
      Intl.message('Booking for $teacherName', name: 'bookingFor', args: [teacherName]);
  String get totalAmount => Intl.message('Total Amount', name: 'totalAmount');
  String get confirmAndPay =>
      Intl.message('Confirm & Pay', name: 'confirmAndPay');

  // Payments
  String get choosePackage =>
      Intl.message('Choose a Package', name: 'choosePackage');
  String get popular => Intl.message('POPULAR', name: 'popular');
  String get choosePlan => Intl.message('Choose Plan', name: 'choosePlan');
  String get session => Intl.message('session', name: 'session');
  String sessionsCount(int count) =>
      Intl.message('$count Sessions', name: 'sessionsCount', args: [count]);
  String get days => Intl.message('days', name: 'days');
  String validityDays(int days) =>
      Intl.message('$days days', name: 'validityDays', args: [days]);
  String get packageDetails =>
      Intl.message('Package Details', name: 'packageDetails');
  String get features => Intl.message('Features', name: 'features');
  String get validity => Intl.message('Validity', name: 'validity');
  String get haveCoupon =>
      Intl.message('Have a coupon code?', name: 'haveCoupon');
  String get couponCode => Intl.message('Coupon Code', name: 'couponCode');
  String get applyCoupon => Intl.message('Apply Coupon', name: 'applyCoupon');
  String get couponApplied =>
      Intl.message('Coupon applied successfully!', name: 'couponApplied');
  String get discount => Intl.message('Discount', name: 'discount');
  String get totalPrice => Intl.message('Total Price', name: 'totalPrice');
  String get proceedToPayment =>
      Intl.message('Proceed to Payment', name: 'proceedToPayment');
  String get transactions => Intl.message('Transactions', name: 'transactions');
  String get transactionHistory =>
      Intl.message('Transaction History', name: 'transactionHistory');
  String get noTransactionsFound =>
      Intl.message('No transactions found', name: 'noTransactionsFound');
  String get noTransactionsYet =>
      Intl.message('You haven\'t made any transactions yet', name: 'noTransactionsYet');
  String get amount => Intl.message('Amount', name: 'amount');
  String get date => Intl.message('Date', name: 'date');
  String get type => Intl.message('Type', name: 'type');
  String get transactionDetails =>
      Intl.message('Transaction Details', name: 'transactionDetails');
  String get transactionId =>
      Intl.message('Transaction ID', name: 'transactionId');
  String get paymentMethod =>
      Intl.message('Payment Method', name: 'paymentMethod');
  String get package => Intl.message('Package', name: 'package');
  String get description => Intl.message('Description', name: 'description');
  String get pending => Intl.message('Pending', name: 'pending');
  String get completed => Intl.message('Completed', name: 'completed');
  String get failed => Intl.message('Failed', name: 'failed');
  String get refunded => Intl.message('Refunded', name: 'refunded');

  // Profile
  String get myProfile => Intl.message('My Profile', name: 'myProfile');
  String get editProfile => Intl.message('Edit Profile', name: 'editProfile');
  String get saveChanges => Intl.message('Save Changes', name: 'saveChanges');
  String get cancel => Intl.message('Cancel', name: 'cancel');
  String get myProgress => Intl.message('My Progress', name: 'myProgress');
  String get notifications => Intl.message('Notifications', name: 'notifications');
  String get helpSupport => Intl.message('Help & Support', name: 'helpSupport');
  String get privacyPolicy =>
      Intl.message('Privacy Policy', name: 'privacyPolicy');
  String get termsOfService =>
      Intl.message('Terms of Service', name: 'termsOfService');
  String get aboutApp => Intl.message('About', name: 'aboutApp');
  String get logout => Intl.message('Logout', name: 'logout');
  String get areYouSureLogout =>
      Intl.message('Are you sure you want to logout?', name: 'areYouSureLogout');
  String get version => Intl.message('Version', name: 'version');

  // Settings
  String get settings => Intl.message('Settings', name: 'settings');
  String get appearance => Intl.message('Appearance', name: 'appearance');
  String get darkMode => Intl.message('Dark Mode', name: 'darkMode');
  String get language => Intl.message('Language', name: 'language');
  String get english => Intl.message('English', name: 'english');
  String get arabic => Intl.message('العربية', name: 'arabic');
  String get selectLanguage =>
      Intl.message('Select Language', name: 'selectLanguage');
  String get notificationSettings =>
      Intl.message('Notification Settings', name: 'notificationSettings');
  String get sessionReminders =>
      Intl.message('Session Reminders', name: 'sessionReminders');
  String get paymentNotifications =>
      Intl.message('Payment Notifications', name: 'paymentNotifications');
  String get newMessagesNotifications =>
      Intl.message('New Messages', name: 'newMessagesNotifications');
  String get promotionalNotifications =>
      Intl.message('Promotional Offers', name: 'promotionalNotifications');

  // Common
  String get save => Intl.message('Save', name: 'save');
  String get edit => Intl.message('Edit', name: 'edit');
  String get delete => Intl.message('Delete', name: 'delete');
  String get close => Intl.message('Close', name: 'close');
  String get ok => Intl.message('OK', name: 'ok');
  String get yes => Intl.message('Yes', name: 'yes');
  String get no => Intl.message('No', name: 'no');
  String get retry => Intl.message('Retry', name: 'retry');
  String get loading => Intl.message('Loading...', name: 'loading');
  String get error => Intl.message('Error', name: 'error');
  String get success => Intl.message('Success', name: 'success');
  String get warning => Intl.message('Warning', name: 'warning');
  String get info => Intl.message('Info', name: 'info');
  String get search => Intl.message('Search', name: 'search');
  String get filter => Intl.message('Filter', name: 'filter');
  String get sort => Intl.message('Sort', name: 'sort');
  String get refresh => Intl.message('Refresh', name: 'refresh');
  String get loadMore => Intl.message('Load More', name: 'loadMore');
  String get noDataAvailable =>
      Intl.message('No data available', name: 'noDataAvailable');
  String get somethingWentWrong =>
      Intl.message('Something went wrong', name: 'somethingWentWrong');
  String get pleaseTryAgain =>
      Intl.message('Please try again', name: 'pleaseTryAgain');
  String get networkError =>
      Intl.message('Network connection error', name: 'networkError');
  String get checkInternetConnection => Intl.message(
      'Please check your internet connection',
      name: 'checkInternetConnection');

  // Status
  String get scheduled => Intl.message('Scheduled', name: 'scheduled');
  String get inProgress => Intl.message('In Progress', name: 'inProgress');
  String get cancelled => Intl.message('Cancelled', name: 'cancelled');
  String get active => Intl.message('Active', name: 'active');
  String get expired => Intl.message('Expired', name: 'expired');
  String get inactive => Intl.message('Inactive', name: 'inactive');

  // Time
  String get today => Intl.message('Today', name: 'today');
  String get tomorrow => Intl.message('Tomorrow', name: 'tomorrow');
  String get yesterday => Intl.message('Yesterday', name: 'yesterday');
  String get morning => Intl.message('Morning', name: 'morning');
  String get afternoon => Intl.message('Afternoon', name: 'afternoon');
  String get evening => Intl.message('Evening', name: 'evening');
  String get night => Intl.message('Night', name: 'night');
}

class AppLocalizationDelegate extends LocalizationsDelegate<S> {
  const AppLocalizationDelegate();

  List<Locale> get supportedLocales {
    return const <Locale>[
      Locale.fromSubtags(languageCode: 'en'),
      Locale.fromSubtags(languageCode: 'ar'),
    ];
  }

  @override
  bool isSupported(Locale locale) => _isSupported(locale);
  @override
  Future<S> load(Locale locale) => S.load(locale);
  @override
  bool shouldReload(AppLocalizationDelegate old) => false;

  bool _isSupported(Locale locale) {
    for (var supportedLocale in supportedLocales) {
      if (supportedLocale.languageCode == locale.languageCode) {
        return true;
      }
    }
    return false;
  }
}
