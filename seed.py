from app import app
from models import db, User, Contact, Location, Conf_status, Configuration, Ticket_status, Ticket_priority, Ticket_type, Ticket, Ticket_activity
import datetime
"""
Seeds the DB with all tables except users. Users will need to be created manually beforehand.
Doesn't drop all tables because it will also delete all user entries.
"""


with app.app_context():
    engine = db.engine
    # db.drop_all()
    Ticket_activity.__table__.drop(engine)
    Ticket.__table__.drop(engine)
    Ticket_priority.__table__.drop(engine)
    Ticket_status.__table__.drop(engine)
    Ticket_type.__table__.drop(engine)
    Configuration.__table__.drop(engine)
    Conf_status.__table__.drop(engine)
    Contact.__table__.drop(engine)
    Location.__table__.drop(engine)

    db.create_all()


########################################################
# User models
    
# u1 = User.signup(
#     email = "testapp1234@test.com",
#     username = "admin",
#     first_name = "User",
#     last_name = "Admin",
#     password = "testtest",
#     image_url= None,
#     is_admin = True
# )

# u2 = User.signup(
#     email = "testapp1235@test.com",
#     username = "user2",
#     first_name = "User",
#     last_name = "Two",
#     password = "testtest",
#     image_url= None,
#     is_admin = False
# )

# u3 = User.signup(
#     email = "testapp1236@test.com",
#     username = "user3",
#     first_name = "User",
#     last_name = "Three",
#     password = "testtest",
#     image_url= None,
#     is_admin = False
# )

# u4 = User.signup(
#     email = "testapp1237@test.com",
#     username = "user4",
#     first_name = "User",
#     last_name = "Four",
#     password = "testtest",
#     image_url= None,
#     is_admin = False
# )


# with app.app_context():
#     db.session.add_all([u1, u2, u3, u4])
#     db.session.commit()

########################################################
# Generic models
    
l1 = Location(
    name = 'External'
)

l2 = Location(
    name = 'Marketing'
)

l3 = Location(
    name = 'HR'
)

l4 = Location(
    name = 'Development'
)

l5 = Location(
    name = 'IT'
)

with app.app_context():
    db.session.add_all([l1, l2, l3, l4, l5])
    db.session.commit()


c1 = Contact(
    first_name = "John",
    last_name = "Smith",
    email = "contact1234@test.com",
    location_id = 1
)

c2 = Contact(
    first_name = "Maria",
    last_name = "Watson",
    email = "contact1235@test.com",
    location_id = 2
)

c3 = Contact(
    first_name = "Dave",
    last_name = "Johnson",
    email = "contact1236@test.com",
    location_id = 3
)

c4 = Contact(
    first_name = "Jacob",
    last_name = "Chavez",
    email = "contact1237@test.com",
    location_id = 4
)

c5 = Contact(
    first_name = "Stephen",
    last_name = "Beeler",
    email = "contact1238@test.com",
    location_id = 5
)

c6 = Contact(
    first_name = "Rodney",
    last_name = "Simpson",
    email = "contact1239@test.com",
    location_id = 1
)

c7 = Contact(
    first_name = "Amit",
    last_name = "Casal",
    email = "contact1244@test.com",
    location_id = 4
)

c8 = Contact(
    first_name = "Mark",
    last_name = "Davidson",
    email = "contact1254@test.com",
    location_id = 1
)

with app.app_context():
    db.session.add_all([c1, c2, c3, c4, c5, c6, c7, c8])
    db.session.commit()


########################################################
# Configuration models
    
cs1 = Conf_status(
    name = "Active"
)

cs2 = Conf_status(
    name = "Inactive"
)

with app.app_context():
    db.session.add_all([cs1, cs2])
    db.session.commit()

conf1 = Configuration(
    name="SonicWall",
    model="TZ370",
    notes="Company firewall in IT network rack",
    status_id = 1,
    location_id = 2
)

conf6 = Configuration(
    name="Netgear",
    model="24port",
    notes="Company switch in IT network rack",
    status_id = 1,
    location_id = 2
)

conf2 = Configuration(
    name="Old SonicWall",
    model="TZ300",
    notes="Old company firewall in IT network rack",
    status_id = 2,
    location_id = 2
)

conf3 = Configuration(
    name="Ricoh",
    model="C2006",
    notes="Company copier",
    status_id = 1,
    location_id = 2
)

conf4 = Configuration(
    name="PC1",
    model="Dell",
    notes="Desktop 1",
    status_id = 1,
    location_id = 3
)

conf5 = Configuration(
    name="PC2",
    model="Dell",
    notes="Desktop 2",
    status_id = 1,
    location_id = 4
)

with app.app_context():
    db.session.add_all([conf1, conf2, conf3, conf4, conf5, conf6])
    db.session.commit()

########################################################
# Ticket models
    
ts1 = Ticket_status(
    name="New"
)

ts2 = Ticket_status(
    name="In progress"
)

ts3 = Ticket_status(
    name="Closed",
    is_closed = True
)

with app.app_context():
    db.session.add_all([ts1, ts2, ts3])
    db.session.commit()

tt1 = Ticket_type(
    name="Incident"
)

tt2 = Ticket_type(
    name="Question"
)

tt3 = Ticket_type(
    name="Service",
)

with app.app_context():
    db.session.add_all([tt1, tt2, tt3])
    db.session.commit()

tp1 = Ticket_priority(
    name="Low"
)

tp2 = Ticket_priority(
    name="Medium"
)

tp3 = Ticket_priority(
    name="High",
)

with app.app_context():
    db.session.add_all([tp1, tp2, tp3])
    db.session.commit()

t1 = Ticket(
    title="Perform maintenance on Desktop 2",
    notes = "Time for scheduled maintenance",
    timestamp = datetime.datetime(2023, 1, 2, 7, 43, 0, 668420),
    notification_sent = True,
    status_id = 3,
    priority_id = 1,
    type_id = 1,
    user_id = 4,
    contact_id = 4,
    configuration_id = 5
)

t2 = Ticket(
    title="Update Netgear switch",
    notes = "New update released",
    timestamp = datetime.datetime(2023, 1, 23, 7, 12, 0, 668420),
    notification_sent = True,
    status_id = 3,
    priority_id = 2,
    type_id = 2,
    user_id = 2,
    configuration_id = 2
)

t3 = Ticket(
    title="Update SonicWall",
    notes = "New update released",
    timestamp = datetime.datetime(2023, 1, 23, 11, 42, 0, 668420),
    notification_sent = True,
    status_id = 3,
    priority_id = 2,
    type_id = 2,
    user_id = 2,
    contact_id = 2,
    configuration_id = 1
)

t4 = Ticket(
    title="Perform maintenance on Desktop 2",
    notes = "Time for scheduled maintenance",
    timestamp = datetime.datetime(2023, 3, 2, 7, 43, 0, 668420),
    notification_sent = True,
    status_id = 3,
    priority_id = 1,
    type_id = 1,
    user_id = 4,
    contact_id = 4,
    configuration_id = 5
)

t5 = Ticket(
    title="Update Netgear switch",
    notes = "New update released",
    timestamp = datetime.datetime(2023, 3, 3, 11, 12, 0, 668420),
    notification_sent = True,
    status_id = 3,
    priority_id = 2,
    type_id = 2,
    user_id = 2,
    configuration_id = 2
)

t6 = Ticket(
    title="Update SonicWall",
    notes = "New update released",
    timestamp = datetime.datetime(2023, 3, 23, 11, 42, 0, 668420),
    notification_sent = True,
    status_id = 3,
    priority_id = 2,
    type_id = 2,
    user_id = 2,
    contact_id = 2,
    configuration_id = 1
)

t7 = Ticket(
    title="Perform maintenance on Desktop 2",
    notes = "Time for scheduled maintenance",
    timestamp = datetime.datetime(2023, 6, 2, 7, 42, 0, 668420),
    notification_sent = True,
    status_id = 3,
    priority_id = 1,
    type_id = 1,
    user_id = 4,
    contact_id = 4,
    configuration_id = 5
)

t8 = Ticket(
    title="Perform maintenance on Desktop 2",
    notes = "Time for scheduled maintenance",
    timestamp = datetime.datetime(2023, 6, 2, 7, 43, 0, 668420),
    notification_sent = True,
    status_id = 3,
    priority_id = 1,
    type_id = 1,
    user_id = 4,
    contact_id = 4,
    configuration_id = 5
)

t9 = Ticket(
    title="Update SonicWall",
    notes = "New update released",
    timestamp = datetime.datetime(2023, 6, 23, 11, 42, 0, 668420),
    notification_sent = True,
    status_id = 3,
    priority_id = 2,
    type_id = 2,
    user_id = 2,
    contact_id = 2,
    configuration_id = 1
)

t10 = Ticket(
    title="Update Netgear switch",
    notes = "New update released",
    timestamp = datetime.datetime(2023, 8, 3, 11, 12, 0, 668420),
    notification_sent = True,
    status_id = 3,
    priority_id = 2,
    type_id = 2,
    user_id = 2,
    contact_id = 4,
    configuration_id = 2
)

t11 = Ticket(
    title="Ricoh not printing",
    notes = "Error message out of paper",
    timestamp = datetime.datetime(2023, 8, 19, 16, 43, 0, 668420),
    notification_sent = False,
    status_id = 3,
    priority_id = 1,
    type_id = 1,
    user_id = 1,
    contact_id = 1,
    configuration_id = 2
)

t12 = Ticket(
    title="Perform maintenance on Desktop 2",
    notes = "Time for scheduled maintenance",
    timestamp = datetime.datetime(2023, 9, 2, 7, 43, 0, 668420),
    notification_sent = True,
    status_id = 3,
    priority_id = 1,
    type_id = 1,
    user_id = 4,
    contact_id = 4,
    configuration_id = 5
)

t13 = Ticket(
    title="Desktop 1 not turning on",
    notes = "No signs of power",
    timestamp = datetime.datetime(2023, 10, 11, 19, 22, 0, 668420),
    notification_sent = True,
    status_id = 3,
    priority_id = 3,
    type_id = 1,
    user_id = 3,
    contact_id = 3,
    configuration_id = 4
)

t14 = Ticket(
    title="Update SonicWall",
    notes = "New update released",
    timestamp = datetime.datetime(2023, 11, 23, 11, 42, 0, 668420),
    notification_sent = True,
    status_id = 3,
    priority_id = 2,
    type_id = 2,
    user_id = 2,
    contact_id = 2,
    configuration_id = 1
)

t15 = Ticket(
    title="Ricoh not printing",
    notes = "Error message out of toner",
    timestamp = datetime.datetime(2023, 12, 19, 16, 43, 0, 668420),
    notification_sent = False,
    status_id = 2,
    priority_id = 1,
    type_id = 1,
    user_id = 1,
    contact_id = 1,
    configuration_id = 2
)

t16 = Ticket(
    title="Update Netgear switch",
    notes = "New update released",
    timestamp = datetime.datetime(2023, 12, 20, 7, 12, 0, 668420),
    notification_sent = True,
    status_id = 1,
    priority_id = 2,
    type_id = 2,
    configuration_id = 2
)

t17 = Ticket(
    title="Perform maintenance on Desktop 2",
    notes = "Time for scheduled maintenance",
    timestamp = datetime.datetime(2023, 12, 20, 7, 43, 0, 668420),
    notification_sent = True,
    status_id = 1,
    priority_id = 1,
    type_id = 1,
    contact_id = 4,
    configuration_id = 5
)

with app.app_context():
    db.session.add_all([t1,t2,t3,t4,t5,t6,t7,t8,t9,t10,t11,t12,t13,t14,t15,t16,t17])
    db.session.commit()


ta1 = Ticket_activity(
    notes = "Installed available updates, performed maintenance",
    timestamp = datetime.datetime(2023, 1, 3, 7, 43, 0, 668420),
    notification_sent = True,
    ticket_id = 1,
    user_id = 4,
    time_spent = 0.75
)

ta2 = Ticket_activity(
    notes = "Installed available updates",
    timestamp = datetime.datetime(2023, 1, 23, 8, 1, 0, 668420),
    notification_sent = True,
    ticket_id = 2,
    user_id = 2,
    time_spent = 0.75
)

ta3 = Ticket_activity(
    notes = "Installed available updates",
    timestamp = datetime.datetime(2023, 1, 24, 6, 42, 0, 668420),
    notification_sent = True,
    ticket_id = 3,
    user_id = 3,
    time_spent = 0.75
)

ta4 = Ticket_activity(
    notes = "Installed available updates, performed maintenance",
    timestamp = datetime.datetime(2023, 3, 2, 7, 53, 0, 668420),
    notification_sent = True,
    ticket_id = 4,
    user_id = 4,
    time_spent = 2.25
)

ta5 = Ticket_activity(
    notes = "Installed available updates",
    timestamp = datetime.datetime(2023, 3, 3, 11, 59, 0, 668420),
    notification_sent = True,
    ticket_id = 5,
    user_id = 2,
    time_spent = 2.25
)

ta6 = Ticket_activity(
    notes = "Installed available updates",
    timestamp = datetime.datetime(2023, 3, 23, 23, 42, 0, 668420),
    notification_sent = True,
    ticket_id = 6,
    user_id = 2,
    time_spent = 2.25
)

ta7 = Ticket_activity(
    notes = "Installed available updates, performed maintenance",
    timestamp = datetime.datetime(2023, 6, 2, 7, 52, 0, 668420),
    notification_sent = True,
    ticket_id = 7,
    user_id = 4,
    time_spent = 2.25
)

ta8 = Ticket_activity(
    notes = "Installed available updates",
    timestamp = datetime.datetime(2023, 6, 2, 7, 59, 0, 668420),
    notification_sent = True,
    ticket_id = 8,
    user_id = 4,
    time_spent = 0.75
)

ta9 = Ticket_activity(
    notes = "Installed available updates",
    timestamp = datetime.datetime(2023, 6, 23, 22, 42, 0, 668420),
    notification_sent = True,
    ticket_id = 9,
    user_id = 5,
    time_spent = 0.75
)

ta10 = Ticket_activity(
    notes = "Installed available updates",
    timestamp = datetime.datetime(2023, 8, 3, 23, 42, 0, 668420),
    notification_sent = True,
    ticket_id = 10,
    user_id = 2,
    time_spent = 0.75
)

ta11 = Ticket_activity(
    notes = "Loaded more paper",
    timestamp = datetime.datetime(2023, 8, 19, 16, 46, 0, 668420),
    notification_sent = True,
    ticket_id = 11,
    user_id =1,
    time_spent = 0.25
)

ta12 = Ticket_activity(
    notes = "Performed maintenance",
    timestamp = datetime.datetime(2023, 9, 2, 7, 53, 0, 668420),
    notification_sent = True,
    ticket_id = 12,
    user_id =4,
    time_spent = 0.75
)

ta13 = Ticket_activity(
    notes = ", Checked power outlet, performed maintenance",
    timestamp = datetime.datetime(2023, 10, 11, 19, 25, 0, 668420),
    notification_sent = True,
    ticket_id = 13,
    user_id =3,
    time_spent = 0.75
)

ta14 = Ticket_activity(
    notes = "Installed available updates",
    timestamp = datetime.datetime(2023, 11, 23, 23, 2, 0, 668420),
    notification_sent = True,
    ticket_id = 14,
    user_id = 2,
    time_spent = 1.25
)

ta15 = Ticket_activity(
    notes = "Installed new toner",
    timestamp = datetime.datetime(2023, 12, 19, 16, 46, 0, 668420),
    notification_sent = True,
    ticket_id = 15,
    user_id = 1,
    time_spent = 0.25
)


with app.app_context():
    db.session.add_all([ta1,ta2,ta3,ta4,ta5,ta6,ta7,ta8,ta9,ta10,ta11,ta12,ta13,ta14,ta15])
    db.session.commit()