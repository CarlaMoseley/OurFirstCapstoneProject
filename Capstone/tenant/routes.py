from flask import Blueprint, render_template, redirect, url_for, request, session
from flask import current_app as app

# Blueprint for tenant
tenant_bp = Blueprint(
    'tenant_bp', __name__,
    template_folder='templates',
    static_folder='static'
)


def check_credentials(username, password):



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

        # Check if the user exists in the database
        user_exists, tenant_id = check_user_credentials(username, password)

        if user_exists:
            # Store the tenant_id in the session for future use
            session['tenant_id'] = tenant_id

            # Redirect to the tenant profile page with the tenant_id
            return redirect(url_for('tenant_bp.tenant_profile', tenant_id=tenant_id))
        else:
            # User does not exist or incorrect credentials, show an error message
            error_message = "Invalid credentials. Please try again."
            return render_template('login.html', error_message=error_message)

    # Render the login page for GET requests
    return render_template('login.html')

@tenant_bp.route('/tenant/signup')
def tenant_signup():
    # tenant sign up page
    pass

@tenant_bp.route('/tenant/<int:tenant_id>')
def tenant_profile(tenant_id):
    # render tenant profile page
    pass

@tenant_bp.route('/tenant/<int:tenant_id>/payments')
def tenant_payments(tenant_id):
    # render tenant payments page
    pass

@tenant_bp.route('/tenant/<int:tenant_id>/unit')
def tenant_unit(tenant_id):
    # render tenant unit page
    pass

@tenant_bp.route('/tenant/<int:tenant_id>/makepayment')
def make_payment(tenant_id):
    # render make payment page
    pass

@tenant_bp.route('/tenant/<int:tenant_id>/<int:payment_id>')
def tenant_payment(tenant_id, payment_id):
    # render individual payment page
    pass