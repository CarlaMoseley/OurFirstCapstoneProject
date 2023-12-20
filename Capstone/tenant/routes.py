from flask import Blueprint, render_template, request
from flask import current_app as app
from ..models import Tenant, Unit, Payment

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
    tenant = Tenant.query.filter_by(id=tenant_id).first()

    return render_template('PLACEHOLDER', tenant=tenant)

@tenant_bp.route('/tenant/<int:tenant_id>/payments')
def tenant_payments(tenant_id):
    # render tenant payments page
    tenant = Tenant.query.filter_by(id=tenant_id).first()
    payments = tenant.payments

    return render_template('PLACEHOLDER', tenant=tenant, payments=payments)

@tenant_bp.route('/tenant/<int:tenant_id>/unit')
def tenant_unit(tenant_id):
    # render tenant unit page
    tenant = Tenant.query.filter_by(id=tenant_id).first()
    unit = Unit.query.filter_by(tenant.unit_id).first()

    return render_template('PLACEHOLDER', tenant=tenant, unit=unit)

@tenant_bp.route('/tenant/<int:tenant_id>/makepayment', methods=['GET', 'POST'])
def make_payment(tenant_id):
    # render make payment page
    tenant = Tenant.query.filter_by(id=tenant_id).first()
    if request.method == 'GET':
        return render_template('PLACEHOLDER', tenant=tenant)
    elif request.method == 'POST':
        # insert logic about payment processing here
        pass

@tenant_bp.route('/tenant/<int:tenant_id>/<int:payment_id>')
def tenant_payment(tenant_id, payment_id):
    # render individual payment page
    tenant = Tenant.query.filter_by(id=tenant_id).first()
    payment = Payment.query.filter_by(id=payment_id).first

    return render_template('PLACEHOLDER', tenant=tenant, payment=payment)