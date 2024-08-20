# SocialMedia App API

A social media platform built using Django REST framework, featuring JWT-based authentication, custom user management, posts, comments, likes, and comprehensive testing using Django's built-in test framework and Pytest.

## Features

- **JWT Authentication**: Secure authentication using `rest_framework_simple_jwt`
- **Custom User & Auth Apps**: Custom user model with registration and login endpoints
- **Post Creation**: Users can create, update, and delete posts
- **Commenting**: Comment on posts and manage comments
- **Likes**: Users can like/unlike posts
- **Comprehensive Testing**: Tests written using both Django's built-in testing tools and Pytest

## Prerequisites

- Python 3.x
- Django 3.x or higher
- Django REST Framework
- Pytest
- SQLite

## Installation

### 1. Clone the repository:

```bash
git clone https://github.com/yourusername/social-rest-api.git
cd social-rest-api
```

### 2. Create and activate a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install dependencies:

```bash
pip install -r requirements.txt
```

### 4. Configure the database:

Update the `settings.py` file to configure your database settings (use PostgreSQL or SQLite by default).

```bash
python manage.py migrate
```

### 5. Create a superuser:

```bash
python manage.py createsuperuser
```

### 6. Run the development server:

```bash
python manage.py runserver
```

The API will be accessible at `http://127.0.0.1:8000/`.

## API Endpoints

Here are some of the key endpoints in the API:

### Authentication

- `POST /api/auth/login/` - User login with JWT
- `POST /api/auth/register/` - User registration
- `POST /api/auth/refresh/` - Refresh JWT token

### Posts

- `GET /api/posts/` - List all posts
- `POST /api/posts/` - Create a new post
- `GET /api/posts/<id>/` - Retrieve a single post
- `PUT /api/posts/<id>/` - Update a post
- `DELETE /api/posts/<id>/` - Delete a post

### Comments

- `POST /api/posts/<id>/comments/` - Add a comment to a post
- `PUT /api/posts/<id>/comments/<id>/` - Update a comment
- `DELETE /api/posts/<id>/comments/<id>/` - Delete a comment

### Likes

- `POST /api/posts/<id>/like/` - Like/unlike a post

### User Profiles

- `GET /api/users/<id>/` - Retrieve user profile

## Customization

You can customize the project by:

1. Modifying the post, comment, and like models as needed.
2. Adding new features such as follower/following, hashtags, or media uploads.
3. Integrating third-party packages for additional functionality.

## Testing

This project includes tests for both core Django functionality and Pytest for advanced testing scenarios.

### Running Django tests:

```bash
python manage.py test
```

### Running Pytest:

```bash
pytest
```

Ensure that all tests pass before deployment.

## Deployment

For deploying the API, follow these steps:

1. Set up a production database and update the `settings.py` file.
2. Use a WSGI server like Gunicorn:

```bash
gunicorn socialmedia.wsgi:application --bind 0.0.0.0:8000
```

3. Set up your web server (e.g., Nginx) for serving the application.

## Contributing

Contributions are welcome! Fork the repository and submit a pull request to propose new features, improvements, or bug fixes.
