from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, BooleanField, SubmitField, SelectField
from wtforms.validators import DataRequired, Email, Length, EqualTo, Regexp


class LoginForm(FlaskForm):
    identifier = StringField(
        'Email or Username',
        validators=[DataRequired(), Length(min=3, max=120)]
    )
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember me')
    submit = SubmitField('Login')


class RegistrationForm(FlaskForm):
    username = StringField(
        'Username',
        validators=[
            DataRequired(),
            Length(min=4, max=16),
            Regexp(r'^[A-Za-z0-9_]+$', message='Letters, numbers and _ only')
        ]
    )
    email = StringField(
        'Email',
        validators=[DataRequired(), Email()]
    )
    password = PasswordField(
        'Password',
        validators=[
            DataRequired(),
            Length(min=8, max=16),
            Regexp(
              r'(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])',
              message='Must include upper, lower, digit & special'
            )
        ]
    )
    confirm_password = PasswordField(
        'Confirm Password',
        validators=[
            DataRequired(),
            EqualTo('password', message='Passwords must match')
        ]
    )
    department_id = SelectField(
        'Department',
        coerce=int,
        validators=[DataRequired()]
    )
    submit = SubmitField('Register')


class TicketForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(max=120)])
    description = TextAreaField('Description', validators=[DataRequired()])
    status = SelectField(
        'Status',
        choices=[('Open', 'Open'), ('In Progress', 'In Progress'), ('Closed', 'Closed')],
        default='Open'
    )
    assigned_to = SelectField('Assign to', coerce=int)
    submit = SubmitField('Submit')


class CommentForm(FlaskForm):
    comment = TextAreaField(
        'Comment',
        validators=[DataRequired(), Length(min=1, max=500)]
    )
    submit = SubmitField('Post Comment')

class UserAdminForm(FlaskForm):
    role = SelectField('Role', choices=[('user', 'User'), ('admin', 'Admin')])
    department_id = SelectField('Department', coerce=int)
    submit = SubmitField('Update')
