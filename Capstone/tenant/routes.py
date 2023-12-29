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
import pyotp
import json


# Blueprint for tenant
tenant_bp = Blueprint(
    'tenant_bp', __name__,
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


def check_credentials(username, password):
    tenant = Tenant.query.filter_by(username=username).first()

    if not tenant:
        return False, None

    if tenant.password == password:
        return True, tenant.id
    else:
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

        # Check user input against blacklist
        try:
            sanitize_input(password, username)
        except ValueError as e:
            error_message = f"Invalid credentials: {str(e)}"
            flash(error_message, 'error')
            return render_template('tenant_login.html', error_message=error_message)

        # Hashing application
        secured_hash_password = hash_password(password)

        # Check if the user exists in the database
        user_exists, tenant_id = check_credentials(username, secured_hash_password)

        if user_exists:
            # Check if TOTP setup is required for the user
            totp_required = True  # Replace this with your logic to determine if TOTP is required
            if totp_required:
                # Generate TOTP URI and secret
                totp_uri, totp_secret = generate_totp_uri(username)
                print(totp_uri)
                print(totp_secret)

                # Store the TOTP secret in the session for later verification
                session['totp_secret'] = totp_secret
                session['tenant_id'] = tenant_id
                # Redirect to the TOTP setup page
                return redirect(url_for('tenant_bp.setup_totp', totp_uri=totp_uri))

            # If TOTP is not required, proceed with regular login
        else:
            # User does not exist or incorrect credentials, show an error message
            error_message = "Invalid credentials. Please try again."
            flash(error_message, 'error')
            return render_template('tenant_login.html', error_message=error_message)

    # Render the login page for GET requests
    return render_template('tenant_login.html')


@tenant_bp.route('/tenant/setup_totp', methods=['GET', 'POST'])
def setup_totp():
    totp_uri = request.args.get('totp_uri')
    # Retrieve the TOTP secret from the session
    totp_secret = session.get('totp_secret')
    tenant_id = session.get('tenant_id')

    if not totp_secret:
        # Redirect to the login page if TOTP secret is not available
        return redirect(url_for('tenant_bp.tenant_login'))

    if request.method == 'POST':
        otp_number = request.form.get('OTP')
        session['last_activity'] = datetime.utcnow()
        # Verify the provided OTP against the TOTP secret
        totp = pyotp.TOTP(totp_secret)
        is_valid_otp = totp.verify(otp_number)

        if is_valid_otp:
            print('valid otp')
            # OTP is valid, you can proceed with whatever action is needed
            # (e.g., store the fact that TOTP is set up for this user)
            return redirect(url_for('tenant_bp.tenant_profile', tenant_id=tenant_id))
        else:
            print('not valid')
            # Invalid OTP, render the setup_totp page with an error message
            error_message = "Invalid OTP. Please try again."
            flash(error_message, 'error')
            return render_template('tenant_setup_totp.html', totp_secret=totp_secret, totp_uri=totp_uri, error_message=error_message)

    # Render the TOTP setup page with the QR code
    return render_template('tenant_setup_totp.html', totp_secret=totp_secret, totp_uri=totp_uri)


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
        unit_password = request.form.get('id')
        #Check user input against blacklist
        try: 
            sanitize_input(password, username)
        except ValueError as e:
            error_message = f"Invalid credentials: {str(e)}"
            flash(error_message, 'error')
            return redirect(url_for('tenant_bp.tenant_signup', error_message=error_message))
                        
        #hashing password and confirmpassword
        secured_password = hash_password(password)
        secured_ConfirmPassword = hash_password(confirmpassword)

        if secured_password != secured_ConfirmPassword:
            error_message = "Password does not match"
            flash(error_message, 'error')

            # redirect back to signup page
            return redirect(url_for('tenant_bp.tenant_signup'))

        if unit_password is None:
            flash('One Time Unit Password from landlord is required', 'error')
            return redirect(url_for('tenant_bp.tenant_signup'))

        # Check if the unit_id exists in the Unit table
        unit = Unit.query.filter_by(tenant_password=unit_password).first()
        if unit is None:
            flash(f'Unit with One Time Password {unit_password} does not exist', 'error')
            return redirect(url_for('tenant_bp.tenant_signup'))

        new_tenant = Tenant(
            first_name=f_name,
            last_name=l_name,
            phone_number=phonenumber,
            email=email,
            username=username,
            password=secured_password,
            unit_id=unit.id
        )
        db.session.add(new_tenant)
        unit.tenant_password = None
        db.session.commit()

        # Redirect to a success page or another route
        flash('Tenant registration successful!', 'success')

    # tenant sign up page
    return render_template('TenantSignUp.html')


@tenant_bp.route('/tenant/<int:tenant_id>')
def tenant_profile(tenant_id):
    logged_in_tenant_id = session.get('tenant_id')

    # Check if the logged-in landlord is authorized to view the requested profile
    if logged_in_tenant_id is None or logged_in_tenant_id != tenant_id:
        flash('You are not authorized to view this profile.', 'error')
        session.clear()
        return redirect(url_for('home_bp.home'))

    # render tenant profile page
    tenant = Tenant.query.filter_by(id=tenant_id).first()
    if request.method == 'POST':
        f_name = request.form.get('f_name')
        l_name = request.form.get('l_name')
        phonenumber = request.form.get('phonenumber')
        email = request.form.get('email')

        tenant.first_name = f_name
        tenant.last_name = l_name
        tenant.phone_number = phonenumber
        tenant.email = email

        db.session.commit()

        redirect(url_for('tenant_bp.tenant_profile', tenant_id=tenant.id))
    else:
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
    logged_in_tenant_id = session.get('tenant_id')

    # Check if the logged-in landlord is authorized to view the requested profile
    if logged_in_tenant_id is None or logged_in_tenant_id != tenant_id:
        flash('You are not authorized to view this profile.', 'error')
        session.clear()
        return redirect(url_for('home_bp.home'))

    # render make payment page
    tenant = Tenant.query.filter_by(id=tenant_id).first()
    if request.method == 'POST':

        try:
            amount = tenant.unit.rent
            card_number = request.form.get('cardNumber')
            expiration_month = request.form.get('expMonth')
            expiration_year = request.form.get('expYear')
            security_code = request.form.get('securityCode')
            account_number = request.form.get('accountNumber')
            routing_number = request.form.get('routingNumber')
            payment_id = request.form.get('payment_id')

            payment_service = PaymentService()
            if not payment_id:
                flash('No statement selected')
                return redirect(url_for("tenant_bp.tenant_payments", tenant_id=tenant.id))

            if card_number:
                # payment service makes a cc request
                response = payment_service.make_dummy_cc_request(amount, card_number, expiration_month, expiration_year, security_code)

            elif routing_number:
                # payment service makes an ach request                
                response = payment_service.make_ach_request(amount, account_number, routing_number)

            parsed_response = json.loads(response)

            approval_status = parsed_response["paymentReceipt"]["processorResponseDetails"]["approvalStatus"]

            if not approval_status == "APPROVED":
                flash('Payment failed')
                return redirect(url_for("tenant_bp.tenant_payments", tenant_id=tenant.id))


            payment = Payment.query.filter_by(id=payment_id).first()
            payment.date = date.today()
            payment.paid=True
            db.session.commit()
 

            compose_email(tenant, 'payment_success')
            compose_email(tenant.unit.landlord, 'landlord_receipt', tenant=tenant)

            return redirect(url_for("tenant_bp.tenant_payments", tenant_id=tenant.id))
        except Exception as e:
            return jsonify({"status": "error", "message": str(e)})
    else:
        unpaid_statements = Payment.query.filter_by(paid=False).filter_by(tenant_id=tenant.id).all()
        return render_template('makepayment.html', tenant=tenant, unpaid_statements=unpaid_statements)


@tenant_bp.route('/tenant/<int:tenant_id>/<int:payment_id>')
def tenant_payment(tenant_id, payment_id):
    logged_in_tenant_id = session.get('tenant_id')

    # Check if the logged-in landlord is authorized to view the requested profile
    if logged_in_tenant_id is None or logged_in_tenant_id != tenant_id:
        flash('You are not authorized to view this profile.', 'error')
        session.clear()
        return redirect(url_for('home_bp.home'))

    # render individual payment page
    tenant = Tenant.query.filter_by(id=tenant_id).first()
    payment = Payment.query.filter_by(id=payment_id).first()

    return render_template('tenant_payment.html', tenant=tenant, payment=payment)


@tenant_bp.route('/tenant/logout')
def tenant_logout():
    session.pop('tenant_id', None)  # Remove the tenant_id from the session
    return redirect(url_for('home_bp.home'))
