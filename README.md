# ALkemy

Purpose: Dashboard for secure community messaging with groups/channels, threaded conversations, real-time updates, role-based permissions, moderation tools, and background-processed notifications/analytics.

## Stack

Django + Django REST Framework 
PostgreSQL (later - start with SQLite)
React + TypeScript + Vite + Tailwind CSS
Docker Compose 
Celery + Redis 
Django Channels + GraphQL subscriptions 

### 1. Initialize Django Backend

Create backend directory and set up Django

### 2. Create First App & Simple Model

Add to core/settings.py:
- Add 'messages', 'rest_framework', 'corsheaders' to INSTALLED_APPS
- Add corsheaders middleware
- Configure CORS_ALLOWED_ORIGINS = ['http://localhost:5173']
- Configure REST_FRAMEWORK settings

Create simple Message model in messages/models.py:
- id (auto)
- text (TextField)
- author (CharField)
- created_at (DateTimeField)

### 3. Create Simple REST API

In messages/ create:
- serializers.py (MessageSerializer)
- views.py 
- urls.py (router for /api/messages/)

### 4. Initialize React Frontend

Create frontend with Vite:


Configure Tailwind in tailwind.config.js and src/index.css

Verify React works at http://localhost:5173

### 5. Connect Frontend to Backend

Create a simple test component:
- Fetch messages from Django API using axios
- Display list of messages
- Form to create new message
- POST to Django API

### 6. Expand Models & Django Apps

Create proper Django apps:
- Groups 
- Users

Define new models:
- Custom User model (extend AbstractUser)
- Group/Channel (name, description, private/public, members)
- Thread (group, subject, created_by, created_at)
- Message (thread, text, author, parent_message for replies, created_at)
- Membership/Roles (user, group, role: admin/moderator/member)

Add relationships and migrations

### 7. Build Out REST API

Create serializers and viewsets for:
- User registration, login 
- Groups 
- Threads 
- Messages 

Add authentication to views (IsAuthenticated permission)
Add permission checks (can only delete own messages, moderators can delete any)

### 8. Build Frontend Features

Create pages:
- Login/Register page
- Groups list page
- Thread view page
- Message list with reply functionality

Implement:
- Auth flow 
- Protected routes
- Group selection sidebar
- Thread list for selected group
- Message posting with @mentions
- Basic styling with Tailwind

### 9. Switch to PostgreSQL

Install psycopg2 and configure settings to use PostgreSQL
Create database and migrate existing data

### 10. Add GraphQL 

Install graphene-django
Create GraphQL schema for existing models
Add queries, mutations
Test in GraphiQL at /graphql/
Update frontend to use Apollo Client

### 11. Add Real-Time with Django Channels

Install channels and daphne
Configure channel layers with Redis
Create WebSocket consumers for live messages
Update frontend to subscribe to message updates
Test real-time messaging

### 12. Add Background Tasks with Celery

Install celery and redis
Configure celery.py
Create tasks:
- send_notification_email (on @mentions)
- generate_daily_report
- moderate_content_check

Add celery worker and beat to your setup
Test tasks execute in background

### 13. Dockerize Everything

Create docker-compose.yml with services:
- postgres
- redis
- backend (Django)
- celery-worker
- celery-beat  
- frontend (React)

Create Dockerfiles for backend and frontend

### 14. Testing

Write tests for:
- Django models and API endpoints (pytest-django)
- Frontend components (Vitest/React Testing Library)
- Integration tests for key flows
