from flask import Flask, render_template, request, abort
import requests
import datetime
import smtplib
import os
from dotenv import load_dotenv
load_dotenv()

EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
BLOG_API_URL = os.getenv("BLOG_API_URL")

response = requests.get(BLOG_API_URL)
data = response.json()

app = Flask(__name__)

@app.context_processor
def inject_year():
    return {"year":datetime.datetime.now().year}

@app.route("/")
def home():
    return render_template("index.html", data=data)

@app.route("/<int:post_id>")
def post(post_id):
    for post in data:
        if post["id"] == post_id:
            return render_template("post.html", post=post)
    abort(404)

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/contact", methods=["POST", "GET"])
def contact():
    msg = None
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        phone_number = request.form["phone"]
        message = request.form["message"]
        msg = f"Message successfully sent"
        with smtplib.SMTP("smtp.gmail.com", 587) as connection:
            connection.starttls()
            connection.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            connection.sendmail(from_addr=EMAIL_ADDRESS, to_addrs=EMAIL_ADDRESS, msg=f"Subject: Client contact.\n\nContact details:\nName: {name}\nEmail: {email}\nPhone number: {phone_number}\nMessage: {message}".encode("utf-8"))
    return render_template("contact.html", msg=msg)



if __name__ =="__main__":
    app.run(debug=True)


