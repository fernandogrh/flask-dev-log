from markupsafe import Markup
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, EmailField, PasswordField, TelField
from wtforms.validators import DataRequired, URL, Email
from flask_ckeditor import CKEditorField


class NewPost(FlaskForm):
    title = StringField("Blog Post Title", validators=[DataRequired()])
    subtitle = StringField("Subtitle", validators=[DataRequired()])
    image_url = StringField("Blog Post Image URL", validators=[DataRequired(), URL()])
    body = CKEditorField("Blog Post Content", validators=[DataRequired()])
    submit_button = SubmitField("Submit Post")

class ContactForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    email = EmailField("Email Address", validators=[DataRequired(), Email()])
    phone = TelField("Phone Number", validators=[DataRequired()])
    message = TextAreaField("Message", validators=[DataRequired()])
    submit_button = SubmitField("SEND")

class RegisterForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    email = EmailField("Email Address", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Register")

class LoginForm(FlaskForm):
    email = EmailField("Email Address", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Login")

class CommentForm(FlaskForm):
    label_for_comment = Markup("<strong>Comment</strong>")
    comment = TextAreaField(label_for_comment, validators=[DataRequired()])
    submit = SubmitField("Submit Comment")

