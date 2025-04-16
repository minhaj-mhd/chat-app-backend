# Django Chat API Backend

![Django](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white)
![Django REST](https://img.shields.io/badge/django%20rest-ff1709?style=for-the-badge&logo=django&logoColor=white)
![WebSocket](https://img.shields.io/badge/WebSocket-010101?style=for-the-badge&logo=websocket&logoColor=white)
![JWT](https://img.shields.io/badge/JWT-000000?style=for-the-badge&logo=JSON%20web%20tokens&logoColor=white)

A robust backend for a real-time chat application built with Django, Django REST Framework, and WebSockets. Features JWT authentication, real-time messaging, and friend management.

## ✨ Features

- **Secure Authentication**
  - JWT-based auth 
  - Custom middleware for token validation
  - Password encryption

- **Real-time Communication**
  - WebSocket implementation via Django Channels

- **Social Features**
  - User search functionality
  - Friend request system
  - Friend list management

- **Chat Functionality**
  - One-to-one messaging
  - Message history
  - WebSocket notifications

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Redis (for channel layers)
- PostgreSQL (recommended)

### Installation
```bash
# Clone repository
git clone https://github.com/yourusername/django-chat-backend.git
cd django-chat-backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your credentials

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser
