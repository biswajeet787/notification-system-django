# NotifyHub – Backend

## 🔐 Admin Access – Read First

**Django Admin URL:**  
https://notification-system-api-xjqq.onrender.com/admin/

**Admin Username:** `YOUR_ADMIN_USERNAME`

**Admin Password:** `YOUR_ADMIN_PASSWORD`

**Live Frontend:**  
https://notification-system-frontend-three.vercel.app/login

**Backend API:**  
https://notification-system-api-xjqq.onrender.com

### How to Create Another Administrator Account

If you already have access to the Django Admin panel:

1. Open the Django Admin URL.
2. Log in using your existing administrator account.
3. Navigate to **Authentication and Authorization → Users**.
4. Click **Add User**.
5. Enter the new username and password.
6. Save the user.
7. Open the newly created user.
8. Enable the following permissions:
   - Active
   - Staff status
   - Superuser status
9. Save the changes.

The new account can now access the Django Admin panel and administrator features in NotifyHub.

**Important:** A superuser account created in your local database is not automatically available in the production Render database.

If no production administrator exists, one must first be created in the production database through an authorized administrative process. The local `python manage.py createsuperuser` command creates an account only in whichever database your local environment is connected to.

---

## 1. Project Overview

NotifyHub is a Notification Management System backend built using Python, Django, Django REST Framework and PostgreSQL.

It provides authentication, notification trigger management, notification templates and multi-channel notification delivery through Email, WhatsApp and Web Push.

## 2. Live Application

| Resource | URL |
|---|---|
| Backend | https://notification-system-api-xjqq.onrender.com |
| Django Admin | https://notification-system-api-xjqq.onrender.com/admin/ |
| Health Check | https://notification-system-api-xjqq.onrender.com/api/health/ |
| Frontend | https://notification-system-frontend-three.vercel.app/login |
| GitHub | https://github.com/biswajeet787/notification-system-django |

## 3. Project Setup Instructions

### Prerequisites

- Python 3.10 or later
- PostgreSQL
- Git
- Visual Studio Code (recommended)

### Step 1: Clone the repository

```bash
git clone https://github.com/biswajeet787/notification-system-django.git
cd notification-system-django
```

### Step 2: Create a virtual environment

```bash
python -m venv venv
```

Activate on Windows:

```powershell
.\venv\Scripts\Activate.ps1
```

Activate on Linux/macOS:

```bash
source venv/bin/activate
```

### Step 3: Install dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Configure environment variables

Create a `.env` file in the backend root directory.

```env
SECRET_KEY=your_django_secret_key
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost

DATABASE_URL=postgresql://username:password@localhost:5432/notification_system

BREVO_API_KEY=your_brevo_api_key
BREVO_SENDER_EMAIL=your_verified_sender_email
BREVO_SENDER_NAME=Notification System

WHATSAPP_ACCESS_TOKEN=your_whatsapp_access_token
WHATSAPP_PHONE_NUMBER_ID=your_whatsapp_phone_number_id
WHATSAPP_API_VERSION=vXX.X

VAPID_PUBLIC_KEY=your_vapid_public_key
VAPID_PRIVATE_KEY=your_vapid_private_key
VAPID_CLAIMS_EMAIL=mailto:your_email@example.com
```

Replace all placeholder values with your actual configuration.

The PostgreSQL database must exist before running the application.

### Step 5: Run migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### Step 6: Create a local administrator

```bash
python manage.py createsuperuser
```

Enter the requested username, email and password.

This command creates a superuser in the database configured by your local `.env`.

### Step 7: Start the backend

```bash
python manage.py runserver
```

Backend:

http://127.0.0.1:8000/

Health check:

http://127.0.0.1:8000/api/health/

## 4. Features

### Authentication

- User registration.
- User login and logout.
- Token-based authentication.
- Current-user profile endpoint.
- Role-based administrator and normal-user access.
- WhatsApp phone number associated with user profiles.

### Notification Management

- Create and manage notification triggers.
- Create and update notification templates.
- Enable or disable notification channels.
- Test notification templates.
- Dynamic template rendering using variable mapping.

### Notification Channels

**Email**
- Email delivery using Brevo API.
- Configurable sender details.
- Dynamic subject and body.

**WhatsApp**
- WhatsApp Cloud API integration.
- Template-based message delivery.
- Sandbox recipient support.

**Web Push**
- Browser notification subscriptions.
- VAPID authentication.
- Push delivery to registered browser subscriptions.
- Individual subscription testing.

### Trigger Events

- Login
- Logout

Each trigger can have separate Email, WhatsApp and Web Push templates.

## 5. API Endpoints

All endpoints use the `/api/` prefix.

### Authentication

| Method | Endpoint | Purpose |
|---|---|---|
| POST | `/api/auth/register/` | Register a user |
| POST | `/api/auth/login/` | Login |
| POST | `/api/auth/logout/` | Logout |
| GET | `/api/auth/me/` | Current user |

### Triggers

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/api/triggers/` | List triggers |
| POST | `/api/triggers/` | Create trigger |
| GET | `/api/triggers/{id}/` | Get trigger |
| PATCH | `/api/triggers/{id}/` | Update trigger |
| DELETE | `/api/triggers/{id}/` | Delete trigger |
| POST | `/api/triggers/{id}/fire/` | Fire trigger |

### Notification Templates

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/api/templates/` | List templates |
| POST | `/api/templates/` | Create template |
| GET | `/api/templates/{id}/` | Get template |
| PATCH | `/api/templates/{id}/` | Update template |
| DELETE | `/api/templates/{id}/` | Delete template |
| POST | `/api/templates/{id}/test/` | Test supported channels |

### Web Push

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/api/web-push/public-key/` | Get VAPID public key |
| GET | `/api/push-subscriptions/` | List subscriptions |
| POST | `/api/push-subscriptions/` | Register subscription |
| POST | `/api/push-subscriptions/{id}/test/` | Test subscription |

Protected APIs use token authentication:

```http
Authorization: Token YOUR_AUTH_TOKEN
```

## 6. Notification Template Variable Mapping

Example message:

```text
Hello {{name}}, welcome to NotifyHub!
```

Example mapping:

```json
{
  "name": "user.username"
}
```

The backend resolves the mapped values using notification context before sending the message.

## 7. External Integrations

### Brevo

Used for email notifications.

Requirements:
- Brevo account.
- API key.
- Verified sender email.

### WhatsApp Cloud API

Requirements:
- Meta Developer account.
- WhatsApp Cloud API configuration.
- Phone Number ID.
- Access token.
- Verified recipient in sandbox mode.

WhatsApp sandbox delivery is limited to eligible verified recipients.

### Web Push

Requirements:
- VAPID public key.
- VAPID private key.
- VAPID claims email.
- Browser notification permission.
- Registered browser subscription.

Web Push requires HTTPS in production. Localhost is also supported.

## 8. Production Deployment

The backend is deployed on Render.

- Hosting: Render
- Database: Render PostgreSQL
- Application server: Gunicorn
- Static files: WhiteNoise

### Production Environment Variables

Configure these in Render:

```env
SECRET_KEY=your_production_secret_key
DEBUG=False
ALLOWED_HOSTS=notification-system-api-xjqq.onrender.com
DATABASE_URL=your_render_internal_database_url

CORS_ALLOWED_ORIGINS=https://notification-system-frontend-three.vercel.app

BREVO_API_KEY=your_brevo_api_key
BREVO_SENDER_EMAIL=your_verified_sender_email
BREVO_SENDER_NAME=Notification System

WHATSAPP_ACCESS_TOKEN=your_whatsapp_access_token
WHATSAPP_PHONE_NUMBER_ID=your_whatsapp_phone_number_id
WHATSAPP_API_VERSION=vXX.X

VAPID_PUBLIC_KEY=your_vapid_public_key
VAPID_PRIVATE_KEY=your_vapid_private_key
VAPID_CLAIMS_EMAIL=mailto:your_email@example.com
```

### Build Command

```bash
pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate
```

### Start Command

```bash
gunicorn config.wsgi:application
```

## 9. Security

- Environment variables are used for secrets.
- `.env` is excluded from Git.
- VAPID private key files are excluded from Git.
- Token authentication protects API endpoints.
- Administrator-only APIs use administrator permissions.
- CORS is configured for approved frontend origins.

Never commit production credentials to GitHub.

## 10. Technology Stack

| Technology | Purpose |
|---|---|
| Python | Programming language |
| Django | Backend framework |
| Django REST Framework | REST APIs |
| PostgreSQL | Database |
| Gunicorn | Production server |
| WhiteNoise | Static file serving |
| Brevo | Email notifications |
| WhatsApp Cloud API | WhatsApp notifications |
| Web Push / VAPID | Browser notifications |
| Render | Backend hosting |

## 11. Author

Developed as part of the NotifyHub Notification Management System project.

**Backend Repository:** https://github.com/biswajeet787/notification-system-django