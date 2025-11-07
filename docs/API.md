# API Documentation

Base URL: `https://api.motken.com/api/v1/`

## Authentication

### Register User
```http
POST /auth/register/
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "SecurePassword123",
  "first_name": "John",
  "last_name": "Doe",
  "user_type": "student",
  "phone_number": "+1234567890"
}
```

### Login
```http
POST /auth/login/
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "SecurePassword123"
}

Response:
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "user": {
    "id": "uuid",
    "email": "user@example.com",
    "user_type": "student"
  }
}
```

### Refresh Token
```http
POST /auth/token/refresh/
Content-Type: application/json

{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

## Teachers

### List Teachers
```http
GET /teachers/?page=1&search=&specialization=tajweed
Authorization: Bearer {access_token}

Response:
{
  "count": 50,
  "next": "http://api.../teachers/?page=2",
  "previous": null,
  "results": [
    {
      "id": "uuid",
      "user": {
        "first_name": "Ahmed",
        "last_name": "Hassan",
        "profile_picture": "url"
      },
      "bio": "...",
      "specializations": ["tajweed", "memorization"],
      "years_of_experience": 10,
      "average_rating": 4.8,
      "session_30min_rate": 15.00,
      "is_available": true
    }
  ]
}
```

### Get Teacher Detail
```http
GET /teachers/{teacher_id}/
Authorization: Bearer {access_token}
```

### Teacher Availability
```http
GET /teachers/{teacher_id}/availability/
Authorization: Bearer {access_token}

Response:
{
  "availability": [
    {
      "day_of_week": 0,
      "start_time": "09:00:00",
      "end_time": "17:00:00"
    }
  ]
}
```

## Sessions

### Book Session
```http
POST /sessions/book/
Authorization: Bearer {access_token}
Content-Type: application/json

{
  "teacher": "teacher_uuid",
  "scheduled_date": "2024-02-01",
  "scheduled_time": "10:00:00",
  "duration": 30,
  "curriculum": "Tajweed Basics",
  "lesson_topic": "Noon Saakin rules"
}
```

### List My Sessions
```http
GET /sessions/my-sessions/?status=scheduled
Authorization: Bearer {access_token}
```

### Get Session Detail
```http
GET /sessions/{session_id}/
Authorization: Bearer {access_token}
```

### Cancel Session
```http
POST /sessions/{session_id}/cancel/
Authorization: Bearer {access_token}
Content-Type: application/json

{
  "cancellation_reason": "Emergency came up"
}
```

### Join Session (Get Zoom Link)
```http
GET /sessions/{session_id}/join/
Authorization: Bearer {access_token}

Response:
{
  "zoom_join_url": "https://zoom.us/j/...",
  "zoom_meeting_password": "123456"
}
```

## Payments

### List Packages
```http
GET /payments/packages/
Authorization: Bearer {access_token}

Response:
{
  "results": [
    {
      "id": "uuid",
      "name": "Basic Package",
      "session_count": 4,
      "session_duration": 30,
      "price": 50.00,
      "final_price": 45.00,
      "features": ["Recordings", "Materials"]
    }
  ]
}
```

### Purchase Package
```http
POST /payments/purchase/
Authorization: Bearer {access_token}
Content-Type: application/json

{
  "package": "package_uuid",
  "payment_method": "paymob_card",
  "coupon_code": "WELCOME10"
}

Response:
{
  "transaction_id": "uuid",
  "payment_url": "https://paymob.com/...",
  "status": "pending"
}
```

### Apply Coupon
```http
POST /payments/apply-coupon/
Authorization: Bearer {access_token}
Content-Type: application/json

{
  "coupon_code": "SUMMER2024",
  "package_id": "package_uuid"
}

Response:
{
  "valid": true,
  "discount_amount": 10.00,
  "final_amount": 40.00
}
```

### Payment Webhook (Paymob)
```http
POST /payments/webhook/paymob/
Content-Type: application/json

# Paymob will send payment confirmation
```

## Learning

### List Curricula
```http
GET /learning/curricula/
Authorization: Bearer {access_token}

Response:
{
  "results": [
    {
      "id": "uuid",
      "name": "Tajweed Basics",
      "curriculum_type": "tajweed",
      "difficulty": "beginner",
      "total_lessons": 20,
      "enrolled_students": 150
    }
  ]
}
```

### Get Curriculum Detail
```http
GET /learning/curricula/{curriculum_id}/
Authorization: Bearer {access_token}
```

### List Lessons
```http
GET /learning/curricula/{curriculum_id}/lessons/
Authorization: Bearer {access_token}
```

### Get My Progress
```http
GET /learning/progress/
Authorization: Bearer {access_token}

Response:
{
  "results": [
    {
      "curriculum": {...},
      "status": "in_progress",
      "progress_percent": 65.5,
      "lessons_completed": 13,
      "lessons_total": 20
    }
  ]
}
```

### Mark Lesson Complete
```http
POST /learning/lessons/{lesson_id}/complete/
Authorization: Bearer {access_token}
Content-Type: application/json

{
  "time_spent_minutes": 45,
  "score": 85
}
```

## Profile

### Get My Profile
```http
GET /auth/profile/
Authorization: Bearer {access_token}
```

### Update Profile
```http
PATCH /auth/profile/
Authorization: Bearer {access_token}
Content-Type: multipart/form-data

{
  "first_name": "John",
  "profile_picture": <file>,
  "timezone": "America/New_York"
}
```

### Get My Subscription
```http
GET /payments/my-subscription/
Authorization: Bearer {access_token}

Response:
{
  "package": {...},
  "status": "active",
  "sessions_remaining": 6,
  "end_date": "2024-03-01"
}
```

## Error Responses

All endpoints return errors in this format:

```json
{
  "success": false,
  "error": {
    "message": "Error description",
    "code": 400,
    "details": {
      "field_name": ["Error message"]
    }
  }
}
```

### Common Status Codes
- 200: Success
- 201: Created
- 400: Bad Request
- 401: Unauthorized
- 403: Forbidden
- 404: Not Found
- 429: Too Many Requests
- 500: Internal Server Error

## Rate Limiting

- Anonymous users: 100 requests/hour
- Authenticated users: 1000 requests/hour

Rate limit headers:
- `X-RateLimit-Limit`: Request limit
- `X-RateLimit-Remaining`: Remaining requests
- `X-RateLimit-Reset`: Time until limit resets

## Pagination

All list endpoints support pagination:
```http
GET /teachers/?page=2&page_size=20
```

Response includes:
- `count`: Total number of items
- `next`: URL to next page
- `previous`: URL to previous page
- `results`: Array of items
