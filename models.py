from datetime import datetime

from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy

"""
Models for all relations
"""

bcrypt = Bcrypt()
db = SQLAlchemy()

########################################################
# User models


class User(db.Model):
    """
    Users in the system.
    Uses Bcrypt to encrypt the user password.
    Includes a signup method to create a new user, and authenticate method to authenticate while logging in.
    """

    __tablename__ = 'users'

    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement = True
    )

    email = db.Column(
        db.Text,
        nullable=False,
        unique=True,
    )

    username = db.Column(
        db.Text,
        nullable=False,
        unique=True,
    )

    first_name = db.Column(
        db.Text,
        nullable = False
    )

    last_name = db.Column(
        db.Text,
        nullable = False
    )

    image_url = db.Column(
        db.Text,
        default="/static/images/default-pic.png"
    )


    password = db.Column(
        db.Text,
        nullable=False,
    )

    is_admin = db.Column(
        db.Boolean,
        nullable=False,
        default=False
    )


    def __repr__(self):
        return f"<User #{self.id}: {self.username}, {self.email}>"

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    @classmethod
    def signup(cls, username, first_name, last_name, email, password, image_url, is_admin):
        """Sign up user.

        Hashes password and adds user to system.
        """

        hashed_pwd = bcrypt.generate_password_hash(password).decode('UTF-8')

        user = User(
            username=username,
            email=email,
            first_name=first_name,
            last_name=last_name,
            password=hashed_pwd,
            image_url=image_url,
            is_admin=is_admin
        )
        
        db.session.add(user)
        return user

    @classmethod
    def authenticate(cls, username, password):
        """Find user with `username` and `password`.

        This is a class method (call it on the class, not an individual user.)
        It searches for a user whose password hash matches this password
        and, if it finds such a user, returns that user object.

        If can't find matching user (or if password is wrong), returns False.
        """

        user = cls.query.filter_by(username=username).first()

        if user:
            is_auth = bcrypt.check_password_hash(user.password, password)
            if is_auth:
                return user

        return False
    

    
########################################################
# Generic models

class Location(db.Model):
    """Locations entries - to be used with contacts and configurations"""
    __tablename__ = "locations"
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Text, nullable = False, unique=True)


class Contact(db.Model):
    """External or internal contacts that need assistance"""
    __tablename__ = "contacts"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(
        db.Text,
        nullable = False
    )

    last_name = db.Column(
        db.Text,
        nullable = False
    )

    email = db.Column(
        db.Text,
        nullable=False,
        unique=True
    )

    notes = db.Column(db.Text)

    location_id = db.Column(db.Integer, db.ForeignKey('locations.id', ondelete='SET NULL'))

    location = db.relationship('Location', backref="contacts")

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'

########################################################
# Configuration models

class Conf_status(db.Model):
    """Status for the configuration - for example 'active' or 'inactive'"""

    __tablename__ = "conf_statuses"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(
        db.Text,
        nullable = False,
        unique = True
    )


class Configuration(db.Model):
    """Configurations - devices, software, anything that the helpdesk can assist with"""

    __tablename__ = "configurations"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(
        db.Text,
        nullable = False,
        unique = True
    )
    notes = db.Column(db.Text)
    model = db.Column(db.Text)
    status_id = db.Column(db.Integer, db.ForeignKey('conf_statuses.id', ondelete='SET NULL'))
    location_id = db.Column(db.Integer, db.ForeignKey('locations.id', ondelete='SET NULL'))
    contact_id = db.Column(db.Integer, db.ForeignKey('contacts.id', ondelete='SET NULL'))

    status = db.relationship('Conf_status', backref="configurations")
    location = db.relationship('Location', backref="configurations")
    contact = db.relationship('Contact', backref="configurations")

########################################################
# Ticket models

class Ticket_status(db.Model):
    """Ticket status options - for example 'New', 'In progress', 'Closed'"""

    __tablename__ = "ticket_statuses"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(
        db.Text,
        nullable = False,
        unique = True
    )
    is_closed = db.Column(db.Boolean, nullable=False, default=False)

class Ticket_type(db.Model):
    """Ticket type options - for example 'Incident', 'Service'"""

    __tablename__ = "ticket_types"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(
        db.Text,
        nullable = False,
        unique = True
    )

class Ticket_priority(db.Model):
    """Ticket priority options - for example 'Low', 'High'"""

    __tablename__ = "ticket_priorities"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(
        db.Text,
        nullable = False,
        unique = True
    )

class Ticket(db.Model):
    """
    Ticket model - has a title and notes. The user can be assigned during ticket creation. Contact is required.
    The timestamp is automatic to current datetime.
    """
    __tablename__ = "tickets"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(
        db.Text,
        nullable = False
    )
    notes = db.Column(db.Text, nullable = False)
    timestamp = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.now(),
    )
    notification_sent = db.Column(db.Boolean, default=True)
    status_id = db.Column(db.Integer, db.ForeignKey('ticket_statuses.id', ondelete='SET NULL'))
    priority_id = db.Column(db.Integer, db.ForeignKey('ticket_priorities.id', ondelete='SET NULL'))
    type_id = db.Column(db.Integer, db.ForeignKey('ticket_types.id', ondelete='SET NULL'))
    contact_id = db.Column(db.Integer, db.ForeignKey('contacts.id', ondelete='SET NULL'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='SET NULL'))
    configuration_id = db.Column(db.Integer, db.ForeignKey('configurations.id', ondelete='SET NULL'))

    status = db.relationship('Ticket_status', backref="ticket")
    contact = db.relationship('Contact', backref="ticket")
    user = db.relationship('User', backref="ticket")
    type = db.relationship('Ticket_type')
    priority = db.relationship('Ticket_priority', backref="ticket")
    configuration = db.relationship('Configuration', backref="ticket")
    ticket_activities = db.relationship('Ticket_activity', backref="ticket", cascade="all, delete-orphan")

    @property
    def friendly_date(self):

        return self.timestamp.strftime("%b %-d  %Y, %-I:%M %p")
    
    def serialize(self):
        """
        Returns ticket data in format that is JSON serializable
        to be used to plot the charts for the dashboard
        """
        user = self.user.full_name if self.user else 'Not Assigned'
        return {
            'id': self.id,
            'status': self.status.is_closed,
            'user': user,
            'timestamp': self.timestamp
        }

class Ticket_activity(db.Model):
    """Ticket activity model - has a time_spent column to calculate time spent for each ticket"""
    __tablename__ = "ticket_activities"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    notes = db.Column(db.Text, nullable = False)
    timestamp = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow(),
    )
    notification_sent = db.Column(db.Boolean, default=True)
    time_spent = db.Column(db.Numeric(precision = 10, scale = 2), nullable = False)
    ticket_id = db.Column(db.Integer, db.ForeignKey('tickets.id', ondelete='CASCADE'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='SET NULL'))
    
    user = db.relationship('User', backref="ticket_activities")

    @property
    def friendly_date(self):

        return self.timestamp.strftime("%b %-d  %Y, %-I:%M %p")



def connect_db(app):
    """Connect this database to provided Flask app.
    """

    db.app = app
    db.init_app(app)