import os
from dotenv import load_dotenv
from datetime import time, datetime

from flask import Flask, render_template, request, flash, redirect, session, g, jsonify
from sqlalchemy.exc import IntegrityError
from sqlalchemy import or_, desc
from werkzeug.utils import secure_filename

from forms import UserForm, LoginForm, LocationForm, ContactForm, ConfStatusForm, ConfigurationForm, TicketStatusForm, TicketPriorityForm, TicketTypeForm, TicketForm, TicketActivityForm
from models import db, connect_db, User, Location, Contact, Conf_status, Configuration, Ticket_status, Ticket_type, Ticket_priority, Ticket, Ticket_activity

from date_convert import from_time, to_time
from email_api import send_mail_ticket, send_mail_activity

CURR_USER_KEY = "curr_user"
UPLOAD_FOLDER = os.getenv('IMAGE_ABS_PATH')
DEFAULT_IMAGE = os.getenv('DEFAULT_IMAGE')

app = Flask(__name__)
app.debug=True

# Get DB_URI from environ variable (useful for production/testing) or,
# if not set there, use development local db.
app.config['SQLALCHEMY_DATABASE_URI'] = (
    os.environ.get('DATABASE_URL', 'postgresql:///itdocs'))

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = True
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', "it's a secret")
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

connect_db(app)
with app.app_context():
    db.create_all()


##############################################################################
# 404 route

@app.errorhandler(404) 
def not_found(e): 
  return render_template("404.html") 

##############################################################################
# User signup/login/logout


@app.before_request
def add_user_to_g():
    """If we're logged in, add curr user to Flask global."""

    if CURR_USER_KEY in session:
        g.user = User.query.get(session[CURR_USER_KEY])

    else:
        g.user = None


def do_login(user):
    """Log in user."""

    session[CURR_USER_KEY] = user.id


def do_logout():
    """Logout user."""

    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]


@app.route('/admin/signup', methods=["GET", "POST"])
def signup():
    """
    Create new user and add to DB. Redirect to home page.
    If form not valid, present form.
    If there already is a user with that username: flash message
    and re-present form.
    """
    if not g.user:
        flash("Login first.", "danger")
        return redirect("/login")
    elif not g.user.is_admin:
        flash("Access unauthorized.", "danger")
        return redirect("/")
    
    form = UserForm()

    if form.validate_on_submit():
        try:
            # Checks if image is uploaded - if there is - saves it with the absolute path
            # but saves relative path to DB
            file = request.files['image_file']
            if file:
                filename = secure_filename(file.filename)
                file_path = os.getenv('IMAGE_ABS_PATH')+filename
                file_abs_path = os.getenv('IMAGE_REL_PATH')+filename
            else:
                file_abs_path = DEFAULT_IMAGE
                
            user = User.signup(
                username=form.username.data,
                password=form.password.data,
                first_name = form.first_name.data,
                last_name = form.last_name.data,
                email=form.email.data,
                image_url= file_abs_path,
                is_admin = form.is_admin.data
            )
            
            db.session.commit()
            if file:
                file.save(file_path)

        except IntegrityError:
            db.session.rollback()
            form.username.errors.append("Username already taken!")
            return render_template('users/signup.html', form=form)


        return redirect("/admin/users")

    else:
        return render_template('users/signup.html', form=form)


@app.route('/login', methods=["GET", "POST"])
def login():
    """Handle user login."""

    form = LoginForm()

    if form.validate_on_submit():
        user = User.authenticate(form.username.data,
                                 form.password.data)

        if user:
            do_login(user)
            flash(f"Hello, {user.username}!", "success")
            return redirect("/")

        flash("Invalid credentials.", 'danger')

    return render_template('users/login.html', form=form)


@app.route('/logout')
def logout():
    """Handle logout of user."""

    do_logout()
    flash('You have logged out successfully!', "success")
    return redirect('/login')


##############################################################################
# General user routes:

@app.route('/admin/users')
def list_users():
    """Page with listing of users.
    Can take a 'q' param in querystring to search by that username, first or last name.
    """
    if not g.user:
        flash("Login first.", "danger")
        return redirect("/login")
    elif not g.user.is_admin:
        flash("Access unauthorized.", "danger")
        return redirect("/")
    
    search = request.args.get('q')

    if not search:
        users = User.query.order_by(User.username).all()
    else:
        users = db.session.query(User).filter(or_(User.first_name.ilike(f"%{search}%"), User.last_name.ilike(f"%{search}%"), 
                                                  User.username.ilike(f"%{search}%"))).order_by(User.username).all()

    return render_template('users/index.html', users=users)


@app.route('/admin/users/<int:user_id>')
def users_show(user_id):
    """Show user profile."""
    if not g.user:
        flash("Login first.", "danger")
        return redirect("/login")
    elif not g.user.is_admin:
        flash("Access unauthorized.", "danger")
        return redirect("/")
    
    user = User.query.get_or_404(user_id)
    
    return render_template('users/detail.html', user=user)




@app.route('/admin/users/<int:user_id>/edit', methods=["GET", "POST"])
def user_edit(user_id):
    """Update profile for current user."""

    if not g.user:
        flash("Login first.", "danger")
        return redirect("/login")
    elif not g.user.is_admin:
        flash("Access unauthorized.", "danger")
        return redirect("/")
    
    user = User.query.get_or_404(user_id)
    form = UserForm(obj=user)
    if form.validate_on_submit():
        try:
            file = request.files['image_file']
            if file:
                filename = secure_filename(file.filename)
                file_path = os.getenv('IMAGE_ABS_PATH')+filename
                file_abs_path = os.getenv('IMAGE_REL_PATH')+filename
            else:
                file_abs_path = user.image_url
            user.username = form.username.data
            user.email = form.email.data
            user.first_name = form.first_name.data
            user.last_name = form.last_name.data
            user.image_url = file_abs_path
            user.is_admin = form.is_admin.data

            db.session.commit()
            if file:
                file.save(file_path)

            return redirect(f'/admin/users/{user.id}')
        except IntegrityError:
            db.session.rollback()
            form.username.errors.append("Username already taken!")
            return render_template('users/signup.html', form=form)
        
    return render_template("/users/edit.html", form=form)


@app.route('/admin/users/<int:user_id>/delete', methods=["POST"])
def delete_user(user_id):
    """Delete user."""

    if not g.user:
        flash("Login first.", "danger")
        return redirect("/login")
    elif not g.user.is_admin:
        flash("Access unauthorized.", "danger")
        return redirect("/")
    
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()

    return redirect("/admin/users")


##########################################################
# App routes

@app.route('/')
def homepage():
    """
    Redirects to dashboard route if user is logged in.
    Else to login page
    """
    if not g.user:
        flash("Login first.", "danger")
        return redirect("/login")
    
    return redirect('/desk')


@app.route('/admin')
def homepage_docs():
    """If user is logged in and admin - shows the settings homepage"""
    if not g.user:
        flash("Login first.", "danger")
        return redirect("/login")
    elif not g.user.is_admin:
        flash("Access unauthorized.", "danger")
        return redirect("/")
    
    return render_template('/admin/home_admin.html')


@app.route('/desk')
def desk_dashboard():
    """Show desk dashboard for logged in users"""
    if not g.user:
        flash("Login first.", "danger")
        return redirect("/")
    
    return render_template('/desk/home_desk.html')

##########################################################
# Locations routes

@app.route('/admin/location')
def locations_list():
    """If user is logged in and admin - shows a page with listing of locations.
    Can take a 'q' param in querystring to search by that name.
    """
    if not g.user:
        flash("Login first.", "danger")
        return redirect("/login")
    elif not g.user.is_admin:
        flash("Access unauthorized.", "danger")
        return redirect("/")
    
    search = request.args.get('q')

    if not search:
        locations = Location.query.order_by(Location.name).all()
    else:
        locations = Location.query.filter(Location.name.ilike(f"%{search}%")).order_by(Location.name).all()

    return render_template('admin/locations_list.html', locations=locations)


@app.route('/admin/location/add', methods=["GET", "POST"])
def location_add():
    """If user is logged in and admin - shows a list and add new locations
    """
    if not g.user:
        flash("Login first.", "danger")
        return redirect("/login")
    elif not g.user.is_admin:
        flash("Access unauthorized.", "danger")
        return redirect("/")
    
    form = LocationForm()

    if form.validate_on_submit():
        try:
            location = Location(
                name=form.name.data,
            )
            db.session.add(location)
            db.session.commit()

        except IntegrityError:
            db.session.rollback()
            form.name.errors.append("Location with the name already exists!")
            return render_template('admin/admin_add.html', form=form, config='location')

        return redirect("/admin/location")

    else:
        return render_template('admin/admin_add.html', form=form, config='location')

   
@app.route('/admin/location/<int:location_id>/edit', methods=["GET", "POST"])
def location_edit(location_id):
    """If user is logged in and admin - shows a page to update a location."""

    if not g.user:
        flash("Login first.", "danger")
        return redirect("/login")
    elif not g.user.is_admin:
        flash("Access unauthorized.", "danger")
        return redirect("/")
    
    location = Location.query.get_or_404(location_id)
    form = LocationForm(obj=location)
    if form.validate_on_submit():
        try:
            location.name = form.name.data
    
            db.session.commit()
            return redirect('/admin/location')
        except IntegrityError:
            db.session.rollback()
            form.name.errors.append("Location with the name already exists!")
            return render_template('/admin/admin_edit.html', form=form, config='location')
        
    return render_template("/admin/admin_edit.html", form=form, config='location')


@app.route('/admin/location/<int:location_id>/delete', methods=["POST"])
def location_delete(location_id):
    """If user is logged in and admin - delete locations."""

    if not g.user:
        flash("Login first.", "danger")
        return redirect("/login")
    elif not g.user.is_admin:
        flash("Access unauthorized.", "danger")
        return redirect("/")
    
    location = Location.query.get_or_404(location_id)
    db.session.delete(location)
    db.session.commit()

    return redirect("/admin/location")
    

##########################################################
# Priority routes

@app.route('/admin/priority')
def priority_list():
    """If user is logged in and admin - shows a page with listing of priority for tickets.
    Can take a 'q' param in querystring to search by that name.
    """
    if not g.user:
        flash("Login first.", "danger")
        return redirect("/login")
    elif not g.user.is_admin:
        flash("Access unauthorized.", "danger")
        return redirect("/")
    
    search = request.args.get('q')

    if not search:
        priority = Ticket_priority.query.order_by(Ticket_priority.name).all()
    else:
        priority = Ticket_priority.query.filter(Ticket_priority.name.ilike(f"%{search}%")).order_by(Ticket_priority.name).all()

    return render_template('admin/priority_list.html', list=priority)


@app.route('/admin/priority/add', methods=["GET", "POST"])
def priority_add():
    """If user is logged in and admin - shows a page to add a new ticket priority
    """
    if not g.user:
        flash("Login first.", "danger")
        return redirect("/login")
    elif not g.user.is_admin:
        flash("Access unauthorized.", "danger")
        return redirect("/")
    
    form = TicketPriorityForm()

    if form.validate_on_submit():
        try:
            priority = Ticket_priority(
                name=form.name.data
            )
            db.session.add(priority)
            db.session.commit()

        except IntegrityError:
            db.session.rollback()
            form.name.errors.append("Ticket priority with the name already exists!")
            return render_template('admin/admin_add.html', form=form, config='priority')

        return redirect("/admin/priority")

    else:
        return render_template('admin/admin_add.html', form=form, config='priority')
    


@app.route('/admin/priority/<int:priority_id>/edit', methods=["GET", "POST"])
def priority_edit(priority_id):
    """If user is logged in and admin - shows a page to update ticket priority."""

    if not g.user:
        flash("Login first.", "danger")
        return redirect("/login")
    elif not g.user.is_admin:
        flash("Access unauthorized.", "danger")
        return redirect("/")
    
    priority = Ticket_priority.query.get_or_404(priority_id)
    form = TicketPriorityForm(obj=priority)
    if form.validate_on_submit():
        try:
            priority.name = form.name.data
            
            db.session.commit()
            return redirect('/admin/priority')
        except IntegrityError:
            db.session.rollback()
            form.name.errors.append("Ticket priority with the name already exists!")
            return render_template('/admin/admin_edit.html', form=form, config='priority')
        
    return render_template("/admin/admin_edit.html", form=form, config='priority')


@app.route('/admin/priority/<int:priority_id>/delete', methods=["POST"])
def priority_delete(priority_id):
    """If user is logged in and admin - delete ticket priorities."""

    if not g.user:
        flash("Login first.", "danger")
        return redirect("/login")
    elif not g.user.is_admin:
        flash("Access unauthorized.", "danger")
        return redirect("/")
    
    priority = Ticket_priority.query.get_or_404(priority_id)
    db.session.delete(priority)
    db.session.commit()

    return redirect("/admin/priority")


##########################################################
# Ticket status routes

@app.route('/admin/ticket_status')
def ticket_status_list():
    """If user is logged in and admin - shows a page with listing of status for ticket.
    Can take a 'q' param in querystring to search by that name.
    """
    if not g.user:
        flash("Login first.", "danger")
        return redirect("/login")
    elif not g.user.is_admin:
        flash("Access unauthorized.", "danger")
        return redirect("/")
    
    search = request.args.get('q')

    if not search:
        ticket_status = Ticket_status.query.order_by(Ticket_status.name).all()
    else:
        ticket_status = Ticket_status.query.filter(Ticket_status.name.ilike(f"%{search}%")).order_by(Ticket_status.name).all()

    return render_template('admin/ticket_status_list.html', list=ticket_status)


@app.route('/admin/ticket_status/add', methods=["GET", "POST"])
def ticket_status_add():
    """If user is logged in and admin - shows a page to add a new ticket status.
    """
    if not g.user:
        flash("Login first.", "danger")
        return redirect("/login")
    elif not g.user.is_admin:
        flash("Access unauthorized.", "danger")
        return redirect("/")
    
    form = TicketStatusForm()

    if form.validate_on_submit():
        try:
            ticket_status = Ticket_status(
                name=form.name.data,
                is_closed=form.is_closed.data
            )
            db.session.add(ticket_status)
            db.session.commit()

        except IntegrityError:
            db.session.rollback()
            form.name.errors.append("Ticket status with the name already exists!")
            return render_template('admin/admin_add.html', form=form, config='ticket status')

        return redirect("/admin/ticket_status")

    else:
        return render_template('admin/admin_add.html', form=form, config='ticket status')
    


@app.route('/admin/ticket_status/<int:ticket_status_id>/edit', methods=["GET", "POST"])
def ticket_status_edit(ticket_status_id):
    """If user is logged in and admin - shows a page to update ticket status."""

    if not g.user:
        flash("Login first.", "danger")
        return redirect("/login")
    elif not g.user.is_admin:
        flash("Access unauthorized.", "danger")
        return redirect("/")
    
    ticket_status = Ticket_status.query.get_or_404(ticket_status_id)
    form = TicketStatusForm(obj=ticket_status)
    if form.validate_on_submit():
        try:
            ticket_status.name = form.name.data
            ticket_status.is_closed = form.is_closed.data
            db.session.commit()
            return redirect('/admin/ticket_status')
        except IntegrityError:
            db.session.rollback()
            form.name.errors.append("Ticket status with the name already exists!")
            return render_template('/admin/admin_edit.html', form=form, config='ticket status')
        
    return render_template("/admin/admin_edit.html", form=form, config='ticket status')


@app.route('/admin/ticket_status/<int:ticket_status_id>/delete', methods=["POST"])
def ticket_status_delete(ticket_status_id):
    """If user is logged in and admin - delete ticket status."""

    if not g.user:
        flash("Login first.", "danger")
        return redirect("/login")
    elif not g.user.is_admin:
        flash("Access unauthorized.", "danger")
        return redirect("/")
    
    ticket_status = Ticket_status.query.get_or_404(ticket_status_id)
    db.session.delete(ticket_status)
    db.session.commit()

    return redirect("/admin/ticket_status")


##########################################################
# Ticket type routes

@app.route('/admin/ticket_type')
def ticket_type_list():
    """If user is logged in and admin - shows a page with listing of type for tickets.
    Can take a 'q' param in querystring to search by that name.
    """
    if not g.user:
        flash("Login first.", "danger")
        return redirect("/login")
    elif not g.user.is_admin:
        flash("Access unauthorized.", "danger")
        return redirect("/")
    
    search = request.args.get('q')

    if not search:
        ticket_type = Ticket_type.query.order_by(Ticket_type.name).all()
    else:
        ticket_type = Ticket_type.query.filter(Ticket_type.name.ilike(f"%{search}%")).order_by(Ticket_type.name).all()

    return render_template('admin/ticket_type_list.html', list=ticket_type)


@app.route('/admin/ticket_type/add', methods=["GET", "POST"])
def ticket_type_add():
    """If user is logged in and admin - shows a page to add new ticket types.
    """
    if not g.user:
        flash("Login first.", "danger")
        return redirect("/login")
    elif not g.user.is_admin:
        flash("Access unauthorized.", "danger")
        return redirect("/")
    
    form = TicketTypeForm()

    if form.validate_on_submit():
        try:
            ticket_type = Ticket_type(
                name=form.name.data
            )
            db.session.add(ticket_type)
            db.session.commit()

        except IntegrityError:
            db.session.rollback()
            form.name.errors.append("Ticket type with the name already exists!")
            return render_template('admin/admin_add.html', form=form, config='ticket type')

        return redirect("/admin/ticket_type")

    else:
        return render_template('admin/admin_add.html', form=form, config='ticket type')
    


@app.route('/admin/ticket_type/<int:ticket_type_id>/edit', methods=["GET", "POST"])
def ticket_type_edit(ticket_type_id):
    """If user is logged in and admin - shows a page to update ticket types."""

    if not g.user:
        flash("Login first.", "danger")
        return redirect("/login")
    elif not g.user.is_admin:
        flash("Access unauthorized.", "danger")
        return redirect("/")
    
    ticket_type = Ticket_type.query.get_or_404(ticket_type_id)
    form = TicketTypeForm(obj=ticket_type)
    if form.validate_on_submit():
        try:
            ticket_type.name = form.name.data
            
            db.session.commit()
            return redirect('/admin/ticket_type')
        except IntegrityError:
            db.session.rollback()
            form.name.errors.append("Ticket type with the name already exists!")
            return render_template('/admin/admin_edit.html', form=form, config='ticket type')
        
    return render_template("/admin/admin_edit.html", form=form, config='ticket type')


@app.route('/admin/ticket_type/<int:ticket_type_id>/delete', methods=["POST"])
def ticket_type_delete(ticket_type_id):
    """If user is logged in and admin - delete ticket type."""

    if not g.user:
        flash("Login first.", "danger")
        return redirect("/login")
    elif not g.user.is_admin:
        flash("Access unauthorized.", "danger")
        return redirect("/")
    
    ticket_type = Ticket_type.query.get_or_404(ticket_type_id)
    db.session.delete(ticket_type)
    db.session.commit()

    return redirect("/admin/ticket_type")

##########################################################
# Configuration status routes

@app.route('/admin/conf_status')
def conf_status_list():
    """If user is logged in and admin - shows a page with listing of status for configurations.
    Can take a 'q' param in querystring to search by that name.
    """
    if not g.user:
        flash("Login first.", "danger")
        return redirect("/login")
    elif not g.user.is_admin:
        flash("Access unauthorized.", "danger")
        return redirect("/")
    
    search = request.args.get('q')

    if not search:
        conf_status = Conf_status.query.order_by(Conf_status.name).all()
    else:
        conf_status = Conf_status.query.filter(Conf_status.name.ilike(f"%{search}%")).order_by(Conf_status.name).all()

    return render_template('admin/conf_status_list.html', list=conf_status)


@app.route('/admin/conf_status/add', methods=["GET", "POST"])
def conf_status_add():
    """If user is logged in and admin - shows a page to add new config status.
    """
    if not g.user:
        flash("Login first.", "danger")
        return redirect("/login")
    elif not g.user.is_admin:
        flash("Access unauthorized.", "danger")
        return redirect("/")
    
    form = ConfStatusForm()

    if form.validate_on_submit():
        try:
            conf_status = Conf_status(
                name=form.name.data
            )
            db.session.add(conf_status)
            db.session.commit()

        except IntegrityError:
            db.session.rollback()
            form.name.errors.append("Configuration status with the name already exists!")
            return render_template('admin/admin_add.html', form=form, config="configuration status")

        return redirect("/admin/conf_status")

    else:
        return render_template('admin/admin_add.html', form=form, config='configuration status')
    


@app.route('/admin/conf_status/<int:conf_status_id>/edit', methods=["GET", "POST"])
def conf_status_edit(conf_status_id):
    """If user is logged in and admin - shows a page to update configuration status."""

    if not g.user:
        flash("Login first.", "danger")
        return redirect("/login")
    elif not g.user.is_admin:
        flash("Access unauthorized.", "danger")
        return redirect("/")
    
    conf_status = Conf_status.query.get_or_404(conf_status_id)
    form = ConfStatusForm(obj=conf_status)
    if form.validate_on_submit():
        try:
            conf_status.name = form.name.data
            
            db.session.commit()
            return redirect('/admin/conf_status')
        except IntegrityError:
            db.session.rollback()
            form.name.errors.append("Configuration status with the name already exists!")
            return render_template('/admin/admin_edit.html', form=form, config='configuration status')
        
    return render_template("/admin/admin_edit.html", form=form, config='configuration status')


@app.route('/admin/conf_status/<int:conf_status_id>/delete', methods=["POST"])
def conf_status_delete(conf_status_id):
    """If user is logged in and admin - delete configuration status."""

    if not g.user:
        flash("Login first.", "danger")
        return redirect("/login")
    elif not g.user.is_admin:
        flash("Access unauthorized.", "danger")
        return redirect("/")
    
    conf_status = Conf_status.query.get_or_404(conf_status_id)
    db.session.delete(conf_status)
    db.session.commit()

    return redirect("/admin/conf_status")


##########################################################
# Configurations routes

@app.route('/admin/configuration')
def configurations_list():
    """If user is logged in and admin - shows a page with listing of configurations.
    Can take a 'q' param in querystring to search by that name.
    """
    if not g.user:
        flash("Login first.", "danger")
        return redirect("/login")
    elif not g.user.is_admin:
        flash("Access unauthorized.", "danger")
        return redirect("/")
    
    search = request.args.get('q')

    if not search:
        configurations = Configuration.query.order_by(Configuration.name).all()
    else:
        configurations = Configuration.query.filter(Configuration.name.ilike(f"%{search}%")).order_by(Configuration.name).all()

    return render_template('admin/configurations_list.html', list=configurations)


@app.route('/admin/configuration/add', methods=["GET", "POST"])
def configurations_add():
    """If user is logged in and admin - shows a page to add new configurations.
    """
    if not g.user:
        flash("Login first.", "danger")
        return redirect("/login")
    elif not g.user.is_admin:
        flash("Access unauthorized.", "danger")
        return redirect("/")
    
    form = ConfigurationForm()
    # Generate choices for select fields. The blank choice is added as the top choice option, and is validated later
    blank_choices = [(0, '')]
    form.contact_id.choices = blank_choices + [(x.id, x.last_name) for x in db.session.query(Contact.id, Contact.last_name).all()]
    form.location_id.choices = blank_choices + [(x.id, x.name) for x in db.session.query(Location.id, Location.name).all()]
    form.status_id.choices = [(x.id, x.name) for x in db.session.query(Conf_status.id, Conf_status.name).all()]

    if form.validate_on_submit():
        try:
            contact_id = form.contact_id.data if form.contact_id.data != 0 else None
            location_id = form.location_id.data if form.location_id.data != 0 else None
            configurations = Configuration(
                name=form.name.data,
                notes=form.notes.data,
                model=form.model.data,
                contact_id=contact_id,
                location_id=location_id,
                status_id=form.status_id.data
            )

            db.session.add(configurations)
            db.session.commit()

        except IntegrityError:
            db.session.rollback()
            form.name.errors.append("Configuration with the name already exists!")
            return render_template('admin/admin_add.html', form=form, config='configuration')

        return redirect("/admin/configuration")

    else:
        return render_template('admin/admin_add.html', form=form, config='configuration')
    


@app.route('/admin/configuration/<int:configuration_id>/edit', methods=["GET", "POST"])
def configuration_edit(configuration_id):
    """If user is logged in and admin - shows a page to update configurations."""

    if not g.user:
        flash("Login first.", "danger")
        return redirect("/login")
    elif not g.user.is_admin:
        flash("Access unauthorized.", "danger")
        return redirect("/")
    
    configuration = Configuration.query.get_or_404(configuration_id)
    form = ConfigurationForm(obj=configuration)

    # Generates choices for select inputs. The blank_choices option is always on top and later validated
    blank_choices = [(0, '')]
    form.contact_id.choices = blank_choices + [(x.id, x.last_name) for x in db.session.query(Contact.id, Contact.last_name).all()]
    form.location_id.choices = blank_choices + [(x.id, x.name) for x in db.session.query(Location.id, Location.name).all()]
    form.status_id.choices = [(x.id, x.name) for x in db.session.query(Conf_status.id, Conf_status.name).all()]


    if form.validate_on_submit():
        try:
            contact_id = form.contact_id.data if form.contact_id.data != 0 else None
            location_id = form.location_id.data if form.location_id.data != 0 else None
            configuration.name = form.name.data
            configuration.notes = form.notes.data
            configuration.model = form.model.data
            configuration.status_id = form.status_id.data
            configuration.location_id = location_id
            configuration.contact_id = contact_id
            
            db.session.commit()
            return redirect('/admin/configuration')
        except IntegrityError:
            db.session.rollback()
            form.name.errors.append("Configuration with the name already exists!")
            return render_template('/admin/admin_edit.html', form=form, config='configuration')
        
    return render_template("/admin/admin_edit.html", form=form, config='configuration')


@app.route('/admin/configuration/<int:configuration_id>/delete', methods=["POST"])
def configuration_delete(configuration_id):
    """If user is logged in and admin - delete configuration."""

    if not g.user:
        flash("Login first.", "danger")
        return redirect("/login")
    elif not g.user.is_admin:
        flash("Access unauthorized.", "danger")
        return redirect("/")
    
    configuration = Configuration.query.get_or_404(configuration_id)
    db.session.delete(configuration)
    db.session.commit()

    return redirect("/admin/configuration")

##########################################################
# Contacts routes

@app.route('/admin/contact')
def contact_list():
    """If user is logged in /admin not required/ shows a page with listing of contacts.
    Can take a 'q' param in querystring to search by that first or last name, and email address.
    """
    if not g.user:
        flash("Login first.", "danger")
        return redirect("/login")
    
    search = request.args.get('q')

    if not search:
        contacts = Contact.query.order_by(Contact.last_name).all()
    else:
        contacts = db.session.query(Contact).filter(or_(Contact.first_name.ilike(f"%{search}%"), Contact.last_name.ilike(f"%{search}%"), 
                                                        Contact.email.ilike(f"%{search}%"))).order_by(Contact.last_name).all()

    return render_template('admin/contacts_list.html', list=contacts)


@app.route('/admin/contact/add', methods=["GET", "POST"])
def contacts_add():
    """If user is logged in /admin not required/ shows a page to add new contacts.
    """
    if not g.user:
        flash("Login first.", "danger")
        return redirect("/login")
    
    form = ContactForm()

    if form.validate_on_submit():
        try:
            contact = Contact(
                first_name=form.first_name.data,
                last_name=form.last_name.data,
                email=form.email.data,
            )
            db.session.add(contact)
            db.session.commit()

        except IntegrityError:
            db.session.rollback()
            form.email.errors.append("Contact with the email address already exists!")
            return render_template('admin/admin_add.html', form=form, config='contact')

        return redirect("/admin/contact")

    else:
        return render_template('admin/admin_add.html', form=form, config='contact')
    


@app.route('/admin/contact/<int:contact_id>/edit', methods=["GET", "POST"])
def contact_edit(contact_id):
    """If user is logged in /admin not required/ shows a page to update a contact entry."""

    if not g.user:
        flash("Login first.", "danger")
        return redirect("/login")
    
    contact = Contact.query.get_or_404(contact_id)
    form = ContactForm(obj=contact)
    if form.validate_on_submit():
        try:
            contact.email = form.email.data
            contact.first_name = form.first_name.data
            contact.last_name = form.last_name.data
            contact.notes = form.notes.data
            db.session.commit()
            return redirect('/admin/contact')
        except IntegrityError:
            db.session.rollback()
            form.email.errors.append("Contact with the email address already exists!")
            return render_template('/admin/admin_edit.html', form=form, config='contact')
        
    return render_template("/admin/admin_edit.html", form=form, config='contact')


@app.route('/admin/contact/<int:contact_id>/delete', methods=["POST"])

def delete_contact(contact_id):
    """If user is logged in /admin not required/ - delete user."""

    if not g.user:
        flash("Login first.", "danger")
        return redirect("/login")
    elif not g.user.is_admin:
        flash("Access unauthorized.", "danger")
        return redirect("/")
    
    contact = Contact.query.get_or_404(contact_id)
    db.session.delete(contact)
    db.session.commit()

    return redirect("/admin/contact")


##########################################################
# Ticket routes

@app.route('/desk/ticket')
def tickets_list():
    """If user is logged in /admin not required/ shows a page with listing of tickets.
    Can take a 'from' and 'to' param in query string to search by that time period.
    """
    if not g.user:
        flash("Login first.", "danger")
        return redirect("/login")
    
    search_from = request.args.get('from')
    search_to = request.args.get('to')

    if search_from and search_to:
        fromdatetime = from_time(search_from)
        todatetime = to_time(search_to)
        tickets = db.session.query(Ticket).filter((Ticket.timestamp.between(fromdatetime, todatetime))).order_by(desc(Ticket.timestamp)).all()
    else:
        tickets = Ticket.query.order_by(desc(Ticket.timestamp)).all()
       

    return render_template('/desk/tickets_list.html', list=tickets)


@app.route('/desk/my_ticket')
def my_tickets_list():
    """If user is logged in /admin not required/ shows a page with listing of the logged in user's tickets.
    """
    if not g.user:
        flash("Login first.", "danger")
        return redirect("/login")
    
    search_from = request.args.get('from')
    search_to = request.args.get('to')

    if search_from and search_to:
        fromdatetime = from_time(search_from)
        todatetime = to_time(search_to)
        tickets = db.session.query(Ticket).filter_by(user_id=g.user.id).filter((Ticket.timestamp.between(fromdatetime, todatetime))).order_by(desc(Ticket.timestamp)).all()
    else:
        tickets = Ticket.query.filter_by(user_id=g.user.id).order_by(desc(Ticket.timestamp)).all()


    return render_template('/desk/tickets_list_my.html', list=tickets)


@app.route('/desk/ticket/add', methods=["GET", "POST"])
def ticket_add():
    """If user is logged in /admin not required/ shows a page to add new tickets.
    """
    if not g.user:
        flash("Login first.", "danger")
        return redirect("/login")

    
    form = TicketForm()
    # Generate choices for select input options - the blank choices are on top and validated when submitted for requried fields.
    blank_choices = [(0, '')]
    form.contact_id.choices = [(x.id, x.last_name) for x in db.session.query(Contact.id, Contact.last_name).all()]
    form.user_id.choices = blank_choices + [(x.id, x.last_name) for x in db.session.query(User.id, User.last_name).all()]
    form.configuration_id.choices = blank_choices + [(x.id, x.name) for x in db.session.query(Configuration.id, Configuration.name).all()]
    form.status_id.choices = [(x.id, x.name) for x in db.session.query(Ticket_status.id, Ticket_status.name).all()]
    form.priority_id.choices = [(x.id, x.name) for x in db.session.query(Ticket_priority.id, Ticket_priority.name).all()]
    form.type_id.choices = [(x.id, x.name) for x in db.session.query(Ticket_type.id, Ticket_type.name).all()]
    

    if form.validate_on_submit():
        user_id = form.user_id.data if form.user_id.data != 0 else None
        configuration_id = form.configuration_id.data if form.configuration_id.data != 0 else None
        ticket = Ticket(
            title=form.title.data,
            notes=form.notes.data,
            status_id=form.status_id.data,
            priority_id=form.priority_id.data,
            type_id=form.type_id.data,
            contact_id=form.contact_id.data,
            user_id=user_id,
            configuration_id=configuration_id
        )

        db.session.add(ticket)
        db.session.commit()
        flash("Ticket successfully created", "success")

        #Send email to assignee and contact
        send_code = send_mail_ticket(ticket)
        
        if send_code == 200:
            msg="info"
            flash(f"Email was sent successfully", msg)
        else:
            ticket.notification_sent = False
            db.session.commit()
            msg="warning"
            flash(f"There was an error sending the email! Please resend", msg)

        return redirect(f"/desk/ticket/{ticket.id}")

    else:
        return render_template('/desk/ticket_add.html', form=form)
    

@app.route('/desk/ticket/<int:ticket_id>')
def ticket_view(ticket_id):
    """If user is logged in /admin not required/ shows a page to view ticket details"""
    if not g.user:
        flash("Login first.", "danger")
        return redirect("/login")

    ticket = Ticket.query.get_or_404(ticket_id)
    return render_template("/desk/ticket_view.html", ticket=ticket)

                           
@app.route('/desk/ticket/<int:ticket_id>/edit', methods=["GET", "POST"])
def ticket_edit(ticket_id):
    """If user is logged in /admin not required/ shows a page to update a ticket."""

    if not g.user:
        flash("Login first.", "danger")
        return redirect("/login")

    
    ticket = Ticket.query.get_or_404(ticket_id)
    form = TicketForm(obj=ticket)
    #Generate select field option choices with a blank option
    blank_choices = [(0, '')]
    form.contact_id.choices = [(x.id, x.last_name) for x in db.session.query(Contact.id, Contact.last_name).all()]
    form.user_id.choices = blank_choices + [(x.id, x.last_name) for x in db.session.query(User.id, User.last_name).all()]
    form.configuration_id.choices = blank_choices + [(x.id, x.name) for x in db.session.query(Configuration.id, Configuration.name).all()]
    form.status_id.choices = [(x.id, x.name) for x in db.session.query(Ticket_status.id, Ticket_status.name).all()]
    form.priority_id.choices = [(x.id, x.name) for x in db.session.query(Ticket_priority.id, Ticket_priority.name).all()]
    form.type_id.choices = [(x.id, x.name) for x in db.session.query(Ticket_type.id, Ticket_type.name).all()]

    if form.validate_on_submit():
        user_id = form.user_id.data if form.user_id.data != 0 else None
        configuration_id = form.configuration_id.data if form.configuration_id.data != 0 else None
        ticket.title=form.title.data,
        ticket.notes=form.notes.data,
        ticket.status_id=form.status_id.data,
        ticket.priority_id=form.priority_id.data,
        ticket.type_id=form.type_id.data,
        ticket.contact_id=form.contact_id.data,
        ticket.user_id=user_id,
        ticket.configuration_id=configuration_id
        db.session.commit()

        #Send email to assignee and contact
        send_code = send_mail_ticket(ticket)
        
        if send_code == 200:
            ticket.notification_sent = True
            db.session.commit()
            msg="info"
            flash(f"Email was sent successfully", msg)
        else:
            ticket.notification_sent = False
            db.session.commit()
            msg="warning"
            flash(f"There was an error sending the email! Please resend", msg)

        return redirect(f'/desk/ticket/{ticket.id}')
    
    return render_template("/desk/ticket_edit.html", form=form)


@app.route('/desk/ticket/<int:ticket_id>/delete', methods=["POST"])
def ticket_delete(ticket_id):
    """If user is logged in /admin not required/ - delete ticket."""

    if not g.user:
        flash("Login first.", "danger")
        return redirect("/login")
    elif not g.user.is_admin:
        flash("Access unauthorized.", "danger")
        return redirect("/")
    
    ticket = Ticket.query.get_or_404(ticket_id)
    db.session.delete(ticket)
    db.session.commit()
    
    return redirect("/desk/ticket")


@app.route('/desk/resend/<int:ticket_id>')
def resend_notification(ticket_id):
    """Shows an option to resend failed notifications"""
    ticket = Ticket.query.get_or_404(ticket_id)
    send_code = send_mail_ticket(ticket)
        
    if send_code == 200:

        msg="info"
    else:
        ticket.notification_sent = False
        db.session.commit()
        msg="warning"
    flash(f"Email was sent with code: {send_code}", msg)

    return redirect(f'/desk/ticket/{ticket.id}')


##########################################################
# Ticket activity routes


@app.route('/desk/ticket/<int:ticket_id>/add-activity', methods=["GET", "POST"])
def ticket_activity_add(ticket_id):
    """If user is logged in /admin not required/ shows a page to add new ticket activity.
    """
    if not g.user:
        flash("Login first.", "danger")
        return redirect("/login")

    
    form = TicketActivityForm()

    form.user_id.choices = [(x.id, x.last_name) for x in db.session.query(User.id, User.last_name).all()]
    
    if form.validate_on_submit():
        ticket_activity = Ticket_activity(
            notes=form.notes.data,
            user_id=form.user_id.data,
            time_spent=form.time_spent.data,
            ticket_id=ticket_id
        )

        db.session.add(ticket_activity)
        db.session.commit()
        
        #Send email to assignee and contact
        send_code = send_mail_activity(ticket_activity)
        
        if send_code == 200:
            msg="info"
            flash(f"Email sent successfully.", msg)
        else:
            ticket_activity.notification_sent = False
            db.session.commit()
            msg="warning"
            flash(f"There was an error sending the email! Please resend", msg)


        return redirect(f"/desk/ticket/{ticket_id}")

    else:
        return render_template('/desk/ticket_activity_add.html', form=form)
    

@app.route('/desk/ticket_activity/<int:activity_id>/edit', methods=["GET", "POST"])
def ticket_activity_edit(activity_id):
    """If user is logged in /admin not required/ shows a page to edit ticket activity.
    """
    if not g.user:
        flash("Login first.", "danger")
        return redirect("/login")

    activity = Ticket_activity.query.get_or_404(activity_id)
    form = TicketActivityForm(obj=activity)

    user_choices = (db.session.query(User.id, User.first_name).all())
    form.user_id.choices = [(x.id, x.first_name) for x in user_choices]
    

    if form.validate_on_submit():
        ticket_activity = Ticket_activity.query.get_or_404(activity_id)
        ticket_activity.notes=form.notes.data,
        ticket_activity.user_id=form.user_id.data,
        ticket_activity.time_spent=form.time_spent.data
        
        db.session.commit()

        #Send email to assignee and contact
        send_code = send_mail_activity(ticket_activity)
        
        if send_code == 200:
            ticket_activity.notification_sent = True
            db.session.commit()
            msg="info"
            flash(f"Email sent successfully.", msg)
        else:
            ticket_activity.notification_sent = False
            db.session.commit()
            msg="warning"
            flash(f"There was an error sending the email! Please resend", msg)


        return redirect(f"/desk/ticket/{ticket_activity.ticket.id}")

    else:
        return render_template('/desk/ticket_activity_edit.html', form=form)


@app.route('/desk/ticket_activity/<int:activity_id>/delete', methods=["POST"])
def ticket_activity_delete(activity_id):
    """If user is logged in /admin not required/ shows a page to delete ticket activity."""

    if not g.user:
        flash("Login first.", "danger")
        return redirect("/login")
    elif not g.user.is_admin:
        flash("Access unauthorized.", "danger")
        return redirect("/")
    
    ticket_activity = Ticket_activity.query.get_or_404(activity_id)
    print(ticket_activity.ticket.id)
    db.session.delete(ticket_activity)
    db.session.commit()

    return redirect(f"/desk/ticket/{ticket_activity.ticket.id}")

@app.route('/desk/resend-activity/<int:activity_id>')
def resend_activity_notification(activity_id):
    "Shows an option to resend ticket activity notification if failed"
    activity = Ticket_activity.query.get_or_404(activity_id)
    send_code = send_mail_activity(activity)
        
    if send_code == 200:
        msg="info"
        activity.notification_sent = True
        db.session.commit()
        flash(f"Email sent successfully.", msg)
    else:
        activity.notification_sent = False
        db.session.commit()
        msg="warning"
        flash(f"There was an error sending the email! Please resend", msg)

    return redirect(f'/desk/ticket/{activity.ticket.id}')

###############################################################
# Get chart statistics routes
@app.route('/desk/stats')
def ticket_stats():
    """Get ticket stats for tickets YTD to plot the dashbaord charts.
    If admin - returns all tickets. If not admin user is logged in - returns only the user's tickets.
    Returns the list of tickets in JSON for the chart.js file."""
    if not g.user:
        flash("Login first.", "danger")
        return redirect("/login")
    
    first_current = datetime.replace(datetime.now(), month=1, day=1)
    ytd = datetime.combine(first_current, time.min)

    if g.user.is_admin:
        tickets = Ticket.query.filter(Ticket.timestamp <= datetime.now()).filter(Ticket.timestamp >= ytd).all()
    else:
        tickets = Ticket.query.filter(Ticket.user_id == g.user.id).filter(Ticket.timestamp <= datetime.now()).filter(Ticket.timestamp >= ytd).all()

    data = [ticket.serialize() for ticket in tickets]
        
    return jsonify(data)