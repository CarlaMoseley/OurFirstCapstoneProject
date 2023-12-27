from flask import Blueprint, render_template, redirect, url_for, request, session, flash
from flask import current_app as app
from flask_session import Session
from ..db import db
from ..models import Landlord, Unit, Expense
from ..utils.password_hash import hash_password
from ..utils.inputblacklist import sanitize_input
from ..utils.date_scan import scan_units
from datetime import timedelta
import pyotp


# Blueprint for landlord
landlord_bp = Blueprint(
    'landlord_bp', __name__,
    template_folder='templates',
    static_folder='static'
)

# Configure Flask-Session
SESSION_TYPE = 'filesystem'
PERMANENT_SESSION_LIFETIME = timedelta(seconds=10)
app.config.from_object(__name__)
Session(app)


def check_credentials(username, password):
    landlord = Landlord.query.filter_by(username=username).first()
    if not landlord:
        return False, None
    if landlord.password == password:
        return True, landlord.id
    else:
        return False, None


@landlord_bp.route('/landlord')
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

        secured_hash_password = hash_password(password) 

        # Check if the user exists in the database
        user_exists, landlord_id = check_credentials(username, secured_hash_password)

        if user_exists:
            # Store the landlord_id in the session for future use
            session['landlord_id'] = landlord_id

            # Set session timeout
            session.permanent = True

            # Redirect to the landlord profile page with the landlord_id
            return redirect(url_for('landlord_bp.landlord_profile', landlord_id=landlord_id))
        else:
            # User does not exist or incorrect credentials, show an error message
            error_message = "Invalid credentials. Please try again."
            flash(error_message, 'error')
            return render_template('landlord_landlord_login.html', error_message=error_message)

    # Render the login page for GET requests
    return render_template('landlord_login.html')


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
            #redirect back to signup page
            return redirect(url_for('landlord_bp.landlord_signup'))

        new_landlord = Landlord(
            first_name=f_name,
            last_name=l_name,
            phone_number=phonenumber,
            email=email,
            username=username,
            password=secured_password
        )
        db.session.add(new_landlord)
        db.session.commit()

        # Redirect to a success page or another route
        flash('Landlord registration successful!', 'success')

    return render_template('LandlordSignUp.html')

@landlord_bp.route('/landlord/2fa', methods=['GET', 'POST'])
def landlord_two_factor_auth():
    if request.method == 'POST':
        # Verify the entered OTP
        entered_otp = request.form.get('otp', '')
        totp = pyotp.TOTP(session['secret'])
        if totp.verify(entered_otp):
            # OTP is valid, redirect to user profile or another protected route, get landlord_id from session
            return redirect(url_for('landlord_bp.landlord_profile'), landlord_id=landlord_id)
        else:
            # Invalid OTP, you may want to handle this case differently
            return render_template('landlord_2fa.html', qr_code_url=session['qr_code_url'])

    # Generate a new TOTP secret for the user
    totp = pyotp.TOTP(pyotp.random_base32())
    session['secret'] = totp.secret
    session['qr_code_url'] = totp.provisioning_uri(name='@katashi1995', issuer_name='MACK')

    return render_template('landlord_2fa.html', qr_code_url=session['qr_code_url'])


@landlord_bp.route('/landlord/<int:landlord_id>', methods=['GET','POST'])
def landlord_profile(landlord_id):
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
    landlord = Landlord.query.filter_by(id=landlord_id).first()
    units = landlord.units
    tenants = []
    for unit in units:
        tenants.extend(unit.tenants)
    
    return render_template('landlord_tenants.html', landlord=landlord, tenants=tenants, units=units)


@landlord_bp.route('/landlord/<int:landlord_id>/<int:unit_id>', methods=['GET'])
def landlord_unit_page(landlord_id, unit_id):
    # render landlord unit page for a given unit
    landlord=Landlord.query.filter_by(id=landlord_id).first()
    unit=Unit.query.filter_by(id=unit_id).first()

    return render_template('landlord_unit_page.html', landlord=landlord, unit=unit)


@landlord_bp.route('/landlord/<int:landlord_id>/<int:unit_id>/expenses', methods=['GET'])
def landlord_unit_expenses(landlord_id, unit_id):
    # render expenses for given unit
    landlord=Landlord.query.filter_by(id=landlord_id).first()
    unit=Unit.query.filter_by(id=unit_id).first()
    expenses=unit.expenses

    return render_template('landlord_unit_expenses.html', landlord=landlord, unit=unit, expenses=expenses)


@landlord_bp.route('/landlord/<int:landlord_id>/<int:unit_id>/payments', methods=['GET'])
def landlord_unit_payments(landlord_id, unit_id):
    # render payments for given unit
    landlord=Landlord.query.filter_by(id=landlord_id).first()
    unit=Unit.query.filter_by(id=unit_id).first()
    payments=unit.payments

    return render_template('landlord_unit_payments.html', landlord=landlord, unit=unit, payments=payments)


@landlord_bp.route('/landlord/<int:landlord_id>/createunit', methods=['GET', 'POST'])
def create_unit(landlord_id):
    # render create unit page
    landlord=Landlord.query.filter_by(id=landlord_id).first()
    if request.method == 'GET':
        return render_template('create_unit.html', landlord=landlord)
    elif request.method=='POST':
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
    # render all expenses for given landlord
    landlord = Landlord.query.filter_by(id=landlord_id).first()
    units = landlord.units

    expenses = []
    for unit in units:
        expenses.extend(unit.expenses)

    return render_template('landlord_expenses.html', landlord=landlord, units=units, expenses=expenses)
    

@landlord_bp.route('/landlord/<int:landlord_id>/createexpense', methods=['GET', 'POST'])
def create_expense(landlord_id):
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
    return redirect(url_for('landlord_bp.landlord_login'))
