from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, DecimalField, TextAreaField, BooleanField, SelectField, FileField
from wtforms.validators import DataRequired, Email, Length, ValidationError
from models import User, Contact, Location, Ticket_priority, Ticket_status, Ticket_type, Conf_status, Configuration
from werkzeug.utils import secure_filename
"""Generate forms for the models. Uses validation to check inputs for required data"""

#############################################
#User forms

# Allowed extensions for images
ALLOWED_EXTENSIONS = ('jpg', 'png')

class UserForm(FlaskForm):
    """Form for adding users."""
        
    def allowed_extensions(form, field):
        """Validates allowed file extensions"""
        if field.raw_data:
            filename = secure_filename(field.data.filename)
            if filename:
                if not filename.endswith(ALLOWED_EXTENSIONS):
                    raise ValidationError('Only .jpg and .png files are allowed!')

    username = StringField('Username*', validators=[DataRequired()])
    first_name = StringField('First Name*', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    email = StringField('E-mail*', validators=[DataRequired(), Email()])
    password = PasswordField('Password*', validators=[Length(min=6)])
    image_file = FileField('Profile Image', validators=[allowed_extensions])
    is_admin = BooleanField('Has Admin Permissions')

class LoginForm(FlaskForm):
    """Login form."""

    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[Length(min=6)])

#############################################
#Generic forms

class LocationForm(FlaskForm):
    """Form for adding locations."""
            
    name = StringField('Name*', validators=[DataRequired()])

class ContactForm(FlaskForm):
    """Form for adding contacts."""
            
    first_name = StringField('First Name*', validators=[DataRequired()])
    last_name = StringField('Last Name*', validators=[DataRequired()])
    email = StringField('E-mail*', validators=[DataRequired(), Email()])
    notes = TextAreaField('Notes')

#############################################
#Configuration forms

class ConfStatusForm(FlaskForm):
    """Form for adding configuration statuses."""

    name = StringField('Name*', validators=[DataRequired()])

class ConfigurationForm(FlaskForm):
    """Form for adding configurations."""
            
    name = StringField('Name*', validators=[DataRequired()])
    model = StringField('Model')
    notes = TextAreaField('Notes')
    status_id = SelectField('Status*', coerce=int)
    contact_id = SelectField('Contact', coerce=int)
    location_id = SelectField('Location', coerce=int)

#############################################
#Ticket forms

class TicketStatusForm(FlaskForm):
    """Form for adding ticket statuses."""

    name = StringField('Name*', validators=[DataRequired()])
    is_closed = BooleanField('Marks ticket as closed')

class TicketPriorityForm(FlaskForm):
    """Form for adding ticket priorities."""
            
    name = StringField('Name*', validators=[DataRequired()])

class TicketTypeForm(FlaskForm):
    """Form for adding ticket types."""

    name = StringField('Name*', validators=[DataRequired()])

class TicketForm(FlaskForm):
    """Form for adding tickets."""

    title = StringField('Title*', validators=[DataRequired()])
    notes = TextAreaField('Notes', validators=[DataRequired()])
    status_id = SelectField('Status*', coerce=int, validators=[DataRequired()])
    priority_id = SelectField('Priority*', coerce=int, validators=[DataRequired()])
    type_id = SelectField('Type*', coerce=int, validators=[DataRequired()])
    user_id = SelectField('Assignee', coerce=int)
    contact_id = SelectField('Contact*', coerce=int, validators=[DataRequired()])
    configuration_id = SelectField('Configuration', coerce=int)

class TicketActivityForm(FlaskForm):
    """Form for adding ticket activites."""
    
    notes = TextAreaField('Notes*', validators=[DataRequired()])
    time_spent = DecimalField('Time spent*', validators=[DataRequired()])
    user_id = SelectField('Assignee*', coerce=int, validators=[DataRequired()])