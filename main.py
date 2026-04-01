from flask import Flask, render_template, abort, redirect, url_for, flash
from flask_bootstrap import Bootstrap5
from datetime import date, datetime
import smtplib
import os
from dotenv import load_dotenv
from flask_ckeditor import CKEditor
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Integer, String, Text, Date
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from forms import NewPost, ContactForm, RegisterForm, LoginForm, CommentForm
from flask_login import UserMixin, login_user, LoginManager, current_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from flask_wtf.csrf import CSRFProtect

load_dotenv()

EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
SECRET_KEY = os.getenv("SECRET_KEY")
DATABASE_URI = os.getenv("DATABASE_URI")

if not all([EMAIL_ADDRESS, EMAIL_PASSWORD, SECRET_KEY, DATABASE_URI]):
    raise Exception("Missing one or more environment variables")

def admin_only(func):
    @wraps(func)
    def is_user_admin(*args, **kwargs):
        if not current_user.is_authenticated or current_user.id != 1:
            return abort(403)
        return func(*args, **kwargs)
    return is_user_admin

app = Flask(__name__)
app.config["SECRET_KEY"] = SECRET_KEY
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
bootstrap = Bootstrap5(app)
ckeditor = CKEditor(app)
csrf = CSRFProtect(app)

class Base(DeclarativeBase):
    pass

app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
db = SQLAlchemy(model_class=Base)
db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

class User(UserMixin, db.Model):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(100), nullable=False)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    posts = relationship("Post", back_populates="author", cascade="all, delete-orphan")
    comments = relationship("Comment", back_populates="comment_author", cascade="all, delete-orphan")

class Post(db.Model):
    __tablename__ = "posts"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    author_id: Mapped[int] = mapped_column(Integer, db.ForeignKey("users.id"))
    author = relationship("User", back_populates="posts")
    title: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    subtitle: Mapped[str] = mapped_column(String(250), nullable=False)
    date: Mapped[date] = mapped_column(Date, nullable=False)
    body: Mapped[str] = mapped_column(Text, nullable=False)
    image_url: Mapped[str] = mapped_column(String(250), nullable=False)
    comments = relationship("Comment", back_populates="parent_post", cascade="all, delete-orphan")

class Comment(db.Model):
    __tablename__ = "comments"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    author_id: Mapped[int] = mapped_column(Integer, db.ForeignKey("users.id"))
    comment_author = relationship("User", back_populates="comments")
    post_id: Mapped[int] = mapped_column(Integer, db.ForeignKey("posts.id"))
    parent_post = relationship("Post", back_populates="comments")
    text: Mapped[str] = mapped_column(Text, nullable=False)

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))

with app.app_context():
    db.create_all()

@app.context_processor
def inject_year():
    return {"year": datetime.now().year}

@app.route("/")
def home():
    all_posts = db.session.execute(db.select(Post).order_by(Post.date.desc())).scalars().all()
    return render_template("index.html", data=all_posts)

@app.route("/post/<int:post_id>", methods=["GET", "POST"])
def show_post(post_id):
    post = db.session.get(Post, post_id)
    if not post:
        abort(404)
    comment_form = CommentForm()
    if comment_form.validate_on_submit():
        if not current_user.is_authenticated:
            flash("You need to login or register to comment.")
            return redirect(url_for("login"))
        new_comment = Comment(text=comment_form.comment.data, comment_author=current_user, parent_post=post)
        db.session.add(new_comment)
        db.session.commit()
        return redirect(url_for("show_post", post_id=post_id))
    return render_template("post.html", post=post, form=comment_form)

@app.route("/delete-comment/<int:comment_id>", methods=["POST"])
@admin_only
def delete_comment(comment_id):
    comment_to_delete = db.session.get(Comment, comment_id)
    if not comment_to_delete:
        abort(404)
    post_id = comment_to_delete.parent_post.id
    db.session.delete(comment_to_delete)
    db.session.commit()
    return redirect(url_for("show_post", post_id=post_id))

@app.route("/new-post", methods=["GET", "POST"])
@admin_only
def new_post():
    new_post_form = NewPost()
    if new_post_form.validate_on_submit():
        post_to_add = Post(title=new_post_form.title.data, subtitle=new_post_form.subtitle.data, author=current_user, image_url=new_post_form.image_url.data, date=date.today(), body=new_post_form.body.data)
        db.session.add(post_to_add)
        db.session.commit()
        return redirect(url_for("home"))
    return render_template("create_post.html", form=new_post_form)

@app.route("/edit-post/<int:post_id>", methods=["GET", "POST"])
@admin_only
def edit_post(post_id):
    post_to_edit = db.session.get(Post, post_id)
    if  not post_to_edit:
        abort(404)
    edit_post_form = NewPost(
        title=post_to_edit.title,
        subtitle=post_to_edit.subtitle,
        image_url=post_to_edit.image_url,
        body=post_to_edit.body
    )
    if edit_post_form.validate_on_submit():
        post_to_edit.title = edit_post_form.title.data
        post_to_edit.subtitle = edit_post_form.subtitle.data
        post_to_edit.body = edit_post_form.body.data
        post_to_edit.image_url = edit_post_form.image_url.data
        db.session.commit()
        return redirect(url_for("show_post", post_id=post_id))
    return render_template("create_post.html", form=edit_post_form, post=post_to_edit)

@app.route("/delete-post/<int:post_id>", methods=["POST"])
@admin_only
def delete_post(post_id):
    post_to_delete = db.session.get(Post, post_id)
    if not post_to_delete:
        abort(404)
    db.session.delete(post_to_delete)
    db.session.commit()
    return redirect(url_for("home"))

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/contact", methods=["GET", "POST"])
def contact():
    contact_form = ContactForm()
    if contact_form.validate_on_submit():
        try:
            with smtplib.SMTP("smtp.gmail.com", 587) as connection:
                connection.starttls()
                connection.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
                connection.sendmail(from_addr=EMAIL_ADDRESS, to_addrs=EMAIL_ADDRESS, msg=f"Subject: Client contact.\n\nContact details:\nName: {contact_form.name.data}\nEmail: {contact_form.email.data}\nPhone number: {contact_form.phone.data}\nMessage: {contact_form.message.data}".encode("utf-8"))
                flash("Message successfully sent")
                return redirect(url_for("contact"))
        except smtplib.SMTPException:
            flash("Sorry, your message could not be sent. Please try again later.")
            return redirect(url_for("contact"))
    return render_template("contact.html", form=contact_form)

@app.route("/register", methods=["GET", "POST"])
def register():
    register_form = RegisterForm()
    if register_form.validate_on_submit():
        email = db.session.execute(db.select(User).where(User.email == register_form.email.data)).scalar()
        if email:
            flash("You have already signed up with that email, please log in instead.")
            return redirect(url_for('login'))
        hash_and_salted_password = generate_password_hash(register_form.password.data, method='pbkdf2:sha256',
                                                          salt_length=8)
        new_user = User(name=register_form.name.data, email=register_form.email.data, password=hash_and_salted_password)
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        return redirect(url_for("home"))
    return render_template("register.html", form=register_form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    login_form = LoginForm()
    if login_form.validate_on_submit():
        user = db.session.execute(db.select(User).where(User.email == login_form.email.data)).scalar()
        if not user:
            flash("That email does not exist, please try again.")
            return redirect(url_for('login'))
        elif not check_password_hash(user.password, login_form.password.data):
            flash('Password incorrect, please try again.')
            return redirect(url_for('login'))
        else:
            login_user(user)
            return redirect(url_for('home'))
    return render_template("login.html", form=login_form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for("home"))

if __name__ == "__main__":
    app.run()
