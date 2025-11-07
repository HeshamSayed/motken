# Motken Bilingual Implementation Guide (Arabic/English)

## 🎯 Overview

This guide documents the complete bilingual (Arabic/English) implementation for the Motken Quran Learning App, including RTL (Right-to-Left) support for Arabic.

---

## ✅ What Has Been Implemented

### 1. **Localization Infrastructure** ✅

#### Created Files:
- `/mobile/lib/l10n/app_en.arb` - English translations (160+ strings)
- `/mobile/lib/l10n/app_ar.arb` - Arabic translations (160+ strings)
- `/mobile/lib/generated/l10n.dart` - Main localization class
- `/mobile/lib/generated/intl/messages_all.dart` - Message loader
- `/mobile/lib/generated/intl/messages_en.dart` - English messages
- `/mobile/lib/generated/intl/messages_ar.dart` - Arabic messages

#### Translation Coverage:
- ✅ App branding (Motken, taglines)
- ✅ Authentication (login, register, passwords)
- ✅ Navigation (home, teachers, sessions, profile)
- ✅ Teachers (specializations, filters, bookings)
- ✅ Sessions (upcoming, completed, cancelled)
- ✅ Payments (packages, transactions, coupons)
- ✅ Profile & Settings
- ✅ Form validation messages
- ✅ Common actions (save, edit, delete, etc.)
- ✅ Status messages
- ✅ Time & date labels

---

### 2. **Language State Management** ✅

#### Created Files:
- `/mobile/lib/core/language/bloc/language_bloc.dart`
- `/mobile/lib/core/language/bloc/language_event.dart`
- `/mobile/lib/core/language/bloc/language_state.dart`

#### Features:
- ✅ Language state management with BLoC pattern
- ✅ Persists language selection to SharedPreferences
- ✅ Loads saved language on app start
- ✅ Supports language switching between English and Arabic
- ✅ Automatic RTL detection for Arabic

---

### 3. **Main App Configuration** ✅

#### Updated: `/mobile/lib/main.dart`

**Changes:**
- ✅ Added SharedPreferences initialization
- ✅ Integrated LanguageBloc with MultiBlocProvider
- ✅ Added S.delegate to localizationsDelegates
- ✅ Made MaterialApp reactive to language changes with BlocBuilder
- ✅ Configured locale resolution callback
- ✅ Updated HomePage with localized strings
- ✅ Updated MainNavigationPage with localized bottom nav labels
- ✅ Supports RTL layout automatically for Arabic

**Key Code:**
```dart
BlocBuilder<LanguageBloc, LanguageState>(
  builder: (context, languageState) {
    return MaterialApp(
      locale: languageState.locale,
      localizationsDelegates: const [
        S.delegate,  // Our custom delegate
        GlobalMaterialLocalizations.delegate,
        GlobalWidgetsLocalizations.delegate,
        GlobalCupertinoLocalizations.delegate,
      ],
      supportedLocales: S.delegate.supportedLocales,
      // ... rest of app config
    );
  },
)
```

---

### 4. **Updated Pages** ✅

#### Completed Pages:

**1. Login Page** ✅
- File: `/mobile/lib/features/auth/presentation/pages/login_page.dart`
- All text strings localized
- Validation messages in both languages
- Pattern to follow:
```dart
final s = S.of(context);
TextFormField(
  decoration: InputDecoration(labelText: s.email),
  validator: (value) {
    if (value == null || value.isEmpty) {
      return s.pleaseEnterEmail;
    }
    return null;
  },
)
```

**2. Settings Page** ✅
- File: `/mobile/lib/features/settings/presentation/pages/settings_page.dart`
- **Fully functional language switching**
- All labels localized
- Language dialog shows English/Arabic options
- Connected to LanguageBloc for actual language switching
- Pattern to follow:
```dart
BlocBuilder<LanguageBloc, LanguageState>(
  builder: (context, languageState) {
    final currentLanguage = languageState.locale.languageCode == 'en'
        ? s.english
        : s.arabic;

    return ListTile(
      title: Text(s.language),
      subtitle: Text(currentLanguage),
      onTap: () => _showLanguageDialog(),
    );
  },
)
```

**3. Home Page & Navigation** ✅
- Files: `/mobile/lib/main.dart` (HomePage, MainNavigationPage)
- Bottom navigation localized
- Quick actions localized
- App bar titles localized

---

### 5. **Backend API** ✅

#### Updated: `/backend/users/views.py`

**Added Endpoints:**

1. **Update Language Preference**
   - Endpoint: `POST /api/v1/users/update_language/`
   - Body: `{"language": "en"}` or `{"language": "ar"}`
   - Response:
   ```json
   {
     "message": "Language updated successfully",
     "language": "ar"
   }
   ```

2. **Get Language Preference**
   - Endpoint: `GET /api/v1/users/get_language/`
   - Response:
   ```json
   {
     "language": "ar"
   }
   ```

**Code:**
```python
@action(detail=False, methods=['post', 'patch'])
def update_language(self, request):
    """Update user's preferred language."""
    language = request.data.get('language')

    # Validate language is supported
    supported_languages = ['en', 'ar']
    if language not in supported_languages:
        return Response({
            'error': f'Language must be one of: {", ".join(supported_languages)}'
        }, status=status.HTTP_400_BAD_REQUEST)

    # Update user's preferred language
    request.user.preferred_language = language
    request.user.save()

    return Response({
        'message': 'Language updated successfully',
        'language': language
    }, status=status.HTTP_200_OK)
```

**Note:** The User model already has a `preferred_language` field configured with choices `[('en', 'English'), ('ar', 'Arabic')]`.

---

## 📋 Remaining Work

### Pages That Need Localization:

The following pages still contain hardcoded English strings and need to be updated following the pattern shown above:

#### **Authentication Pages:**
1. `/mobile/lib/features/auth/presentation/pages/register_page.dart` - Registration form
2. `/mobile/lib/features/auth/presentation/pages/change_password_page.dart` - Password change

#### **Teacher Pages:**
3. `/mobile/lib/features/teachers/presentation/pages/teachers_list_page.dart` - Teachers list & filters
4. `/mobile/lib/features/teachers/presentation/pages/teacher_details_page.dart` - Teacher profile

#### **Session Pages:**
5. `/mobile/lib/features/sessions/presentation/pages/my_sessions_page.dart` - Sessions list
6. `/mobile/lib/features/sessions/presentation/pages/book_session_page.dart` - Book session form
7. `/mobile/lib/features/sessions/presentation/pages/session_details_page.dart` - Session details

#### **Payment Pages:**
8. `/mobile/lib/features/payments/presentation/pages/packages_page.dart` - Packages list
9. `/mobile/lib/features/payments/presentation/pages/package_details_page.dart` - Package details with coupon
10. `/mobile/lib/features/payments/presentation/pages/subscription_page.dart` - Subscription status
11. `/mobile/lib/features/payments/presentation/pages/transactions_page.dart` - Transaction history

#### **Profile Pages:**
12. `/mobile/lib/features/profile/presentation/pages/profile_page.dart` - User profile
13. `/mobile/lib/features/profile/presentation/pages/edit_profile_page.dart` - Edit profile form

---

## 🔧 How to Update Remaining Pages

### Step-by-Step Pattern:

#### **Step 1: Import the Localization Class**

At the top of the file, add:
```dart
import '../../../../generated/l10n.dart';
```

(Adjust the path based on your file location. Use `../` to go up directories.)

#### **Step 2: Get the Localization Instance**

In the `build()` method, add at the beginning:
```dart
@override
Widget build(BuildContext context) {
  final s = S.of(context);  // Get localization instance

  // ... rest of the build method
}
```

#### **Step 3: Replace Hardcoded Strings**

Replace all hardcoded strings with localization calls:

**Before:**
```dart
Text('Welcome to Motken')
```

**After:**
```dart
Text(s.welcomeTitle)
```

**Before:**
```dart
const InputDecoration(
  labelText: 'Email',
  hintText: 'Enter your email',
)
```

**After:**
```dart
InputDecoration(
  labelText: s.email,
  hintText: s.pleaseEnterEmail,
)
```

**Before:**
```dart
ElevatedButton(
  child: const Text('Login'),
)
```

**After:**
```dart
ElevatedButton(
  child: Text(s.login),
)
```

#### **Step 4: Update Validation Messages**

**Before:**
```dart
validator: (value) {
  if (value == null || value.isEmpty) {
    return 'Please enter your email';
  }
  if (!value.contains('@')) {
    return 'Please enter a valid email';
  }
  return null;
}
```

**After:**
```dart
validator: (value) {
  if (value == null || value.isEmpty) {
    return s.pleaseEnterEmail;
  }
  if (!value.contains('@')) {
    return s.pleaseEnterValidEmail;
  }
  return null;
}
```

#### **Step 5: Handle String Concatenation**

**Before:**
```dart
Text("Don't have an account? Register")
```

**After:**
```dart
Row(
  children: [
    Text(s.dontHaveAccount + ' '),
    TextButton(
      onPressed: () => Navigator.pushNamed(context, '/register'),
      child: Text(s.register),
    ),
  ],
)
```

#### **Step 6: Handle Dynamic Strings with Parameters**

For strings with parameters, use the methods in the S class:

**Before:**
```dart
Text('$sessionCount Sessions')
```

**After:**
```dart
Text(s.sessionsCount(sessionCount))
```

**Before:**
```dart
Text('${duration} min - \$${price}')
```

**After:**
```dart
Text(s.sessionPrice(duration, price))
```

---

## 📖 Available Localization Keys

All available keys are defined in `/mobile/lib/l10n/app_en.arb` and `/mobile/lib/l10n/app_ar.arb`.

### Quick Reference:

#### **Common:**
- `s.appName` - "Motken" / "متقن"
- `s.appTagline` - "Learn Quran Online" / "تعلم القرآن عبر الإنترنت"
- `s.save`, `s.edit`, `s.delete`, `s.cancel`, `s.ok`, `s.yes`, `s.no`
- `s.loading`, `s.error`, `s.success`, `s.retry`

#### **Authentication:**
- `s.login`, `s.register`, `s.email`, `s.password`
- `s.firstName`, `s.lastName`, `s.phone`
- `s.student`, `s.teacher`
- `s.forgotPassword`, `s.changePassword`

#### **Validation:**
- `s.pleaseEnterEmail`, `s.pleaseEnterValidEmail`
- `s.pleaseEnterPassword`, `s.passwordTooShort`
- `s.passwordsDoNotMatch`
- `s.pleaseEnterFirstName`, `s.pleaseEnterLastName`

#### **Navigation:**
- `s.home`, `s.teachers`, `s.sessions`, `s.profile`
- `s.settings`, `s.notifications`

#### **Teachers:**
- `s.findTeachers`, `s.allTeachers`, `s.noTeachersFound`
- `s.tajweed`, `s.memorization`, `s.reading`
- `s.specialization`, `s.teachingStyle`, `s.availability`
- `s.bookNow`, `s.viewProfile`, `s.perSession`

#### **Sessions:**
- `s.mySessions`, `s.upcomingSessions`, `s.completedSessions`
- `s.joinSession`, `s.cancelSession`, `s.rescheduleSession`
- `s.duration`, `s.minutes`, `s.price`, `s.status`
- `s.selectDate`, `s.selectTime`, `s.selectDuration`

#### **Payments:**
- `s.packages`, `s.choosePackage`, `s.popular`
- `s.transactions`, `s.transactionHistory`
- `s.couponCode`, `s.applyCoupon`, `s.discount`
- `s.totalPrice`, `s.proceedToPayment`
- `s.pending`, `s.completed`, `s.failed`

#### **Profile:**
- `s.myProfile`, `s.editProfile`, `s.saveChanges`
- `s.myProgress`, `s.logout`
- `s.helpSupport`, `s.privacyPolicy`, `s.termsOfService`

#### **Settings:**
- `s.settings`, `s.appearance`, `s.darkMode`
- `s.language`, `s.english`, `s.arabic`
- `s.sessionReminders`, `s.paymentNotifications`

### Methods with Parameters:

```dart
s.yearsExperience(int years)           // "5 years experience" / "5 سنوات خبرة"
s.sessionsCount(int count)             // "10 Sessions" / "10 جلسة"
s.validityDays(int days)               // "30 days" / "30 يوم"
s.sessionPrice(int duration, String price)  // "60 min - $50" / "60 دقيقة - $50"
s.bookingFor(String teacherName)       // "Booking for Ahmad" / "حجز جلسة مع أحمد"
```

---

## 🔄 How Language Switching Works

### User Flow:

1. **User opens Settings**
2. **User taps on "Language"**
3. **Dialog shows with English/Arabic options**
4. **User selects a language**
5. **LanguageBloc receives ChangeLanguageEvent**
6. **Language is saved to SharedPreferences**
7. **App rebuilds with new locale**
8. **All pages automatically show in the selected language**
9. **Optional: Backend API is called to sync preference (can be added to LanguageBloc)**

### Implementation in Settings Page:

```dart
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
```

---

## 🌐 RTL (Right-to-Left) Support

### Automatic RTL:

The app automatically detects when Arabic is selected and applies RTL layout. This is handled by Flutter's built-in directionality system.

**No additional code needed!** Flutter automatically:
- ✅ Reverses layout direction
- ✅ Flips icons and navigation
- ✅ Aligns text to the right
- ✅ Mirrors animations

### Testing RTL:

1. Run the app
2. Go to Settings
3. Change language to العربية (Arabic)
4. Observe:
   - Text aligns to the right
   - Navigation drawer opens from right
   - Back buttons flip to right side
   - List items mirror

---

## 🧪 Testing Checklist

### Test Cases:

- [ ] **App launches in English by default**
- [ ] **Change language to Arabic in Settings**
- [ ] **App rebuilds and shows Arabic text**
- [ ] **RTL layout is applied correctly**
- [ ] **Form validation messages show in Arabic**
- [ ] **Navigate between pages - all text is Arabic**
- [ ] **Change back to English**
- [ ] **App rebuilds and shows English text**
- [ ] **LTR layout is restored**
- [ ] **Close app and reopen - language preference is remembered**
- [ ] **Login/Register with Arabic selected**
- [ ] **All error messages show in correct language**

---

## 🚀 Integration with Backend (Optional Enhancement)

To sync language preference with the backend, update the LanguageBloc:

### Add to `language_bloc.dart`:

```dart
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

    // ✨ NEW: Sync with backend
    await _syncLanguageWithBackend(languageCode);

    debugPrint('Language changed to: $languageCode (RTL: $isRTL)');
  } catch (e) {
    debugPrint('Error changing language: $e');
  }
}

Future<void> _syncLanguageWithBackend(String languageCode) async {
  try {
    // Assuming you have an API client
    final dio = Dio();
    final token = sharedPreferences.getString('access_token');

    if (token != null) {
      await dio.post(
        '${AppConfig.apiBaseUrl}/users/update_language/',
        data: {'language': languageCode},
        options: Options(headers: {'Authorization': 'Bearer $token'}),
      );
      debugPrint('Language synced with backend');
    }
  } catch (e) {
    debugPrint('Failed to sync language with backend: $e');
    // Don't fail the language change if backend sync fails
  }
}
```

---

## 📝 Adding New Translations

If you need to add new strings:

### Step 1: Add to ARB Files

**English** (`/mobile/lib/l10n/app_en.arb`):
```json
{
  "newKey": "New Text in English"
}
```

**Arabic** (`/mobile/lib/l10n/app_ar.arb`):
```json
{
  "newKey": "نص جديد بالعربية"
}
```

### Step 2: Add to Generated Class

In `/mobile/lib/generated/l10n.dart`:
```dart
String get newKey => Intl.message('New Text in English', name: 'newKey');
```

### Step 3: Add to Message Files

**English** (`/mobile/lib/generated/intl/messages_en.dart`):
```dart
"newKey": MessageLookupByLibrary.simpleMessage("New Text in English"),
```

**Arabic** (`/mobile/lib/generated/intl/messages_ar.dart`):
```dart
"newKey": MessageLookupByLibrary.simpleMessage("نص جديد بالعربية"),
```

### Step 4: Use in Code

```dart
Text(s.newKey)
```

---

## 🎨 Font Support

The app already has Arabic font support configured:

**From `pubspec.yaml`:**
```yaml
fonts:
  - family: Poppins
    fonts:
      - asset: assets/fonts/Poppins-Regular.ttf
      - asset: assets/fonts/Poppins-Bold.ttf
        weight: 700

  - family: Cairo      # ✅ Arabic font
    fonts:
      - asset: assets/fonts/Cairo-Regular.ttf
      - asset: assets/fonts/Cairo-Bold.ttf
        weight: 700
```

The theme automatically uses the Cairo font for Arabic text.

---

## ⚠️ Common Pitfalls

### 1. **Forgetting to remove `const`**

**Wrong:**
```dart
const Text('Hello')  // Can't be const when using localization
```

**Correct:**
```dart
Text(s.hello)  // Remove const
```

### 2. **Incorrect Path for Import**

Count the directory levels carefully:
```dart
// If in: /mobile/lib/features/auth/presentation/pages/login_page.dart
// Then:   /mobile/lib/generated/l10n.dart
import '../../../../generated/l10n.dart';  // Go up 4 levels
```

### 3. **Not Handling RTL in Custom Widgets**

Flutter handles most RTL automatically, but if you have custom positioned widgets, use:
```dart
Directionality.of(context).textDirection == TextDirection.rtl
```

### 4. **Hardcoded Text in Subtitles**

Remember to localize subtitles and helper text too:
```dart
ListTile(
  title: Text(s.darkMode),
  subtitle: Text(s.useDarkTheme),  // Don't forget subtitles!
)
```

---

## 📊 Implementation Progress

| Feature | Status |
|---------|--------|
| Localization Infrastructure | ✅ Complete |
| Language State Management (BLoC) | ✅ Complete |
| Main App Configuration | ✅ Complete |
| Login Page | ✅ Complete |
| Settings Page (with language switching) | ✅ Complete |
| Home & Navigation | ✅ Complete |
| Backend API Endpoints | ✅ Complete |
| Register Page | ⏳ Pending |
| Change Password Page | ⏳ Pending |
| Teachers Pages (2 pages) | ⏳ Pending |
| Session Pages (3 pages) | ⏳ Pending |
| Payment Pages (4 pages) | ⏳ Pending |
| Profile Pages (2 pages) | ⏳ Pending |

**Progress: 6/19 pages completed (32%)**

---

## 🎯 Next Steps

1. **Update Remaining Pages (13 pages)**
   - Follow the pattern documented above
   - Start with authentication pages (register, change_password)
   - Then do teacher, session, payment, and profile pages
   - Test each page after updating

2. **Test Language Switching**
   - Test on each updated page
   - Verify RTL layout for Arabic
   - Check form validations in both languages
   - Test navigation in both languages

3. **Backend Integration (Optional)**
   - Add backend sync to LanguageBloc
   - Load user's preferred language on login
   - Handle offline language changes

4. **Deploy**
   - Test on real devices (iOS & Android)
   - Verify Arabic font rendering
   - Test RTL animations and transitions
   - Submit to app stores

---

## 📚 Resources

- **Flutter Internationalization**: https://docs.flutter.dev/development/accessibility-and-localization/internationalization
- **ARB File Format**: https://github.com/google/app-resource-bundle
- **RTL Support**: https://docs.flutter.dev/development/accessibility-and-localization/internationalization#setting-up-an-internationalized-app
- **BLoC Pattern**: https://bloclibrary.dev/

---

## 💡 Tips

1. **Use VS Code Extensions:**
   - "Flutter Intl" extension for easier ARB management
   - "Error Lens" to see localization errors inline

2. **Test Frequently:**
   - Switch languages after updating each page
   - Don't wait until the end to test

3. **Consistent Naming:**
   - Use camelCase for keys: `pleaseEnterEmail`
   - Group related keys: `session*`, `payment*`

4. **Keep ARB Files in Sync:**
   - Every key in `app_en.arb` must exist in `app_ar.arb`
   - Use same key names in both files

---

## ✅ Definition of Done

A page is considered "fully localized" when:

- [ ] All visible text uses `s.` localization
- [ ] All validation messages are localized
- [ ] All dialog titles and content are localized
- [ ] All button labels are localized
- [ ] All placeholders and hints are localized
- [ ] Page displays correctly in English
- [ ] Page displays correctly in Arabic
- [ ] RTL layout works properly for Arabic
- [ ] No hardcoded English strings remain
- [ ] Page has been tested with language switching

---

## 🤝 Need Help?

If you encounter issues:

1. Check that the key exists in both ARB files
2. Verify the import path is correct
3. Make sure you removed `const` from Text widgets
4. Test with a simple string first (like `s.appName`)
5. Check the console for localization errors

---

**Last Updated:** 2025-11-07
**Version:** 1.0
**Completion:** 32% (6/19 pages)

---

Good luck with the implementation! 🚀
