![Python](https://img.shields.io/badge/Python-3.14-3776AB?logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-Web_App-black?logo=flask&logoColor=white)
![Jinja](https://img.shields.io/badge/Jinja-Templating-B41717)
![Bootstrap](https://img.shields.io/badge/Bootstrap-5-7952B3?logo=bootstrap&logoColor=white)
![Requests](https://img.shields.io/badge/Requests-HTTP_Client-2B5B84)
![SMTP](https://img.shields.io/badge/SMTP-Email_Service-orange)

# 🚀Fernando’s Dev Log

### A Flask-powered development blog that renders posts from an external API and includes a working contact form with SMTP email delivery.

## 🧩 Why I built this

The goal was to understand how a server-side web application works beyond static pages. The application renders blog posts from an **external API**, uses reusable **Jinja templates**, and includes a **working contact form** that sends emails via **SMTP**.

## 🧠 What I learned

- structuring a Flask application using reusable templates
- integrating external APIs into a web application
- handling form submissions in Flask
- managing configuration with environment variables

## 🚀 Features
- Home page that lists blog posts (loaded from an **external JSON API**)
- Dynamic post pages using URL parameters (`/<int:post_id>`)
- About page with personal story + direction
- Contact form that sends emails via SMTP (Gmail TLS)
- Reusable templates via `{% include %}` (header/footer)
- Current year injected globally with a Flask context processor

## 🛠 Tech stack
- Python + Flask
- Jinja templating
- Requests (API calls)
- SMTP (email sending)
- python-dotenv (environment variables)
- Bootstrap theme (Start Bootstrap)

## 📁 Project structure

    flask-dev-log/
    ├── main.py
    ├── templates/
    │ ├── index.html
    │ ├── post.html
    │ ├── about.html
    │ ├── contact.html
    │ ├── header.html
    │ └── footer.html
    ├── static/
    │ ├── css/
    │ ├── js/
    │ └── assets/
    ├── .env.example
    ├── .gitignore
    ├── requirements.txt
    └── README.md


## ⚙️ Setup
1) Install dependencies:

        pip install -r requirements.txt

2) Create your environment file:

        Copy .env.example
        
        Rename it to .env
        
        Fill in your credentials

3) Run the app:

        python main.py

4) Open:
 
       http://127.0.0.1:5000/

### Notes on credentials

This project uses Gmail SMTP. Use a Gmail App Password (not your normal password).

## Credits

UI theme based on Start Bootstrap – Clean Blog

Images used on the site are sourced from BusinessCraft, Verpex, Pngtree, and Schoolbag (credited in the footer)

## 👨‍💻Author

**Fernando Ramirez** - Backend development learner focused on Python and web applications.

[GitHub](https://github.com/fernandogrh)