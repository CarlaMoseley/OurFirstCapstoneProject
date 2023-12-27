from flask import Blueprint, render_template, redirect, url_for, request, session, jsonify, flash
from flask import current_app as app
from flask_session import Session
from datetime import date, datetime, timedelta
from ..models import Tenant, Unit, Payment
from ..payment_processing.PaymentFiservAPI import PaymentService
from ..utils.email_processor import compose_email
from ..db import db
from ..utils.password_hash import hash_password
from ..utils.inputblacklist import sanitize_input


# Blueprint for tenant
tenant_bp = Blueprint(
    'tenant_bp', __name__,
    template_folder='templates',
    static_folder='static'
)


def check_credentials(username, secured_hash_password):
    tenant = Tenant.query.filter_by(username=username).first()
    if tenant.password == secured_hash_password:
        return True, tenant.id
    return False, None


@tenant_bp.route('/tenant')
def tenant_redirect():
    # if user is logged in, redirect to user profile page
    # else, redirect to tenant login page
    return redirect(url_for('tenant_login'))


@tenant_bp.route('/tenant/login', methods=['GET', 'POST'])
def tenant_login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
       
       #Check user input against blacklist 
        try: 
            sanitize_input(password, username)
        except ValueError as e:
            error_message = f"Invalid credentials: {str(e)}"
            return render_template('tenant_login.html', error_message=error_message)
        
        #Hashing appliccation
        secured_hash_password = hash_password(password) 
        
        # Check if the user exists in the database
        user_exists, tenant_id = check_credentials(username, secured_hash_password)

        if user_exists:
            # Redirect to the tenant profile page with the tenant_id
            return redirect(url_for('tenant_bp.tenant_profile', tenant_id=tenant_id))
        else:
            # User does not exist or incorrect credentials, show an error message
            error_message = "Invalid credentials. Please try again."
            return render_template('landlord_login.html', error_message=error_message)

    # Render the login page for GET requests
    return render_template('tenant_login.html')


@tenant_bp.route('/tenant/signup', methods=['GET', 'POST'])
def tenant_signup():
    if request.method == 'POST':
        f_name = request.form.get('f_name')
        l_name = request.form.get('l_name')
        phonenumber = request.form.get('phonenumber')
        email = request.form.get('email')
        username = request.form.get('username')
        password = request.form.get('password')
        confirmpassword = request.form.get('confirmpassword')
        unit_id = request.form.get('id')
        
        #Check user input against blacklist 
        try: 
            sanitize_input(password, username)
        except ValueError as e:
            error_message = f"Invalid credentials: {str(e)}"
            return redirect(url_for('tenant_bp.tenant_signup', error_message=error_message))
                        
        #hashing password and confirmpassword
        secured_password = hash_password(password)
        secured_ConfirmPassword = hash_password(confirmpassword)

        if secured_password != secured_ConfirmPassword:
            error_message = "Password does not match"
            flash(error_message, 'error')

            # redirect back to signup page
            return redirect(url_for('tenant_bp.tenant_signup'))

        if unit_id is None:
            flash('Unit ID is required', 'error')
            return redirect(url_for('tenant_bp.tenant_signup'))

        # Check if the unit_id exists in the Unit table
        unit = Unit.query.filter_by(id=unit_id).first()
        if unit is None:
            flash(f'Unit with ID {unit_id} does not exist', 'error')
            return redirect(url_for('tenant_bp.tenant_signup'))

        new_tenant = Tenant(
            first_name=f_name,
            last_name=l_name,
            phone_number=phonenumber,
            email=email,
            username=username,
            password=secured_password,
            unit_id=unit_id
        )
        db.session.add(new_tenant)
        db.session.commit()

        # Redirect to a success page or another route
        flash('Tenant registration successful!', 'success')

    # tenant sign up page
    return render_template('TenantSignUp.html')

  

@tenant_bp.route('/tenant/<int:tenant_id>')
def tenant_profile(tenant_id):
    # render tenant profile page
    tenant = Tenant.query.filter_by(id=tenant_id).first()
    unit = Unit.query.filter_by(id=tenant.unit_id).first()

    return render_template('tenant_profile.html', tenant=tenant, unit=unit)


@tenant_bp.route('/tenant/<int:tenant_id>/payments')
def tenant_payments(tenant_id):
    # render tenant payments page
    tenant = Tenant.query.filter_by(id=tenant_id).first()
    payments = tenant.payments

    return render_template('tenant_payments.html', tenant=tenant, payments=payments)


@tenant_bp.route('/tenant/<int:tenant_id>/makepayment', methods=['GET', 'POST'])
def make_payment(tenant_id):
    # render make payment page
    tenant = Tenant.query.filter_by(id=tenant_id).first()
    if request.method == 'POST':
        try:
            # Create an instance of the PaymentService class
            payment_service = PaymentService()

            # Make the payment request
            payment_service.make_payment_request()

            print(request)

            new_payment = Payment(
                tenant_id=tenant.id,
                unit_id=tenant.unit.id,
                landlord_id=tenant.unit.landlord.id,
                paid=True,
                date=date.today(),
                amount=tenant.unit.rent
            )

            db.session.add(new_payment)
            db.session.commit()

            compose_email(tenant, 'payment_success')
            compose_email(tenant.unit.landlord, 'landlord_receipt', tenant=tenant)

            return redirect(url_for("tenant_bp.tenant_payments", tenant_id=tenant.id))
        except Exception as e:
            return jsonify({"status": "error", "message": str(e)})
    else:
        return render_template('makepayment.html', tenant=tenant)


@tenant_bp.route('/tenant/<int:tenant_id>/<int:payment_id>')
def tenant_payment(tenant_id, payment_id):
    # render individual payment page
    tenant = Tenant.query.filter_by(id=tenant_id).first()
    payment = Payment.query.filter_by(id=payment_id).first

    return render_template('tenant_payment.html', tenant=tenant, payment=payment)


# @tenant_bp.route('/tenant/logout')
# def tenant_logout():
#     session.pop('tenant_id', None)  # Remove the tenant_id from the session
#     return redirect(url_for('tenant_bp.tenant_login'))
