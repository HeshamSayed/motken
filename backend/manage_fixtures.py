#!/usr/bin/env python
"""
Script to create sample data for development and testing.
"""

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from django.contrib.auth import get_user_model
from teachers.models import TeacherProfile, TeacherAvailability
from payments.models import Package, Coupon
from learning.models import Curriculum, Lesson
from decimal import Decimal
from datetime import datetime, timedelta

User = get_user_model()


def create_sample_users():
    """Create sample users."""
    print("Creating sample users...")

    # Create admin
    admin = User.objects.create_superuser(
        email='admin@motken.com',
        password='Admin123!',
        first_name='Admin',
        last_name='User'
    )
    print(f"✓ Created admin: {admin.email}")

    # Create students
    students = []
    for i in range(5):
        student = User.objects.create_user(
            email=f'student{i+1}@test.com',
            password='Student123!',
            first_name=f'Student{i+1}',
            last_name='Test',
            user_type='student',
            country='USA'
        )
        students.append(student)
    print(f"✓ Created {len(students)} students")

    return admin, students


def create_sample_teachers():
    """Create sample teachers."""
    print("Creating sample teachers...")

    teachers = []
    specializations_list = [
        ['tajweed', 'reading'],
        ['memorization', 'recitation'],
        ['tajweed', 'memorization'],
        ['understanding', 'tafseer'],
        ['reading', 'recitation']
    ]

    for i in range(5):
        teacher_user = User.objects.create_user(
            email=f'teacher{i+1}@test.com',
            password='Teacher123!',
            first_name=f'Teacher{i+1}',
            last_name='Quran',
            user_type='teacher',
            country='Egypt' if i % 2 == 0 else 'Saudi Arabia'
        )

        teacher_profile = TeacherProfile.objects.create(
            user=teacher_user,
            bio=f'Experienced Quran teacher with {5 + i*2} years of experience. '
                f'Specializing in {", ".join(specializations_list[i])}. '
                f'Patient and dedicated to helping students learn.',
            years_of_experience=5 + i*2,
            specializations=specializations_list[i],
            education='Bachelor in Islamic Studies',
            certifications=[
                {'name': 'Ijazah in Hafs', 'year': 2015 + i},
                {'name': 'Tajweed Certificate', 'year': 2014 + i}
            ],
            ijazah=True,
            teaching_styles=['patient', 'structured'],
            languages_spoken=['ar', 'en'],
            can_teach_age_groups=['children', 'adults'],
            session_30min_rate=Decimal(str(10 + i * 5)),
            session_45min_rate=Decimal(str(15 + i * 5)),
            session_60min_rate=Decimal(str(20 + i * 5)),
            application_status='approved',
            id_verified=True,
            background_check=True,
            is_available=True,
            average_rating=Decimal(str(4.5 + (i * 0.1))),
            total_ratings=20 + i * 10
        )

        # Add availability (Monday to Friday, 9 AM to 5 PM)
        for day in range(5):
            TeacherAvailability.objects.create(
                teacher=teacher_profile,
                day_of_week=day,
                start_time='09:00:00',
                end_time='17:00:00',
                is_recurring=True,
                is_active=True
            )

        teachers.append(teacher_profile)

    print(f"✓ Created {len(teachers)} teachers with availability")
    return teachers


def create_sample_packages():
    """Create sample packages."""
    print("Creating sample packages...")

    packages_data = [
        {
            'name': 'Trial Package',
            'package_type': 'trial',
            'description': 'Try our service with a discounted trial session',
            'session_count': 1,
            'session_duration': 30,
            'validity_days': 7,
            'price': Decimal('5.00'),
            'discount_percent': 50,
            'features': ['1 Trial Session', '30 minutes', 'No commitment'],
            'is_featured': True
        },
        {
            'name': 'Basic Package',
            'package_type': 'basic',
            'description': 'Perfect for beginners starting their Quran journey',
            'session_count': 4,
            'session_duration': 30,
            'validity_days': 30,
            'price': Decimal('50.00'),
            'discount_percent': 0,
            'features': ['4 Sessions', '30 minutes each', 'Session Recordings', '1 Month Validity'],
            'is_featured': False
        },
        {
            'name': 'Standard Package',
            'package_type': 'standard',
            'description': 'Most popular choice for consistent learning',
            'session_count': 8,
            'session_duration': 45,
            'validity_days': 30,
            'price': Decimal('140.00'),
            'discount_percent': 10,
            'features': ['8 Sessions', '45 minutes each', 'Session Recordings', 'Learning Materials', '1 Month Validity'],
            'is_featured': True
        },
        {
            'name': 'Premium Package',
            'package_type': 'premium',
            'description': 'Best value for serious learners',
            'session_count': 12,
            'session_duration': 60,
            'validity_days': 60,
            'price': Decimal('240.00'),
            'discount_percent': 20,
            'features': ['12 Sessions', '60 minutes each', 'Session Recordings', 'Learning Materials', 'Priority Support', '2 Months Validity'],
            'is_featured': True,
            'priority_support': True
        },
        {
            'name': 'Intensive Package',
            'package_type': 'premium',
            'description': 'Intensive learning program for rapid progress',
            'session_count': 20,
            'session_duration': 60,
            'validity_days': 90,
            'price': Decimal('350.00'),
            'discount_percent': 30,
            'features': ['20 Sessions', '60 minutes each', 'Session Recordings', 'All Learning Materials', 'Priority Support', '3 Months Validity', 'Progress Reports'],
            'is_featured': False,
            'priority_support': True
        }
    ]

    packages = []
    for i, pkg_data in enumerate(packages_data):
        package = Package.objects.create(**pkg_data)
        package.display_order = i
        package.save()
        packages.append(package)

    print(f"✓ Created {len(packages)} packages")
    return packages


def create_sample_coupons():
    """Create sample coupons."""
    print("Creating sample coupons...")

    coupons_data = [
        {
            'code': 'WELCOME10',
            'description': 'Welcome discount for new users',
            'discount_type': 'percentage',
            'discount_value': Decimal('10.00'),
            'valid_from': datetime.now(),
            'valid_until': datetime.now() + timedelta(days=365),
            'for_new_users_only': True,
            'is_active': True
        },
        {
            'code': 'SUMMER25',
            'description': 'Summer special discount',
            'discount_type': 'percentage',
            'discount_value': Decimal('25.00'),
            'max_discount_amount': Decimal('50.00'),
            'valid_from': datetime.now(),
            'valid_until': datetime.now() + timedelta(days=90),
            'is_active': True
        },
        {
            'code': 'RAMADAN50',
            'description': 'Ramadan special offer',
            'discount_type': 'fixed',
            'discount_value': Decimal('50.00'),
            'min_purchase_amount': Decimal('100.00'),
            'valid_from': datetime.now(),
            'valid_until': datetime.now() + timedelta(days=30),
            'is_active': True
        }
    ]

    coupons = []
    for coupon_data in coupons_data:
        coupon = Coupon.objects.create(**coupon_data)
        coupons.append(coupon)

    print(f"✓ Created {len(coupons)} coupons")
    return coupons


def create_sample_curricula():
    """Create sample curricula."""
    print("Creating sample curricula...")

    curricula_data = [
        {
            'name': 'Quran Reading Basics',
            'slug': 'quran-reading-basics',
            'curriculum_type': 'reading',
            'difficulty': 'beginner',
            'description': 'Learn to read Quran from scratch with proper pronunciation',
            'objectives': 'By the end of this course, you will be able to read any Arabic text from the Quran with confidence.',
            'estimated_duration_weeks': 12,
            'total_lessons': 24,
            'is_published': True,
            'is_featured': True
        },
        {
            'name': 'Tajweed Mastery',
            'slug': 'tajweed-mastery',
            'curriculum_type': 'tajweed',
            'difficulty': 'intermediate',
            'description': 'Master the rules of Tajweed for beautiful Quran recitation',
            'objectives': 'Learn all Tajweed rules and apply them correctly in your recitation.',
            'estimated_duration_weeks': 16,
            'total_lessons': 32,
            'is_published': True,
            'is_featured': True
        },
        {
            'name': 'Quran Memorization Program',
            'slug': 'quran-memorization',
            'curriculum_type': 'memorization',
            'difficulty': 'intermediate',
            'description': 'Systematic approach to memorizing the Holy Quran',
            'objectives': 'Develop effective memorization techniques and build consistency.',
            'estimated_duration_weeks': 52,
            'total_lessons': 104,
            'is_published': True,
            'is_featured': False
        }
    ]

    curricula = []
    for curr_data in curricula_data:
        curriculum = Curriculum.objects.create(**curr_data)
        curricula.append(curriculum)

    print(f"✓ Created {len(curricula)} curricula")
    return curricula


def main():
    """Main function to create all sample data."""
    print("\n" + "="*50)
    print("Creating Sample Data for Motken")
    print("="*50 + "\n")

    # Clear existing data (optional - be careful in production!)
    print("Clearing existing data...")
    User.objects.filter(email__contains='@test.com').delete()
    print("✓ Cleared test data\n")

    # Create data
    admin, students = create_sample_users()
    teachers = create_sample_teachers()
    packages = create_sample_packages()
    coupons = create_sample_coupons()
    curricula = create_sample_curricula()

    print("\n" + "="*50)
    print("Sample Data Creation Complete!")
    print("="*50)
    print(f"\nCredentials:")
    print(f"Admin: admin@motken.com / Admin123!")
    print(f"Students: student1@test.com to student5@test.com / Student123!")
    print(f"Teachers: teacher1@test.com to teacher5@test.com / Teacher123!")
    print(f"\nYou can now access:")
    print(f"- Admin Panel: http://localhost:8000/admin")
    print(f"- API: http://localhost:8000/api/v1/")
    print(f"- API Docs: http://localhost:8000/api/docs/\n")


if __name__ == '__main__':
    main()
