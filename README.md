# Blog API

A clean, modern RESTful API for a blogging platform built with **FastAPI**, **SQLAlchemy**, and **MySQL**. It supports user authentication (JWT), post creation with auto-generated slugs, cover image uploads, commenting, and post likes.

---

## Features

- **Authentication & Authorization**: User registration, password hashing (bcrypt), and JWT-based session tokens.
- **Blog Posts**: Create and read blog posts with automatic slug generation and pagination.
- **Media Uploads**: Upload and serve post cover images via static file mounts.
- **Social Engagement**: Add comments to posts and toggle post likes.
- **Interactive Documentation**: Built-in Swagger UI and ReDoc OpenAPI documentation.

---

## Tech Stack

- **Framework**: [FastAPI](https://fastapi.tiangolo.com/)
- **ORM / Database**: [SQLAlchemy](https://www.sqlalchemy.org/) with MySQL (`pymysql`)
- **Validation**: [Pydantic](https://docs.pydantic.dev/)
- **Security**: `passlib[bcrypt]`, `python-jose`
- **Server**: [Uvicorn](https://www.uvicorn.org/)

---

## Project Structure

```text
blog-api/
├── app/
│   ├── api/          # Route handlers (auth, users, posts, dependencies)
│   ├── core/         # Settings and security utilities
│   ├── db/           # Database engine, session, and base model
│   ├── models/       # SQLAlchemy models (User, Post, Comment, Like)
│   ├── repository/   # Database CRUD operations
│   ├── schemas/      # Pydantic schemas for request/response validation
│   ├── static/       # Uploaded media files
│   └── main.py       # Application entry point & router mounting
├── .env              # Environment configuration
└── requirements.txt  # Project dependencies
```

---

## Getting Started

### 1. Prerequisites

- Python 3.10+
- Running MySQL server

### 2. Installation

1. **Clone or navigate to the repository:**
   ```bash
   cd blog-api
   ```

2. **Create and activate a virtual environment:**
   ```bash
   # Windows (PowerShell)
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1

   # Linux / macOS
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

### 3. Environment Variables

Create a `.env` file in the root directory:

```env
DATABASE_URL="mysql+pymysql://<user>:<password>@localhost:3306/<database_name>"
SECRET_KEY="your-super-secret-jwt-key"
JWT_ALGORITHM="HS256"
```

### 4. Run the Server

```bash
uvicorn app.main:app --reload
```

The application will start at `http://127.0.0.1:8000`.

---

## API Documentation

FastAPI provides interactive documentation out of the box once the server is running:

- **Swagger UI**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **ReDoc**: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

---

## API Endpoints

| Method | Endpoint | Description | Auth Required |
| :--- | :--- | :--- | :---: |
| `POST` | `/auth/register` | Register a new user | No |
| `POST` | `/auth/login` | Login and receive JWT access token | No |
| `GET` | `/users/me` | Get current authenticated user profile | Yes |
| `GET` | `/posts` | List posts with pagination (`skip`, `limit`) | No |
| `POST` | `/posts` | Create a new blog post | Yes |
| `GET` | `/posts/{slug}` | Get post details by slug | No |
| `POST` | `/posts/{post_id}/image` | Upload post cover image (Author only) | Yes |
| `GET` | `/posts/{post_id}/comments` | Get all comments for a post | No |
| `POST` | `/posts/{post_id}/comments` | Add a comment to a post | Yes |
| `POST` | `/posts/{post_id}/like` | Toggle like status on a post | Yes |
