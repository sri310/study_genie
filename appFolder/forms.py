from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectMultipleField, widgets,TextAreaField
from wtforms.validators import DataRequired,Length,Email, EqualTo

class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()

class LoginForm(FlaskForm):
    username = StringField('Username',validators=[DataRequired(),Length(min=2, max=20)])
    password = PasswordField('Password', validators = [DataRequired()])
    submit = SubmitField('Log in')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    school_year = StringField('School year', validators=[DataRequired(), Length(min=2, max=20)])
    gpa = StringField('GPA', validators=[DataRequired(), Length(min=1, max=4)])
    string_of_files = ['Sub1\r\nSub2\r\nSub3\r\n']
    list_of_files = string_of_files[0].split()
    # create a list of value/description tuples
    files = [(x, x) for x in list_of_files]
    courses = MultiCheckboxField('Courses/ Areas of Interest', choices=files)
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

class CreatePostForm(FlaskForm):
    subject = StringField('Subject', validators=[DataRequired(), Length(min=2, max=20)])
    title = StringField('Title', validators=[DataRequired(), Length(min=2, max=100)])
    content = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Create')

class UpdatePostForm(FlaskForm):
    subject = StringField('Subject', validators=[DataRequired(), Length(min=2, max=20)])
    title = StringField('Title', validators=[DataRequired(), Length(min=2, max=100)])
    content = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Update')