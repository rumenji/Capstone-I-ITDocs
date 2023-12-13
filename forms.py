from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, DecimalField, TextAreaField, BooleanField, SelectField
from wtforms.validators import DataRequired, Email, Length

#############################################
#User forms

class UserForm(FlaskForm):
    """Form for adding users."""

    username = StringField('Username*', validators=[DataRequired()])
    first_name = StringField('First Name*', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    email = StringField('E-mail*', validators=[DataRequired(), Email()])
    password = PasswordField('Password*', validators=[Length(min=6)])
    image_url = StringField('Image URL')
    is_admin = BooleanField('Has Admin Permissions')

class LoginForm(FlaskForm):
    """Login form."""

    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[Length(min=6)])

#############################################
#Generic forms

class LocationForm(FlaskForm):

    name = StringField('Name*', validators=[DataRequired()])

class ContactForm(FlaskForm):

    first_name = StringField('First Name*', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    email = StringField('E-mail*', validators=[DataRequired(), Email()])
    notes = TextAreaField('Notes')

#############################################
#Configuration forms

class ConfStatusForm(FlaskForm):

    name = StringField('Name*', validators=[DataRequired()])

class ConfigurationForm(FlaskForm):

    name = StringField('Name*', validators=[DataRequired()])
    model = StringField('Model')
    notes = TextAreaField('Notes')
    status_id = SelectField('Status*', coerce=int)
    contact_id = SelectField('Contact', coerce=int)
    location_id = SelectField('Location', coerce=int)

#############################################
#Ticket forms

class TicketStatusForm(FlaskForm):

    name = StringField('Name*', validators=[DataRequired()])

class TicketPriorityForm(FlaskForm):

    name = StringField('Name*', validators=[DataRequired()])

class TicketTypeForm(FlaskForm):

    name = StringField('Name*', validators=[DataRequired()])

class TicketForm(FlaskForm):

    title = StringField('Title*', validators=[DataRequired()])
    notes = TextAreaField('Notes', validators=[DataRequired()])
    status_id = SelectField('Status*', coerce=int, validators=[DataRequired()])
    priority_id = SelectField('Priority*', coerce=int, validators=[DataRequired()])
    type_id = SelectField('Type*', coerce=int, validators=[DataRequired()])
    user_id = SelectField('Assignee', coerce=int, validators=[DataRequired()])
    contact_id = SelectField('Contact*', coerce=int, validators=[DataRequired()])
    configuration_id = SelectField('Configuration', coerce=int, validators=[DataRequired()])
    location_id = SelectField('Location', coerce=int, validators=[DataRequired()])

class TicketActivityForm(FlaskForm):

    notes = TextAreaField('Notes*', validators=[DataRequired()])
    time_spent = DecimalField('Time spent*', validators=[DataRequired()])
    user_id = SelectField('Assignee*', coerce=int, validators=[DataRequired()])