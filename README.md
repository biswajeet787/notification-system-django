
# Notification System — Django Backend

A Django REST Framework backend for a full-stack Notification Management System. It manages notification triggers and templates and delivers notifications through Email, WhatsApp, and Web Push channels.

## Features

- Create, update, and delete notification triggers.
- Create, update, and delete notification templates.
- Enable or disable individual notification channels.
- Send notifications when triggers are fired.
- Dynamic template rendering with user information.
- Email delivery through Brevo Transactional Email API.
- WhatsApp delivery through Meta WhatsApp Cloud API Sandbox.
- Browser push notifications using Web Push and VAPID.
- Store notification triggers, templates, and browser subscriptions in PostgreSQL.
- Django Admin integration.
- Individual delivery results for each notification channel.

## Tech Stack

- Python
- Django
- Django REST Framework
- PostgreSQL
- Brevo REST API
- Meta WhatsApp Cloud API
- Web Push
- pywebpush
- VAPID

## Project Structure

```text
notification-system-django/
├── config/
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── notifications/
│   ├── migrations/
│   ├── management/
│   │   └── commands/
│   ├── services/
│   │   ├── email_service.py
│   │   ├── whatsapp_service.py
│   │   ├── web_push_service.py
│   │   └── template_renderer.py
│   ├── admin.py
│   ├── models.py
│   ├── serializers.py
│   ├── urls.py
│   └── views.py
├── .env.example
├── .gitignore
├── manage.py
├── requirements.txt
└── README.md
```

## Windows Setup

Open this folder in VS Code Terminal.

### 1. Create a virtual environment

```powershell
python -m venv venv
```

### 2. Activate the virtual environment

```powershell
.\venv\Scripts\Activate.ps1
```

### 3. Upgrade pip

```powershell
python -m pip install --upgrade pip
```

### 4. Install dependencies

```powershell
pip install -r requirements.txt
```

## Environment Configuration

Copy `.env.example` to `.env`.

Configure the following environment variables:

```env
# Django Configuration
SECRET_KEY=your_django_secret_key
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost

# PostgreSQL Database
DATABASE_URL=your_postgresql_database_url

# Brevo Email API
BREVO_API_KEY=your_brevo_api_key
BREVO_SENDER_EMAIL=your_verified_sender_email
BREVO_SENDER_NAME=Notification System

# WhatsApp Cloud API Sandbox
WHATSAPP_ACCESS_TOKEN=your_whatsapp_test_token
WHATSAPP_PHONE_NUMBER_ID=your_test_phone_number_id
WHATSAPP_API_VERSION=v26.0

# Web Push Configuration
VAPID_PUBLIC_KEY=your_vapid_public_key
VAPID_PRIVATE_KEY=your_vapid_private_key
VAPID_CLAIMS_EMAIL=mailto:your_email@example.com
```

**Important:**

- This project is configured for PostgreSQL only. SQLite is not supported.
- Use your Render PostgreSQL External Database URL for local development.
- Never commit or share your actual `.env` file.
- Never commit your Brevo API key, WhatsApp access token, or VAPID private key.
- Keep `.env.example` updated with placeholder values only.

## Database Setup

Run the following commands:

```powershell
python manage.py check
python manage.py makemigrations notifications
python manage.py migrate
```

Create a Django admin account:

```powershell
python manage.py createsuperuser
```

Load demo triggers and templates:

```powershell
python manage.py seed_demo
```

## Run Development Server

```powershell
python manage.py runserver
```

Backend URL:

http://127.0.0.1:8000/

API base URL:

http://127.0.0.1:8000/api/

Health check:

http://127.0.0.1:8000/api/health/

Django Admin:

http://127.0.0.1:8000/admin/

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/health/` | Check API health |
| GET | `/api/triggers/` | List notification triggers |
| POST | `/api/triggers/` | Create a trigger |
| GET | `/api/triggers/{id}/` | Retrieve a trigger |
| PUT/PATCH | `/api/triggers/{id}/` | Update a trigger |
| DELETE | `/api/triggers/{id}/` | Delete a trigger |
| POST | `/api/triggers/{id}/fire/` | Fire a notification trigger |
| GET | `/api/templates/` | List notification templates |
| POST | `/api/templates/` | Create a template |
| GET | `/api/templates/{id}/` | Retrieve a template |
| PUT/PATCH | `/api/templates/{id}/` | Update a template |
| DELETE | `/api/templates/{id}/` | Delete a template |
| POST | `/api/templates/{id}/test/` | Test a notification template |

Additional Web Push endpoints are provided for browser subscription management and notification testing.

## Notification Integrations

### 1. Email — Brevo

Email notifications use the Brevo Transactional Email REST API.

Configuration requires:

- Brevo API key.
- Verified sender email address.
- Sender name.

The backend renders notification templates and sends personalized emails through Brevo.

### 2. WhatsApp — Meta WhatsApp Cloud API Sandbox

WhatsApp notifications use the Meta WhatsApp Cloud API sandbox.

Configuration requires:

- Meta Developer account.
- WhatsApp Cloud API test phone number.
- WhatsApp temporary access token.
- Verified test recipient phone number.

**Important:** The sandbox access token expires periodically. Generate a new token from Meta Developer Dashboard when the existing token expires and update the backend environment variable.

### 3. Web Push Notifications

Browser notifications use Web Push with VAPID authentication and the `pywebpush` library.

The frontend allows users to subscribe their browsers.

The backend stores browser subscription information in PostgreSQL and uses the saved subscriptions to deliver push notifications.

Browser notification permission must be granted before receiving notifications.

## Notification Trigger Flow

1. An event such as Login or Logout is triggered from the frontend.
2. The backend identifies the corresponding notification trigger.
3. The backend retrieves its enabled notification templates.
4. The backend renders the templates using the supplied user information.
5. Notifications are sent through the enabled channels.
6. The API returns individual delivery results for each channel.

If one channel fails, the backend reports its failure separately from successful channel deliveries.

## Render Deployment

Deploy the Django backend as a Render Web Service.

### Build Command

```bash
pip install -r requirements.txt
```

### Start Command

```bash
gunicorn config.wsgi:application
```

### Environment Variables

Configure the required environment variables in Render:

- `SECRET_KEY`
- `DEBUG=False`
- `DATABASE_URL`
- `ALLOWED_HOSTS`
- `BREVO_API_KEY`
- `BREVO_SENDER_EMAIL`
- `BREVO_SENDER_NAME`
- `WHATSAPP_ACCESS_TOKEN`
- `WHATSAPP_PHONE_NUMBER_ID`
- `WHATSAPP_API_VERSION`
- `VAPID_PUBLIC_KEY`
- `VAPID_PRIVATE_KEY`
- `VAPID_CLAIMS_EMAIL`

Use the PostgreSQL Internal Database URL when the backend and database are in the same Render region.

Configure production CORS settings to allow requests from the deployed frontend.

After deployment, run database migrations:

```bash
python manage.py migrate
```

## Security

- API credentials are stored in environment variables.
- Actual `.env` files are excluded from Git.
- VAPID private keys are not committed.
- Production deployment should use `DEBUG=False`.
- Configure appropriate allowed hosts and frontend CORS origins.

## Author

**Biswajeet Sahoo**

GitHub: https://github.com/biswajeet787