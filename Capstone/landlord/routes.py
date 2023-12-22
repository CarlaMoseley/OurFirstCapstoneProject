from flask import Blueprint, render_template, redirect, url_for, request, session, flash
from flask import current_app as app
from ..db import db
from ..models import Landlord, Unit, Expense

# Blueprint for landlord
landlord_bp = Blueprint(
    'landlord_bp', __name__,
    template_folder='templates',
    static_folder='static'
)


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
    # else, redirect to tenant login page
    pass


@landlord_bp.route('/landlord/login', methods=['GET', 'POST'])
def landlord_login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        # Check if the user exists in the database
        user_exists, landlord_id = check_credentials(username, password)

        if user_exists:
            # Store the landlord_id in the session for future use
            session['landlord_id'] = landlord_id

            # Redirect to the landlord profile page with the landlord_id
            return redirect(url_for('landlord_bp.landlord_profile', landlord_id=landlord_id))
        else:
            # User does not exist or incorrect credentials, show an error message
            error_message = "Invalid credentials. Please try again."
            flash(error_message, 'error')
            return render_template('login.html', error_message=error_message)

    # Render the login page for GET requests
    return render_template('login.html')


@landlord_bp.route('/landlord/signup')
def landlord_signup():
    # landlord sign up page
    return render_template('LandlordSignUp.html')


@landlord_bp.route('/landlord/<int:landlord_id>', methods=['GET','POST'])
def landlord_profile(landlord_id):
    # render landlord profile page with units table
    landlord = Landlord.query.filter_by(id=landlord_id).first()
    units = landlord.units

    return render_template('landlordhome.html', landlord=landlord, units=units)


@landlord_bp.route('/landlord/<int:landlord_id>/tenants', methods=['GET'])
def landlord_tenants(landlord_id):
    landlord = Landlord.query.filter_by(id=landlord_id).first()
    tenants = []
    for unit in landlord.units:
        tenants.extend(unit.tenants)
    
    return render_template('PLACEHOLDER', landlord=landlord, tenants=tenants)


@landlord_bp.route('/landlord/<int:landlord_id>/<int:unit_id>', methods=['GET'])
def landlord_unit_page(landlord_id, unit_id):
    # render landlord unit page for a given unit
    landlord=Landlord.query.filter_by(id=landlord_id).first()
    unit=Unit.query.filter_by(id=unit_id).first()

    return render_template('PLACEHOLDER', landlord=landlord, unit=unit)

@landlord_bp.route('/landlord/<int:landlord_id>/<int:unit_id>/expenses', methods=['GET'])
def landlord_unit_expenses(landlord_id, unit_id):
    # render expenses for given unit
    landlord=Landlord.query.filter_by(id=landlord_id).first()
    unit=Unit.query.filter_by(id=unit_id).first()
    expenses=unit.expenses

    return render_template('PLACEHOLDER', landlord=landlord, unit=unit, expenses=expenses)

@landlord_bp.route('/landlord/<int:landlord_id>/<int:unit_id>/payments', methods=['GET'])
def landlord_unit_payments(landlord_id, unit_id):
    # render payments for given unit
    landlord=Landlord.query.filter_by(id=landlord_id).first()
    unit=Unit.query.filter_by(id=unit_id).first()
    payments=unit.payments

    return render_template('PLACEHOLDER', landlord=landlord, unit=unit, payments=payments)

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
            rent=rent,
            lease_start=lease_start,
            rent_due=rent_due,
        )

        db.session.add(new_unit)
        db.session.commit()

        unit = Unit.query.filter(landlord_id=landlord.id).filter(unit_number=unit).filter(address=address).first()
        
        return redirect(url_for('landlord_unit_page', landlord_id=unit.landlord_id, unit_id=unit.id))


@landlord_bp.route('/landlord/<int:landlord_id>/expenses', methods=['GET'])
def landlord_expenses(landlord_id):
    # render all expenses for given landlord
    landlord = Landlord.query.filter_by(id=landlord_id).first()
    units = landlord.units

    expenses = []
    for unit in units:
        expenses.extend(unit.expenses)

    return render_template('PLACEHOLDER', landlord=landlord, units=units, expenses=expenses)
    

@landlord_bp.route('/landlord/<int:landlord_id>/createexpense', methods=['GET', 'POST'])
def create_expense(landlord_id):
    # create an expense, select unit from drop down menu
    landlord = Landlord.query.filter_by(id=landlord_id).first()
    units = landlord.units
    if request.method == 'GET':
        return render_template('PLACEHOLDER', landlord=landlord, units=units)
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

        return redirect(url_for('landlord_profile', landlord_id=landlord.id))

@landlord_bp.route('/landlord/<int:landlord_id>/payments', methods=['GET'])
def landlord_payments(landlord_id):
    # render payments table for all units
    landlord = Landlord.query.filter_by(id=landlord_id).first()
    payments=landlord.payments

    return render_template('PLACEHOLDER', landlord=landlord, payments=payments)