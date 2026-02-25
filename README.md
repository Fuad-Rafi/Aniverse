# Aniverse — Social Blogging Platform

Aniverse is a full-stack Django platform where users can publish rich blog posts, build profiles, connect through friend requests, and chat with friends through direct messages.

It combines classic blogging features with social networking interactions in one clean app.

## Highlights

- Rich-text blog posting with categories, snippets, and header images
- Full authentication flow (register, login, logout, password change)
- Personalized user profiles with bio and profile picture
- Post likes and post comments
- Friend request system (send, accept, pending states)
- Friend-only direct messaging and chat conversation view
- Search across titles, content, author fields, categories, and snippets

## Tech Stack

- **Backend:** Django 4.2.x (Python)
- **Database:** SQLite (default)
- **Editor:** CKEditor (`django-ckeditor`)
- **Media Handling:** Django media storage (`/media`)
- **Frontend:** Django Templates + custom CSS

## Core Features

### 1) Authentication & Accounts

- User registration with custom signup form
- Login/logout using Django auth views
- Profile/account editing
- Password change workflow

### 2) Blog System

- Create, update, delete, and view posts
- Rich body content via CKEditor (`RichTextField`)
- Category-based organization
- Snippet support for preview text
- Optional header image uploads

### 3) Social Interactions

- Like/unlike posts with total like count
- Add comments on post detail pages
- View other users’ profiles and their posts

### 4) Friendship + Messaging

- Send and accept friend requests
- Pending request tracking (incoming + sent)
- Friends list generation from accepted requests
- Direct messages allowed only between friends
- Conversation view for 1:1 chat

### 5) Search

Search supports:

- post title
- post body
- author username / first name / last name
- category
- snippet

## Project Structure

```text
Aniverse/
├─ Ani_blog/                # Blog app (posts, categories, comments, social models)
├─ members/                 # User/account/friend/chat flows
├─ Aniverse/                # Project settings and root URLs
├─ static/                  # CSS + static assets
├─ media/                   # Uploaded images
├─ manage.py
└─ db.sqlite3
```

## Data Models (Key)

- **Post**: title, title_tag, author, body, post_date, category, snippet, header_image, likes
- **Category**: name
- **Profile**: user, bio, profile_pic, fb_url
- **Comment**: post, author, body, created_on
- **FriendRequest**: sender, receiver, status (`pending|accepted|rejected`), timestamps
- **DirectMessage**: sender, receiver, body, created_on

## Main Routes

### Auth + Members

- `/` → login page
- `/members/register/` → register
- `/members/edit_profile/` → edit account
- `/members/password/` → change password
- `/members/my_profile/` → redirect to your profile/create profile
- `/members/friend-requests/` → incoming/sent requests + friends list
- `/members/friend-request/send/<user_id>/`
- `/members/friend-request/accept/<request_id>/`
- `/members/chat/<user_id>/` → chat conversation
- `/members/chat/send/<user_id>/` → send DM

### Blog

- `/home/` → post feed
- `/home/post/<pk>` → post detail
- `/home/add_post/` → create post
- `/home/post/edit/<pk>` → edit post
- `/home/post/<pk>/remove` → delete post
- `/home/post/<pk>/comment/` → add comment
- `/home/add_category/` → add category
- `/home/category/<cats>/` → category feed
- `/home/category-list/` → all categories
- `/home/like/<pk>` → like/unlike
- `/home/search` → search

## Getting Started

### 1) Clone and enter project

```bash
git clone <your-repo-url>
cd Aniverse
```

### 2) Create virtual environment

```bash
python -m venv .venv
```

Activate:

- **Windows (PowerShell):**
  ```powershell
  .\.venv\Scripts\Activate.ps1
  ```
- **macOS/Linux:**
  ```bash
  source .venv/bin/activate
  ```

### 3) Install dependencies

```bash
pip install django django-ckeditor pillow
```

### 4) Run migrations

```bash
python manage.py migrate
```

### 5) (Optional) Create admin user

```bash
python manage.py createsuperuser
```

### 6) Start development server

```bash
python manage.py runserver
```

Open:

- `http://127.0.0.1:8000/` (login)
- `http://127.0.0.1:8000/home/` (after login)

## Configuration Notes

- `DEBUG=True` is for development only.
- Default DB is SQLite (`db.sqlite3`).
- Uploaded files are served from `/media/` in development.
- Static files are loaded from `/static/`.

## Why Aniverse Stands Out

Aniverse is not just a CRUD blog. It blends content creation, profile identity, friendship relationships, and direct messaging in one cohesive Django project—making it a strong portfolio-grade social platform.

---

If you want, I can also generate a matching `requirements.txt` and a short API/routes reference table to make this project even more recruiter-friendly.
