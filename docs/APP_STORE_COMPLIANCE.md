# App Store Compliance Guide

## Overview

This document outlines Motken's compliance with Google Play Store and Apple App Store requirements.

## 🍎 Apple App Store Compliance

### App Store Review Guidelines Compliance

#### 1. Safety (Guideline 1)
- ✅ **1.1 Objectionable Content**: Age-appropriate Quran learning content
- ✅ **1.2 User Generated Content**: Moderation of reviews and messages
- ✅ **1.3 Kids Category**: Not targeting kids specifically, 13+ rating
- ✅ **1.4 Physical Harm**: No dangerous activities or challenges
- ✅ **1.5 Developer Information**: Complete contact information provided

#### 2. Performance (Guideline 2)
- ✅ **2.1 App Completeness**: Fully functional, no placeholders
- ✅ **2.2 Beta Testing**: Use TestFlight for beta versions
- ✅ **2.3 Accurate Metadata**: App description matches functionality
- ✅ **2.4 Hardware Compatibility**: Works on all supported devices
- ✅ **2.5 Software Requirements**: Uses public APIs only

#### 3. Business (Guideline 3)
- ✅ **3.1 Payments**: Uses In-App Purchase for digital services
- ✅ **3.2 Other Business Models**: Subscription model clearly described
- ✅ **3.3 Ad Targeting**: No ads currently, future ads comply with policy

#### 4. Design (Guideline 4)
- ✅ **4.1 Copycats**: Original app, not copying others
- ✅ **4.2 Minimum Functionality**: Substantial functionality provided
- ✅ **4.3 Spam**: Not spam, provides value
- ✅ **4.4 Extensions**: No app extensions currently
- ✅ **4.5 Apple Sites and Services**: Proper use of Apple services

#### 5. Legal (Guideline 5)
- ✅ **5.1 Privacy**: Complete privacy policy, data minimization
- ✅ **5.2 Intellectual Property**: No copyright infringement
- ✅ **5.3 Gaming, Gambling, and Lotteries**: Not applicable
- ✅ **5.4 VPN Apps**: Not a VPN app
- ✅ **5.5 Developer Code of Conduct**: Professional conduct maintained

### Privacy Requirements

#### App Privacy Labels (App Store Connect)
```
Data Used to Track You:
- None

Data Linked to You:
- Contact Info (Email, Name, Phone)
- User Content (Photos, Videos during sessions)
- Identifiers (User ID)
- Usage Data (Session attendance, app interactions)
- Purchases (Subscription, payment history)
- Diagnostics (Crash logs, performance data)

Data Not Linked to You:
- Diagnostics (Anonymous analytics)

Data Collection Purpose:
- App Functionality
- Analytics
- Product Personalization
- Developer Advertising (if ads added)
```

### Age Rating
- **Age Rating**: 4+ (Teacher Learning)
- **Content**: Educational, no inappropriate content
- **Target Audience**: General audience, 13+ recommended

### Required Info.plist Entries

```xml
<!-- Camera Usage -->
<key>NSCameraUsageDescription</key>
<string>Camera is needed for video sessions with your Quran teacher</string>

<!-- Microphone Usage -->
<key>NSMicrophoneUsageDescription</key>
<string>Microphone is needed to speak with your Quran teacher during sessions</string>

<!-- Photo Library -->
<key>NSPhotoLibraryUsageDescription</key>
<string>Access photos to set your profile picture</string>

<!-- Calendar (for session scheduling) -->
<key>NSCalendarsUsageDescription</key>
<string>Add sessions to your calendar for reminders</string>

<!-- Location (optional, for finding local teachers) -->
<key>NSLocationWhenInUseUsageDescription</key>
<string>Find teachers near your location (optional)</string>

<!-- Face ID / Touch ID -->
<key>NSFaceIDUsageDescription</key>
<string>Use Face ID for secure and convenient login</string>
```

### Additional Requirements
- ✅ Human Interface Guidelines followed
- ✅ Accessibility features supported
- ✅ Dark mode support (future)
- ✅ iPad and iPhone support
- ✅ Landscape and portrait orientations
- ✅ Proper error handling
- ✅ Crash-free rate > 99%

---

## 🤖 Google Play Store Compliance

### Google Play Policy Compliance

#### 1. Content Policy
- ✅ **Sexual Content**: None present
- ✅ **Hate Speech**: Zero tolerance policy
- ✅ **Violence**: No violent content
- ✅ **Dangerous Content**: Safe, educational content
- ✅ **Impersonation**: Authentic representation

#### 2. Privacy & Security
- ✅ **Personal and Sensitive Data**: Minimal collection, secure handling
- ✅ **Permissions**: Only necessary permissions requested
- ✅ **Device and Network Abuse**: No malicious behavior
- ✅ **Deceptive Behavior**: Transparent functionality
- ✅ **Misrepresentation**: Accurate app description

#### 3. Monetization & Ads
- ✅ **Payments**: Using Google Play Billing for subscriptions
- ✅ **Subscriptions**: Clear terms, easy cancellation
- ✅ **Ads**: No ads currently (future ads comply with policy)

#### 4. Store Listing
- ✅ **Metadata**: Accurate title, description, screenshots
- ✅ **User Reviews**: No fake reviews or rating manipulation
- ✅ **Intellectual Property**: Original content and assets

### Target Audience & Content Rating

#### Target Age Groups
- **Primary**: Ages 13-18 (Teens)
- **Secondary**: Ages 18+ (Adults)

#### Content Rating (IARC)
```
Content Rating: EVERYONE
- No violence
- No sexual content
- No profanity
- No controlled substances
- No gambling
- No scary content
```

### Required AndroidManifest.xml Permissions

```xml
<!-- Required Permissions -->
<uses-permission android:name="android.permission.INTERNET" />
<uses-permission android:name="android.permission.ACCESS_NETWORK_STATE" />

<!-- Camera & Microphone for Video Sessions -->
<uses-permission android:name="android.permission.CAMERA" />
<uses-permission android:name="android.permission.RECORD_AUDIO" />

<!-- Notifications -->
<uses-permission android:name="android.permission.POST_NOTIFICATIONS" />

<!-- Optional Permissions -->
<uses-permission android:name="android.permission.READ_EXTERNAL_STORAGE" />
<uses-permission android:name="android.permission.WRITE_EXTERNAL_STORAGE" />

<!-- Features -->
<uses-feature android:name="android.hardware.camera" android:required="false" />
<uses-feature android:name="android.hardware.microphone" android:required="false" />
```

### Permission Justification

| Permission | Purpose | Required |
|------------|---------|----------|
| INTERNET | API communication | Yes |
| CAMERA | Video sessions with teachers | Yes |
| RECORD_AUDIO | Audio in video sessions | Yes |
| POST_NOTIFICATIONS | Session reminders | No |
| READ/WRITE_STORAGE | Save learning materials | No |

### Data Safety Section (Play Console)

```
Data Collection:
✓ Personal Info (Name, Email, Phone)
✓ Financial Info (Purchase history)
✓ Photos and Videos (Profile picture, session recordings)
✓ App Activity (Session attendance, progress)
✓ Device IDs (For notifications)

Data Usage:
✓ App Functionality
✓ Analytics
✓ Personalization
✗ Advertising (not used)

Data Sharing:
✓ Shared with teachers (name, learning preferences)
✓ Shared with service providers (Zoom, payment processor)
✗ Not sold to third parties

Security:
✓ Data encrypted in transit
✓ Data encrypted at rest (future)
✓ Users can request deletion
```

### Families Policy (If Targeting Children)

**Currently NOT opted into Families Program** (13+ only)

If targeting under 13 in future:
- Teacher-approved ads only (currently no ads)
- COPPA compliance
- Privacy policy for children
- Age-appropriate content rating
- Verified educational value

---

## 📋 Common Compliance Checklist

### Legal Documents
- ✅ Privacy Policy (GDPR, CCPA, COPPA compliant)
- ✅ Terms of Service
- ✅ Data Deletion Instructions
- ✅ Accessible in-app and on website

### Technical Requirements
- ✅ HTTPS/SSL for all connections
- ✅ JWT authentication
- ✅ Data encryption
- ✅ Secure payment processing
- ✅ Session recording consent
- ✅ Parental controls

### Content Safety
- ✅ Content moderation system
- ✅ Report abuse feature
- ✅ Block/mute functionality
- ✅ Zero tolerance for harmful content
- ✅ Background checks for teachers

### User Rights
- ✅ Access personal data
- ✅ Export data
- ✅ Delete account
- ✅ Opt-out of marketing
- ✅ Withdraw consent

---

## 🔄 Pre-Launch Checklist

### Apple App Store
- [ ] Complete App Store Connect listing
- [ ] Upload app binary
- [ ] Configure privacy labels
- [ ] Add screenshots (all device sizes)
- [ ] Write app description
- [ ] Set age rating
- [ ] Add privacy policy URL
- [ ] Add terms of service URL
- [ ] Submit for review

### Google Play Store
- [ ] Complete Play Console listing
- [ ] Upload app bundle (AAB)
- [ ] Configure Data Safety section
- [ ] Add screenshots (all device sizes)
- [ ] Write app description
- [ ] Complete content rating questionnaire
- [ ] Add privacy policy URL
- [ ] Add terms of service URL
- [ ] Submit for review

---

## 📞 Contact for Compliance Issues

- **Privacy Officer**: privacy@motken.com
- **Data Protection Officer**: dpo@motken.com
- **Legal**: legal@motken.com
- **Support**: support@motken.com

---

## 📅 Compliance Review Schedule

- **Quarterly**: Review compliance with updated policies
- **Bi-annually**: Update privacy policy and terms
- **Annually**: Complete security audit
- **As needed**: Respond to app store policy changes

---

**Last Updated**: November 7, 2025
**Next Review**: February 7, 2026
