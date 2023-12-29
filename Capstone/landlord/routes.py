from flask import Blueprint, render_template, redirect, url_for, request, session, flash
from flask import current_app as app
from flask_session import Session
from ..db import db
from ..models import Landlord, Unit, Expense
from datetime import datetime, timedelta
import secrets
from ..utils.password_hash import hash_password
from ..utils.inputblacklist import sanitize_input
from ..utils.date_scan import scan_units
from ..utils.random_gen import generate_random_string
from datetime import timedelta
import pyotp


# Blueprint for landlord
landlord_bp = Blueprint(
    'landlord_bp', __name__,
    template_folder='templates',
    static_folder='static'
)


def generate_totp_uri(username):
    # Generate a random TOTP secret
    totp_secret = pyotp.random_base32()

    # Create a TOTP instance
    totp = pyotp.TOTP(totp_secret)

    # Generate the provisioning URI
    provisioning_uri = totp.provisioning_uri(name=username, issuer_name="MACK")

    return provisioning_uri, totp_secret


# Add this constant to define the session timeout period (in seconds)
SESSION_TIMEOUT = 20
SESSION_TYPE = 'filesystem'
app.config.from_object(__name__)
Session(app)


@app.before_request
def check_session_timeout():
    last_activity = session.get('last_activity')
    print("app before req")
    print(last_activity)

    if last_activity is not None and datetime.utcnow() > last_activity + timedelta(seconds=SESSION_TIMEOUT):
        # Log out the user if the session has timed out
        session.clear()
        flash('Session has timed out due to inactivity. Please log in again.', 'error')
        return redirect(url_for('home_bp.home'))


def check_credentials(username, password):
    landlord = Landlord.query.filter_by(username=username).first()
    if not landlord:
        return False, None, None  # Add a placeholder for totp_secret
    if landlord.password == password:
        return True, landlord.id, landlord.secret_key
    else:
        return False, None, None


def get_totp_secret(landlord_id):
    landlord = Landlord.query.get(landlord_id)
    if landlord:
        return True, landlord.id, landlord.secret_key
    else:
        return False, None, None


@landlord_bp.route('/landlord', methods=['GET', 'POST'])
def landlord_redirect():
    # if user is logged in, redirect to user profile page
    # else, redirect to landlord login page
    pass


@landlord_bp.route('/landlord/login', methods=['GET', 'POST'])
def landlord_login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        try:
            sanitize_input(password, username)
        except ValueError as e:
            error_message = f"Invalid credentials: {str(e)}"
            return render_template('landlord_login.html', error_message=error_message)

        # Check if the user exists in the database
        user_exists, landlord_id, totp_secret = check_credentials(username, hash_password(password))

        if user_exists:
            # Prompt the user for OTP during login
            return render_template('landlord_otp.html', landlord_id=landlord_id)

        else:
            # User does not exist or incorrect credentials, show an error message
            error_message = "Invalid credentials. Please try again."
            flash(error_message, 'error')
            return render_template('landlord_login.html', error_message=error_message)

    # Render the login page for GET requests
    return render_template('landlord_login.html')


@landlord_bp.route('/landlord/otp', methods=['POST'])
def landlord_otp():
    landlord_id = request.form.get('landlord_id')
    otp_number = request.form.get('OTP')

    # Retrieve the TOTP secret for the given landlord_id from the database
    _, _, totp_secret = get_totp_secret(landlord_id)

    totp = pyotp.TOTP(totp_secret)
    is_valid_otp = totp.verify(otp_number)

    if is_valid_otp:
        print("in valid otp")
        # OTP is valid, proceed with regular login
        session['landlord_id'] = landlord_id
        session['last_activity'] = datetime.utcnow()
        print(landlord_id, "aadd")
        return redirect(url_for('landlord_bp.landlord_profile', landlord_id=landlord_id))
    else:
        # Invalid OTP, show an error message
        error_message = "Invalid OTP. Please try again."
        return render_template('landlord_login.html', error_message=error_message)


@landlord_bp.route('/landlord/setup_totp', methods=['GET', 'POST'])
def setup_totp():
    totp_uri = request.args.get('totp_uri')
    # Retrieve the TOTP secret from the session
    totp_secret = session.get('totp_secret')

    if not totp_secret:
        # Redirect to the login page if TOTP secret is not available
        return redirect(url_for('landlord_bp.landlord_login'))

    if request.method == 'POST':
        otp_number = request.form.get('OTP')
        session['last_activity'] = datetime.utcnow()
        # Verify the provided OTP against the TOTP secret
        totp = pyotp.TOTP(totp_secret)
        is_valid_otp = totp.verify(otp_number)

        if is_valid_otp:
            # OTP is valid, you can proceed with whatever action is needed
            # (e.g., store the fact that TOTP is set up for this user)
            session.clear()
            return redirect(url_for('landlord_bp.landlord_login'))
        else:
            # Invalid OTP, render the setup_totp page with an error message
            error_message = "Invalid OTP. Please try again."
            return render_template('landlord_setup_totp.html', totp_secret=totp_secret, totp_uri=totp_uri)

    # Render the TOTP setup page with the QR code
    return render_template('landlord_setup_totp.html', totp_secret=totp_secret, totp_uri=totp_uri)


@landlord_bp.route('/landlord/signup', methods=['GET', 'POST'])
def landlord_signup():
    if request.method == 'POST':
        f_name = request.form.get('f_name')
        l_name = request.form.get('l_name')
        phonenumber = request.form.get('phonenumber')
        email = request.form.get('email')
        username = request.form.get('username')
        password = request.form.get('password')
        confirmpassword = request.form.get('confirmpassword')

        try:
            sanitize_input(password, username)
        except ValueError as e:
            error_message = f"Invalid credentials: {str(e)}"
            return redirect(url_for('landlord_bp.landlord_signup', error_message=error_message))

        secured_password = hash_password(password)
        secured_ConfirmPassword = hash_password(confirmpassword)

        if secured_password != secured_ConfirmPassword:
            error_message = "Password does not match"
            flash(error_message, 'error')
            return redirect(url_for('landlord_bp.landlord_signup'))

        # Generate TOTP information during signup
        totp_uri, totp_secret = generate_totp_uri(username)

        new_landlord = Landlord(
            first_name=f_name,
            last_name=l_name,
            phone_number=phonenumber,
            email=email,
            username=username,
            password=secured_password,
            secret_key=totp_secret  # Store TOTP secret in the database
        )

        db.session.add(new_landlord)
        db.session.commit()

        session['totp_secret'] = totp_secret

        # Redirect to the login page with TOTP URI
        return redirect(url_for('landlord_bp.setup_totp', totp_uri=totp_uri))

    return render_template('LandlordSignUp.html')


@landlord_bp.route('/landlord/<int:landlord_id>', methods=['GET','POST'])
def landlord_profile(landlord_id):
    logged_in_landlord_id = session.get('landlord_id')

    # Check if the logged-in landlord is authorized to view the requested profile
    if logged_in_landlord_id is None or int(logged_in_landlord_id) != landlord_id:
        print("Doesnt match the landlord id")
        flash('You are not authorized to view this profile.', 'error')
        session.clear()
        return redirect(url_for('home_bp.home'))

    # render landlord profile page with units table
    landlord = Landlord.query.filter_by(id=landlord_id).first()
    if request.method == 'POST':
        f_name = request.form.get('f_name')
        l_name = request.form.get('l_name')
        phonenumber = request.form.get('phonenumber')
        email = request.form.get('email')

        landlord.first_name = f_name
        landlord.last_name = l_name
        landlord.phone_number = phonenumber
        landlord.email = email

        db.session.commit()

        redirect(url_for('landlord_bp.landlord_profile', landlord_id=landlord.id))
    else:
        # render landlord profile page with units table
        units = landlord.units
        return render_template('landlord_profile.html', landlord=landlord, units=units)


@landlord_bp.route('/landlord/<int:landlord_id>/tenants', methods=['GET'])
def landlord_tenants(landlord_id):
    logged_in_landlord_id = session.get('landlord_id')

    # Check if the logged-in landlord is authorized to view the requested profile
    if logged_in_landlord_id is None or logged_in_landlord_id != landlord_id:
        flash('You are not authorized to view this profile.', 'error')
        session.clear()
        return redirect(url_for('landlord_bp.home'))
    landlord = Landlord.query.filter_by(id=landlord_id).first()
    units = landlord.units
    tenants = []
    for unit in units:
        tenants.extend(unit.tenants)
    
    return render_template('landlord_tenants.html', landlord=landlord, tenants=tenants, units=units)


@landlord_bp.route('/landlord/<int:landlord_id>/<int:unit_id>', methods=['GET', 'POST'])
def landlord_unit_page(landlord_id, unit_id):
    logged_in_landlord_id = session.get('landlord_id')
    print(logged_in_landlord_id)

    # Check if the logged-in landlord is authorized to view the requested profile
    if logged_in_landlord_id is None or logged_in_landlord_id != landlord_id:
        flash('You are not authorized to view this profile.', 'error')
        session.clear()
        return redirect(url_for('home_bp.home'))
    # render landlord unit page for a given unit
    landlord=Landlord.query.filter_by(id=landlord_id).first()
    unit=Unit.query.filter_by(id=unit_id).first()
    if request.method == 'POST':
        unit_number = request.form.get('unit_number')
        address = request.form.get('address')
        rent = request.form.get('rent') if request.form.get('rent') else None
        lease_start = request.form.get('lease_start') if request.form.get('lease_start') else None
        rent_due = request.form.get('rent_due') if request.form.get('rent_due') else None

        if request.form.get('rent_this_unit_hidden'):
            tenant_password = generate_random_string()
        else:
            tenant_password = None

        unit.unit_number = unit_number
        unit.address = address
        unit.rent = rent
        unit.lease_start = lease_start
        unit.rent_due = rent_due
        unit.tenant_password = tenant_password

        db.session.commit()
    
    

    return render_template('landlord_unit_page.html', landlord=landlord, unit=unit)


@landlord_bp.route('/landlord/<int:landlord_id>/<int:unit_id>/expenses', methods=['GET'])
def landlord_unit_expenses(landlord_id, unit_id):
    logged_in_landlord_id = session.get('landlord_id')

    # Check if the logged-in landlord is authorized to view the requested profile
    if logged_in_landlord_id is None or logged_in_landlord_id != landlord_id:
        flash('You are not authorized to view this profile.', 'error')
        session.clear()
        return redirect(url_for('home_bp.home'))
    # render expenses for given unit
    landlord=Landlord.query.filter_by(id=landlord_id).first()
    unit=Unit.query.filter_by(id=unit_id).first()
    expenses=unit.expenses

    return render_template('landlord_unit_expenses.html', landlord=landlord, unit=unit, expenses=expenses)


@landlord_bp.route('/landlord/<int:landlord_id>/<int:unit_id>/payments', methods=['GET'])
def landlord_unit_payments(landlord_id, unit_id):
    logged_in_landlord_id = session.get('landlord_id')

    # Check if the logged-in landlord is authorized to view the requested profile
    if logged_in_landlord_id is None or logged_in_landlord_id != landlord_id:
        flash('You are not authorized to view this profile.', 'error')
        session.clear()
        return redirect(url_for('landlord_bp.home'))
    # render payments for given unit
    landlord=Landlord.query.filter_by(id=landlord_id).first()
    unit=Unit.query.filter_by(id=unit_id).first()
    payments=unit.payments

    return render_template('landlord_unit_payments.html', landlord=landlord, unit=unit, payments=payments)


@landlord_bp.route('/landlord/<int:landlord_id>/createunit', methods=['GET', 'POST'])
def create_unit(landlord_id):
    logged_in_landlord_id = session.get('landlord_id')

    # Check if the logged-in landlord is authorized to view the requested profile
    if logged_in_landlord_id is None or logged_in_landlord_id != landlord_id:
        flash('You are not authorized to view this profile.', 'error')
        session.clear()
        return redirect(url_for('landlord_bp.home'))
    # render create unit page
    landlord=Landlord.query.filter_by(id=landlord_id).first()
    if request.method == 'GET':
        return render_template('create_unit.html', landlord=landlord)
    elif request.method =='POST':
        unit_number = request.form.get('unit_number')
        address = request.form.get('address')
        rent = request.form.get('rent')
        lease_start=request.form.get('lease_start')
        rent_due=request.form.get('rent_due')

        new_unit = Unit(
            landlord_id=landlord.id,
            unit_number=unit_number,
            address=address,
            rent=rent if rent else None,
            lease_start=lease_start if lease_start else None,
            rent_due=rent_due if rent_due else None,
        )

        db.session.add(new_unit)
        db.session.commit()

        unit = new_unit
        
        return redirect(url_for('landlord_bp.landlord_unit_page', landlord_id=unit.landlord_id, unit_id=unit.id))


@landlord_bp.route('/landlord/<int:landlord_id>/expenses', methods=['GET'])
def landlord_expenses(landlord_id):
    logged_in_landlord_id = session.get('landlord_id')

    # Check if the logged-in landlord is authorized to view the requested profile
    if logged_in_landlord_id is None or logged_in_landlord_id != landlord_id:
        flash('You are not authorized to view this profile.', 'error')
        session.clear()
        return redirect(url_for('landlord_bp.home'))
    # render all expenses for given landlord
    landlord = Landlord.query.filter_by(id=landlord_id).first()
    units = landlord.units

    expenses = []
    for unit in units:
        expenses.extend(unit.expenses)

    return render_template('landlord_expenses.html', landlord=landlord, units=units, expenses=expenses)
    

@landlord_bp.route('/landlord/<int:landlord_id>/createexpense', methods=['GET', 'POST'])
def create_expense(landlord_id):
    logged_in_landlord_id = session.get('landlord_id')

    # Check if the logged-in landlord is authorized to view the requested profile
    if logged_in_landlord_id is None or logged_in_landlord_id != landlord_id:
        flash('You are not authorized to view this profile.', 'error')
        session.clear()
        return redirect(url_for('landlord_bp.home'))
    # create an expense, select unit from drop down menu
    landlord = Landlord.query.filter_by(id=landlord_id).first()
    units = landlord.units
    if request.method == 'GET':
        return render_template('create_expense.html', landlord=landlord, units=units)
    elif request.method == 'POST':
        unit_id = request.form.get('unit_id')
        cost = request.form.get('cost')
        description = request.form.get('description')
        contractor = request.form.get('contractor')
        contractor_contact = request.form.get('contractor_contact')
        date = request.form.get('date')

        new_expense = Expense(
            unit_id=unit_id,
            cost=cost,
            description=description,
            contractor=contractor,
            contractor_contact=contractor_contact,
            date=date
        )

        db.session.add(new_expense)
        db.session.commit()

        return redirect(url_for('landlord_bp.landlord_profile', landlord_id=landlord.id))


@landlord_bp.route('/landlord/<int:landlord_id>/payments', methods=['GET'])
def landlord_payments(landlord_id):
    logged_in_landlord_id = session.get('landlord_id')

    # Check if the logged-in landlord is authorized to view the requested profile
    if logged_in_landlord_id is None or logged_in_landlord_id != landlord_id:
        flash('You are not authorized to view this profile.', 'error')
        session.clear()
        return redirect(url_for('landlord_bp.home'))
    # render payments table for all units
    landlord = Landlord.query.filter_by(id=landlord_id).first()
    payments=landlord.payments

    return render_template('landlord_payments.html', landlord=landlord, payments=payments)

@landlord_bp.route('/landlord/<int:landlord_id>/payments/scan', methods=['GET'])
def landlord_scan(landlord_id):
    landlord = Landlord.query.filter_by(id=landlord_id).first()
    scan_units(landlord)

    return redirect(url_for('landlord_bp.landlord_payments', landlord_id=landlord.id))


@landlord_bp.route('/landlord/logout')
def landlord_logout():
    session.pop('landlord_id', None)  # Remove the landlord_id from the session
    return redirect(url_for('home_bp.home'))
