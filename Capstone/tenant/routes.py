from flask import Blueprint
from flask import current_app as app

# Blueprint for tenant
tenant_bp = Blueprint(
    'tenant_bp', __name__,
    template_folder='templates',
    static_folder='static'
)

@tenant_bp.route('/tenant')
def tenant_redirect():
    # if user is logged in, redirect to user profile page
    # else, redirect to tenant login page
    pass

@tenant_bp.route('/tenant/login')
def tenant_login():
    # tenant login page
    pass

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