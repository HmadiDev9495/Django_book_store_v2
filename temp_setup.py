#!/usr/bin/env python
"""
🚀 اسکریپت موقت: پاک کردن کامل دیتابیس + ساخت از نو + سوپریوزر
محل: کنار manage.py
اجرا: python temp_setup.py
بعدش پاکش کن!
"""

import os
import sys
import django

# تنظیمات جنگو
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'book_store.settings')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
django.setup()

from django.contrib.auth import get_user_model
from book.models import Book, ImageBook

User = get_user_model()

# ==================== داده‌ها ====================

SUPERUSER_DATA = {
    'username': 'admin',
    'email': 'admin@test.com',
    'password': 'admin12345',
    'phone_number': '09999999999',
    'national_code': '9999999999',
}

USERS_DATA = [
    {
        'username': 'writer1',
        'email': 'writer1@test.com',
        'password': 'test12345',
        'phone_number': '09123456789',
        'national_code': '1234567890',
        'is_author': True,
    },
    {
        'username': 'writer2',
        'email': 'writer2@test.com',
        'password': 'test12345',
        'phone_number': '09123456788',
        'national_code': '1234567891',
        'is_author': True,
    },
    {
        'username': 'reader1',
        'email': 'reader1@test.com',
        'password': 'test12345',
        'phone_number': '09123456787',
        'national_code': '1234567892',
        'is_author': False,
    }
]

BOOKS_DATA = [
    {
        "name": "تاریخ ایران باستان",
        "author": "پرویز رجبی",
        "published_date": "2010-01-01",
        "price": 150000,
        "currency": "TOMAN",
        "category": "HC",
        "page_count": 520,
        "description": "بررسی جامع تاریخ ایران از دوران باستان تا ساسانیان.",
        "is_published": True,
        "publisher_idx": 0
    },
    {
        "name": "فیزیک کوانتوم برای تازه‌کارها",
        "author": "استیون هاوکینگ",
        "published_date": "2015-06-15",
        "price": 85000,
        "currency": "TOMAN",
        "category": "SC",
        "page_count": 320,
        "description": "مقدمه‌ای بر مکانیک کوانتوم و نظریه نسبیت.",
        "is_published": True,
        "publisher_idx": 1
    },
    {
        "name": "عشق در زمان جنگ",
        "author": "نسیم مرعشی",
        "published_date": "2018-03-20",
        "price": 65000,
        "currency": "TOMAN",
        "category": "RM",
        "page_count": 280,
        "description": "داستان عاشقانه‌ای در دوران جنگ تحمیلی.",
        "is_published": False,
        "publisher_idx": 0
    },
    {
        "name": "معماری ایرانی",
        "author": "محمد کریم پیرنیا",
        "published_date": "2005-11-10",
        "price": 200000,
        "currency": "TOMAN",
        "category": "HC",
        "page_count": 450,
        "description": "بررسی سبک‌های معماری سنتی ایران.",
        "is_published": True,
        "publisher_idx": 1
    },
    {
        "name": "رازهای ذهن ناخودآگاه",
        "author": "جو دیسپنزا",
        "published_date": "2020-09-01",
        "price": 95000,
        "currency": "TOMAN",
        "category": "SC",
        "page_count": 380,
        "description": "چگونه ذهن خود را دوباره سیم‌کشی کنیم.",
        "is_published": True,
        "publisher_idx": 0
    },
    {
        "name": "شب‌های تهران",
        "author": "صادق هدایت",
        "published_date": "1937-01-01",
        "price": 45000,
        "currency": "TOMAN",
        "category": "TH",
        "page_count": 180,
        "description": "داستان‌های کوتاه و مرموز از تهران قدیم.",
        "is_published": True,
        "publisher_idx": 1
    },
    {
        "name": "کمدی انسانی",
        "author": "ویلیام شکسپیر",
        "published_date": "1599-01-01",
        "price": 120000,
        "currency": "TOMAN",
        "category": "FN",
        "page_count": 240,
        "description": "نمایشنامه کمدی کلاسیک شکسپیر.",
        "is_published": False,
        "publisher_idx": 0
    },
    {
        "name": "تاریخ علم در ایران",
        "author": "غلامحسین مصاحب",
        "published_date": "1975-04-12",
        "price": 175000,
        "currency": "TOMAN",
        "category": "HC",
        "page_count": 600,
        "description": "تاریخچه پیشرفت علمی در ایران اسلامی.",
        "is_published": True,
        "publisher_idx": 1
    },
    {
        "name": "زیست‌شناسی سلولی",
        "author": "بروس آلبرتس",
        "published_date": "2019-08-30",
        "price": 250000,
        "currency": "TOMAN",
        "category": "SC",
        "page_count": 800,
        "description": "مرجع جامع زیست‌شناسی سلول مولکولی.",
        "is_published": True,
        "publisher_idx": 0
    },
    {
        "name": "دره سکوت",
        "author": "هارلن کوبن",
        "published_date": "2021-05-15",
        "price": 78000,
        "currency": "TOMAN",
        "category": "TH",
        "page_count": 350,
        "description": "رمان پلیسی و مرموز با پیچش‌های داستانی.",
        "is_published": False,
        "publisher_idx": 1
    },
    {
        "name": "عاشقانه‌های فردوسی",
        "author": "علی شریعتی",
        "published_date": "1980-02-14",
        "price": 55000,
        "currency": "TOMAN",
        "category": "RM",
        "page_count": 220,
        "description": "تحلیل عشق در شاهنامه فردوسی.",
        "is_published": True,
        "publisher_idx": 0
    },
    {
        "name": "طنز و طنزپردازی",
        "author": "ساموئل بکت",
        "published_date": "1953-10-10",
        "price": 68000,
        "currency": "TOMAN",
        "category": "FN",
        "page_count": 190,
        "description": "نقد و بررسی هنر طنز در ادبیات جهان.",
        "is_published": True,
        "publisher_idx": 1
    }
]


def clear_database():
    """🗑️ پاک کردن کامل دیتابیس"""
    print("🗑️  در حال پاک کردن دیتابیس...")

    # شمارش قبل از پاک کردن
    book_count = Book.objects.count()
    user_count = User.objects.count()
    image_count = ImageBook.objects.count()

    print(f"   📚 کتاب‌ها: {book_count}")
    print(f"   👥 یوزرها: {user_count}")
    print(f"   🖼️  تصاویر: {image_count}")

    # پاک کردن (ترتیب مهمته!)
    ImageBook.objects.all().delete()
    Book.objects.all().delete()
    User.objects.filter(is_superuser=False).delete()  # سوپریوزرها رو نگه دار

    print("   ✅ دیتابیس پاک شد!\n")


def create_superuser():
    """👑 ساخت سوپریوزر"""
    print("👑 ساخت سوپریوزر...")

    # چک کن اگه وجود داشت پاک کن
    User.objects.filter(username=SUPERUSER_DATA['username']).delete()

    superuser = User.objects.create_superuser(
        username=SUPERUSER_DATA['username'],
        email=SUPERUSER_DATA['email'],
        password=SUPERUSER_DATA['password'],
        phone_number=SUPERUSER_DATA['phone_number'],
        national_code=SUPERUSER_DATA['national_code'],
        is_author=True,
    )

    print(f"   ✅ سوپریوزر ساخته شد: {superuser.username}")
    print(f"      رمز: {SUPERUSER_DATA['password']}")
    return superuser


def create_test_users():
    """👥 ساخت یوزرهای تست"""
    print("\n👥 ساخت یوزرهای تست...")
    created_users = []

    for user_data in USERS_DATA:
        user_obj = User.objects.create_user(
            username=user_data['username'],
            email=user_data['email'],
            password=user_data['password'],
            phone_number=user_data['phone_number'],
            national_code=user_data['national_code'],
            is_author=user_data['is_author'],
        )
        print(f"   ✅ {user_obj.username} ساخته شد")
        created_users.append(user_obj)

    return created_users


def create_test_books(user_list):
    """📚 ساخت کتاب‌های تست"""
    print("\n📚 ساخت کتاب‌ها...")
    created_books = []

    for book_info in BOOKS_DATA:
        publisher_user = user_list[book_info.pop('publisher_idx')]

        book_obj = Book.objects.create(
            name=book_info['name'],
            author=book_info['author'],
            published_date=book_info['published_date'],
            price=book_info['price'],
            currency=book_info['currency'],
            category=book_info['category'],
            page_count=book_info['page_count'],
            description=book_info['description'],
            is_published=book_info['is_published'],
            publisher=publisher_user,
            publisher_name=publisher_user.username,  # noqa
        )

        status_msg = "✅ منتشر شد" if book_obj.is_published else "📝 پیش‌نویس"
        print(f"   {status_msg}: {book_obj.name} ({publisher_user.username})")  # noqa
        created_books.append(book_obj)

    return created_books


def run_tests(user_list, book_list):
    """🧪 تست سریع دسترسی‌ها"""
    print("\n🧪 تست سریع دسترسی‌ها...")

    writer1 = user_list[0]
    writer2 = user_list[1]
    reader1 = user_list[2]

    # تست 1: writer1 چندتا کتاب داره؟
    w1_count = Book.objects.filter(publisher=writer1).count()
    print(f"   ✅ writer1: {w1_count} کتاب")

    # تست 2: writer2 چندتا کتاب داره؟
    w2_count = Book.objects.filter(publisher=writer2).count()
    print(f"   ✅ writer2: {w2_count} کتاب")

    # تست 3: reader1 چندتا کتاب داره؟
    r1_count = Book.objects.filter(publisher=reader1).count()
    print(f"   ✅ reader1: {r1_count} کتاب (باید 0 باشه)")

    # تست 4: چندتا منتشر شده؟
    pub_count = Book.objects.filter(is_published=True).count()
    print(f"   📚 منتشر شده: {pub_count}")

    # تست 5: چندتا پیش‌نویس؟
    draft_count = Book.objects.filter(is_published=False).count()
    print(f"   📝 پیش‌نویس: {draft_count}")


def print_final_summary(user_list, book_list):
    """📊 چاپ خلاصه نهایی"""
    print("\n" + "=" * 70)
    print("🎉 تمام شد! حالا می‌تونی در Postman تست کنی:")
    print("=" * 70)

    print("\n🔑 اطلاعات لاگین:")
    print(f"   👑 admin / {SUPERUSER_DATA['password']} (سوپریوزر)")
    for user_item in user_list:
        print(f"   ✍️  {user_item.username} / test12345")

    print("\n🌐 اندپوینت‌های تست:")
    print("   • POST http://localhost:8000/api/auth/login/")
    print("   • GET  http://localhost:8000/api/books/published/  (عمومی)")
    print("   • GET  http://localhost:8000/api/books/my/          (نیاز به توکن)")
    print("   • POST http://localhost:8000/api/books/my/          (ساخت کتاب)")
    print("   • GET  http://localhost:8000/api/books/my/<id>/     (جزئیات کتاب)")

    published_count = sum(1 for b in book_list if b.is_published)
    draft_count = len(book_list) - published_count

    print(f"\n📊 آمار نهایی:")
    print(f"   • کل یوزرها: {len(user_list) + 1} (3 نویسنده + 1 سوپریوزر)")
    print(f"   • کل کتاب‌ها: {len(book_list)}")
    print(f"   • منتشر شده: {published_count}")
    print(f"   • پیش‌نویس: {draft_count}")

    print("\n" + "=" * 70)
    print("⚠️  حالا این فایل (temp_setup.py) رو پاک کن!")
    print("=" * 70)


if __name__ == "__main__":
    print("🚀 شروع ریست کامل دیتابیس...\n")

    # تأیید از کاربر
    response = input("⚠️  همه داده‌ها پاک می‌شن! ادامه بدم؟ (yes/no): ")
    if response.lower() != 'yes':
        print("❌ لغو شد.")
        exit()

    # 1. پاک کردن
    clear_database()

    # 2. ساخت سوپریوزر
    superuser = create_superuser()

    # 3. ساخت یوزرها
    all_users = create_test_users()

    # 4. ساخت کتاب‌ها
    all_books = create_test_books(all_users)

    # 5. تست سریع
    run_tests(all_users, all_books)

    # 6. خلاصه
    print_final_summary(all_users, all_books)