# 🚀 Fernando’s Dev Log

![Python](https://img.shields.io/badge/Python-3.14-3776AB?logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-Web_App-black?logo=flask&logoColor=white)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-ORM-red)
![Auth](https://img.shields.io/badge/Auth-Login_System-blue)
![Security](https://img.shields.io/badge/Security-CSRF%20%2B%20Hashing-red)

### Full-stack Flask blog application with authentication, database relationships, and admin-controlled content management. 

---
## 🧩 Why I built this

I built this project to move beyond static websites and understand how real web applications work behind the scenes.

Instead of just rendering content, this app handles:

- User authentication

- Database relationships

- Dynamic content creation

- Secure form handling

The goal was to shift from thinking in pages to thinking in systems.

---

## 🚀 Features
- 🔐 User authentication system

   - Register / Login / Logout

   - Password hashing with Werkzeug

- 📝 Admin-controlled blog system

  - Create, edit, delete posts

  - Restricted to admin user

- 💬 Comment system

  - Authenticated users can comment

  - Linked to both users and posts

- 🗄 Database integration (SQLAlchemy ORM)

  - Users ↔ Posts ↔ Comments relationships

  - Automatic table creation

- 📩 Contact form with email delivery

  - Sends messages via SMTP (Gmail TLS)

  - Flash messaging for UX feedback

- 🛡 Security features

  - CSRF protection on forms

  - Password hashing

  - Protected routes

- 🎨 Frontend

  - Bootstrap UI

  - Jinja templating

  - Reusable components (header/footer)

---

## 🧠 What I learned

- Designing relational database models (users, posts, comments)

- Structuring a Flask application using reusable templates

- Integrating external APIs into a web application

- Handling form submissions in Flask

- Managing configuration with environment variables

- Handling authentication and session management

- Securing routes and forms (CSRF, hashing)

- Building full CRUD functionality

- Structuring a real Flask application

- Deploying a production-ready app using Gunicorn

---

## 🛠 Tech stack
- Python

- Flask

- Flask-Login

- Flask-WTF

- Flask-SQLAlchemy

- SQLAlchemy

- Werkzeug

- Bootstrap 5

- Gunicorn

- SMTP (email handling)

- python-dotenv

---

## 📁 Project structure

    flask-dev-log/
    ├── main.py
    ├── forms.py
    ├── Procfile
    ├── .env.example
    ├── .gitignore
    ├── requirements.txt
    ├── README.md
    ├── templates/
    └── static/

---

## ⚙️ How to run
1) Clone the repository:

        git clone https://github.com/fernandogrh/flask-dev-log.git

2) Navigate into the project folder:

         cd flask-dev-log

3) Create and activate a virtual environment:

   **Windows:**
                                       
         python -m venv .venv
         .\.venv\Scripts\activate

   **Mac/Linux:**

         python3 -m venv .venv
         source .venv/bin/activate

4) Install dependencies:

         pip install -r requirements.txt

5) Set up environment variables:

   **Create a .env file and add:**

         EMAIL_ADDRESS=your_email
         
         EMAIL_PASSWORD=your_app_password
         
         SECRET_KEY=your_secret_key
         
         DATABASE_URI=your_database_url

6) Run the application:

         python main.py

7) Open in browser:

         http://127.0.0.1:5000/

### Notes on credentials

This project uses Gmail SMTP. Use a Gmail App Password (not your normal password).

## Credits

UI theme based on Start Bootstrap – Clean Blog

Images used on the site are sourced from BusinessCraft, Verpex, Pngtree, and Schoolbag (credited in the footer)

## 🚀 Deployment

This app is production-ready and can be deployed using Gunicorn.

## 👨‍💻 Author

**Fernando Ramirez** - Backend development learner focused on Python and web applications.

[GitHub](https://github.com/fernandogrh)