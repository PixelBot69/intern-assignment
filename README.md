Intern Assignment - Candidate Profile Playground
This is a full-stack mini project built with Flask, SQLite, and standard HTML/JS. It's a candidate profile playground that stores profile information and projects in a database, exposes them via REST APIs, and provides a minimal frontend for querying.

🚀 Live Demo
You can explore a live demo of the application here: https://intern-assignment-y91g.onrender.com

📂 Features
REST APIs:

/profile — Retrieves candidate profile details (name, email, education, skills, links).

/projects — Provides a list of projects with support for filtering by skill and pagination (/projects?skill=python&page=1&limit=3).

/skills/top — Lists the top skills from the candidate's profile.

/search — Searches projects by title (/search?q=...).

/health — A simple liveness check for the application.

Authentication: Write operations (POST /projects) are protected with Basic Auth using environment variables.

Database Management: The application automatically reseeds the SQLite database on startup to handle Render's ephemeral filesystem.

Frontend: A minimal UI is provided for viewing the profile and projects.

🛠️ Tech Stack
Backend: Flask and SQLAlchemy

Database: SQLite (reseeded on startup for Render deployment)

Frontend: HTML, CSS, and Vanilla JavaScript

Deployment: Render (using Gunicorn server)

⚙️ Local Setup
To run this project on your local machine, follow these steps:

Clone the repository:

Bash

git clone https://github.com/PixelBot69/intern-assignment.git
cd intern-assignment
Create and activate a virtual environment:

Bash

python -m venv venv
# On Mac/Linux
source venv/bin/activate
# On Windows
venv\Scripts\activate
Install dependencies:

Bash

pip install -r requirements.txt
Run the application:

Bash

python app.py
Once the server is running, you can access the application at http://127.0.0.1:8000.

🌐 Deployment on Render
To deploy this project on Render, connect your repository and configure the following:

Environment Variables: Set the ADMIN_USER and ADMIN_PASS variables for Basic Auth.

Ini, TOML

ADMIN_USER=aryan
ADMIN_PASS=MyStrongPass@123
Build Command: pip install -r requirements.txt

Start Command: gunicorn app:app

📑 API Endpoints
Health
GET /health

JSON

{"status": "ok"}
Profile
GET /profile

Projects (with pagination and filter)
GET /projects?page=1&limit=3
GET /projects?skill=Python&page=1&limit=2

Add Project (Auth required)
POST /projects
Auth: Basic (username and password from environment variables)
Example curl command:

Bash

curl -u aryan:MyStrongPass@123 -X POST https://intern-assignment-y91g.onrender.com/projects \
-H "Content-Type: application/json" \
-d '{"title":"New Project","description":"Test project","skills":["Python","Flask"],"link":"https://github.com/PixelBot69/test"}'
Skills
GET /skills/top

Search
GET /search?q=project

🗄️ Database Schema
Profile Table: id, name, email, education, skills (CSV), github, linkedin, portfolio

Project Table: id, title, description, skills (CSV), link

👤 Candidate Information
Name: Aryan Singh

Email: indianpiear@gmail.com

GitHub: https://github.com/PixelBot69

LinkedIn: https://www.linkedin.com/in/aryan-singh-4b1869249/

Portfolio: https://rayvynai.com/

Resume: https://drive.google.com/file/d/1NYhCRMjTyUYkp40pJ7E3Jp9TvaHOnk3e/view?usp=sharing
