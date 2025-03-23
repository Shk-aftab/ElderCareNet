# ElderCareNet - Thesis Project Proposal

## Title:
Social Networking Platform for Elderly: An Interactive Health Article Community

## Overview:
This project proposes the development of a social networking platform tailored specifically for elderly users (ages 50+), focusing primarily on providing and interacting with curated health-related articles. Unlike typical social networks, the site will prioritize ease of use, readability, and user-friendliness suitable for elderly individuals.

## Objectives:
- To create an intuitive and accessible platform for elderly users to engage with health-related content.
- To promote social interaction among elderly users via comment sections under health articles.
- To empower users with personalized experiences, including adjustable readability settings (e.g., font size).

## Target Audience:
- Elderly individuals (aged 50 and above)

## Functional Requirements:

### User Registration & Authentication:
- Registration with name, age, email, password.
- Login/logout functionality.

### Health Articles:
- Admin-only capabilities to create, edit, and delete health-related articles.
- Users can read, comment, and save articles to their profile for later reference.

### Commenting System:
- Users can post comments under health articles.
- Comments displayed chronologically or by popularity.

### User Profile & Personalization:
- Update personal information.
- Manage saved articles.
- Personalize site readability (e.g., change font size).

### Administration Panel:
- Secure authentication.
- Manage users and content effectively.
- CRUD operations for health articles.

## Technology Stack:

### Frontend:
- Jinja, HTML and CSS
- CSS framework (e.g., Tailwind CSS) for responsive design and easy readability.

### Backend:
- FastAPI (Python-based REST API framework)

### Database:
- Sqlite

## Proposed Database Schema:

### Users:
- user_id (PK)
- name
- age (optional)
- email (unique)
- password_hash
- font_size_preference
- created_at

### Articles:
- article_id (PK)
- title
- content (rich-text)
- created_at
- updated_at
- author_id (FK to admin users)

### Comments:
- comment_id (PK)
- article_id (FK)
- user_id (FK)
- content
- created_at

### Saved Articles:
- saved_id (PK)
- user_id (FK)
- article_id (FK)
- saved_at

### Admins:
- admin_id (PK)
- name
- email (unique)
- password_hash
- created_at

## User Flow:
- **Registration/Login** → **Article Browsing** → **View Article** → **Comment / Save Article** → **Adjust Personal Preferences** → **Logout**
- **Admin Login** → **Manage Articles** → **Logout**

## Initial Flowchart:


## Setup Instructions

1. **Clone the Repository & Navigate:**
   ```bash
   git clone https://github.com/Shk-aftab/ElderCareNet
   cd ElderCareNet/backend
   ```

2. **Create a Conda Environment & Install Packages:**
   ```bash
   conda create --name eldercarenet python
   conda activate eldercarenet
   pip install -r requirements.txt
   ```

3. **Start the Application:**
   ```bash
   uvicorn main:app --reload
   ```
