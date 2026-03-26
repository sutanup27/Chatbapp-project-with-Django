# Chatbapp - Django Chat Application

A real-time chat application built with Django, Django REST Framework, and Django Channels with WebSocket support.

## Overview

Chatbapp is a full-featured chat application that allows users to communicate in real-time through group and direct messaging. The application uses WebSockets for instant message delivery and includes user authentication, profile management, and file sharing capabilities.

### Features

- **Real-time Messaging**: Instant message delivery using Django Channels and WebSockets
- **Group Chats**: Create and manage chat rooms/groups
- **Direct Messaging**: One-on-one conversations between users
- **User Authentication**: Secure user registration and login
- **User Profiles**: Customizable user profiles with avatars
- **File Sharing**: Upload and share files in chat
- **REST API**: Complete REST API for frontend integration
- **Django Admin**: Comprehensive admin interface for managing content

## Prerequisites

- Python 3.7 or higher
- pip (Python package manager)
- Redis Server
- MongoDB (or Django's default database)
- Virtual environment tool (virtualenv or venv)

## Installation & Setup

### 1. Django Environment Setup

1. **Install Python**: Ensure Python 3.7+ is installed on your system
2. **Install virtualenvwrapper** (for Windows):
   ```bash
   pip install virtualenvwrapper-win
   ```
   
3. **Create a virtual environment**:
   ```bash
   mkvirtualenv django_env
   ```
   
4. **Activate the virtual environment**:
   - On Windows:
     ```bash
     django_env\Scripts\activate
     ```
   - On macOS/Linux:
     ```bash
     source django_env/bin/activate
     ```

5. **Clone/Navigate to project directory**:
   ```bash
   cd Chatbapp-project-with-Django
   ```

6. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
   
   Or install packages individually:
   ```bash
   pip install django==2.2
   pip install djangorestframework
   pip install django-cors-headers
   ```

### 2. Django Channels Setup (Real-time Messaging)

Django Channels enables real-time WebSocket communication. Install the required packages:

```bash
python -m pip install -U channels
python -m pip install -U channels-redis
pip install daphne
```

### 3. Redis Server Installation

Redis is used as the message broker for Django Channels.

**For Windows**:
- Download from: https://github.com/microsoftarchive/redis/releases
- Or use Windows Subsystem for Linux (WSL) and run: `sudo apt-get install redis-server`

**For macOS** (using Homebrew):
```bash
brew install redis
```

**For Linux**:
```bash
sudo apt-get install redis-server
```

### 4. MongoDB Installation (Optional - if using)

If using MongoDB as the database:

1. Install MongoDB from: https://docs.mongodb.com/manual/installation/
2. Verify MongoDB installation:
   ```bash
   mongo
   ```
3. Check available databases:
   ```bash
   show dbs
   ```

Note: It is always best to use WSL for smoother installations.
## Running the Application

### Step 1: Start Redis Server

**For Windows**:
```bash
redis-server
```

**For Linux/macOS**:
```bash
redis-cli ping  # Check if Redis is running
# If not running, start it:
sudo service redis-server start
```

### Step 2: Start MongoDB (if applicable)

```bash
mongod
```

### Step 3: Apply Database Migrations

```bash
python manage.py migrate
```

### Step 4: Create a Superuser (Admin Account)

```bash
python manage.py createsuperuser
```

### Step 5: Collect Static Files (for production)

```bash
python manage.py collectstatic
```

### Step 6: Run the Development Server

Navigate to the `chatter` directory and run:

```bash
python manage.py runserver
```

Or specify a custom host and port:

```bash
python manage.py runserver 0.0.0.0:8000
```

### Step 7: Access the Application

- **Home Page**: http://localhost:8000
- **Admin Panel**: http://localhost:8000/admin
- **API Root**: http://localhost:8000/api

## Project Structure

```
├── chatter/              # Main project settings
│   ├── settings.py       # Django settings
│   ├── urls.py           # URL routing
│   ├── wsgi.py           # WSGI configuration
│   └── routing.py        # WebSocket routing
├── accounts/             # User authentication and profiles
│   ├── models.py         # User and Profile models
│   ├── views.py          # Authentication views
│   └── api_urls.py       # REST API endpoints
├── chat/                 # Chat functionality
│   ├── models.py         # ChatRoom and Message models
│   ├── views.py          # Chat views
│   ├── consumers.py      # WebSocket consumers
│   └── routing.py        # Chat routing
├── templates/            # HTML templates
├── static/               # CSS, JavaScript, images
├── media/                # User uploads (avatars, files)
└── manage.py             # Django management script
```

## API Endpoints

Key API endpoints available:

- `GET /api/users/` - List all users
- `POST /api/auth/register/` - User registration
- `POST /api/auth/login/` - User login
- `GET /api/chatrooms/` - List chat rooms
- `POST /api/chatrooms/` - Create a new chat room
- `GET /api/messages/` - List messages
- See API documentation in admin panel for complete list
  
## Demo
CLick to play the video below:
[![Watch Demo](https://img.youtube.com/vi/verJp_fhGxU/0.jpg)](https://www.youtube.com/watch?v=verJp_fhGxU)
## Troubleshooting

### Redis Connection Error
- Ensure Redis server is running: `redis-cli ping` should return `PONG`
- If using custom Redis settings, update `CHANNEL_LAYERS` in `settings.py`

### Database Migration Errors
```bash
python manage.py migrate accounts
python manage.py migrate chat
```

### WebSocket Not Connecting
- Check that `daphne` is installed: `pip install daphne`
- Verify `ASGI_APPLICATION` is configured in settings
- Check browser console for connection errors

### Static Files Not Loading
```bash
python manage.py collectstatic --clear --noinput
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request




