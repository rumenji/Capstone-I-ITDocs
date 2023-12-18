from datetime import datetime

from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy

bcrypt = Bcrypt()
db = SQLAlchemy()

########################################################
# User models


class User(db.Model):
    """User in the system."""

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
        default="/static/images/default-pic.png",
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
    def signup(cls, username, first_name, last_name, email, password, image_url):
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
    __tablename__ = "locations"
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Text, nullable = False)


class Contact(db.Model):
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
        unique=True,
    )

    notes = db.Column(db.Text)

    location_id = db.Column(db.Integer, db.ForeignKey('locations.id', ondelete='SET NULL'))

    location = db.relationship('Location')

########################################################
# Configuration models

class Conf_status(db.Model):
    __tablename__ = "conf_statuses"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(
        db.Text,
        nullable = False
    )


class Configuration(db.Model):
    __tablename__ = "configurations"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(
        db.Text,
        nullable = False
    )
    notes = db.Column(db.Text)
    model = db.Column(db.Text)
    status_id = db.Column(db.Integer, db.ForeignKey('conf_statuses.id', ondelete='SET NULL'))
    location_id = db.Column(db.Integer, db.ForeignKey('locations.id', ondelete='SET NULL'))
    contact_id = db.Column(db.Integer, db.ForeignKey('contacts.id', ondelete='SET NULL'))

    status = db.relationship('Conf_status')
    location = db.relationship('Location')
    contact = db.relationship('Contact')

########################################################
# Ticket models

class Ticket_status(db.Model):
    __tablename__ = "ticket_statuses"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(
        db.Text,
        nullable = False
    )
    is_closed = db.Column(db.Boolean, nullable=False, default=False)

class Ticket_type(db.Model):
    __tablename__ = "ticket_types"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(
        db.Text,
        nullable = False
    )

class Ticket_priority(db.Model):
    __tablename__ = "ticket_priorities"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(
        db.Text,
        nullable = False
    )

class Ticket(db.Model):
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

    status = db.relationship('Ticket_status')
    contact = db.relationship('Contact')
    user = db.relationship('User')
    type = db.relationship('Ticket_type')
    priority = db.relationship('Ticket_priority')
    configuration = db.relationship('Configuration')
    ticket_activities = db.relationship('Ticket_activity', cascade="all, delete-orphan")

    @property
    def friendly_date(self):

        return self.timestamp.strftime("%b %-d  %Y, %-I:%M %p")
    
    def serialize(self):
        return {
            'id': self.id,
            'status': self.status.is_closed,
            'user': self.user.full_name,
            'timestamp': self.timestamp
        }

class Ticket_activity(db.Model):
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
    
    ticket = db.relationship('Ticket')
    user = db.relationship('User')

    @property
    def friendly_date(self):

        return self.timestamp.strftime("%b %-d  %Y, %-I:%M %p")



def connect_db(app):
    """Connect this database to provided Flask app.

    You should call this in your Flask app.
    """

    db.app = app
    db.init_app(app)