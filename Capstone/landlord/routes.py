from flask import Blueprint, request
from flask import current_app as app
from ..models import Landlord

# Blueprint for landlord
landlord_bp = Blueprint(
    'landlord_bp', __name__,
    template_folder='templates',
    static_folder='static'
)

@landlord_bp.route('/landlord')
def landlord_redirect():
    # if user is logged in, redirect to user profile page
    # else, redirect to tenant login page
    pass

@landlord_bp.route('/landlord/login')
def landlord_login():
    # landlord login page
    pass

@landlord_bp.route('/landlord/signup')
def landlord_signup():
    # landlord sign up page
    pass

@landlord_bp.route('/landlord/<int:landlord_id>', methods=['GET'])
def landlord_profile(landlord_id):
    # render landlord profile page with units table
    landlord = Landlord.query.filter_by(id=landlord_id).first()
    units = landlord.units

@landlord_bp.route('/landlord/<int:landlord_id>/<int:unit_id>', methods=['GET'])
def landlord_unit_page(landlord_id, unit_id):
    # render landlord unit page for a given unit
    pass

@landlord_bp.route('/landlord/<int:landlord_id>/<int:unit_id>/expenses', methods=['GET'])
def landlord_unit_expenses(landlord_id, unit_id):
    # render expenses for given unit
    pass

@landlord_bp.route('/landlord/<int:landlord_id>/<int:unit_id>/payments', methods=['GET'])
def landlord_unit_payments(landlord_id, unit_id):
    # render payments for given unit
    pass

@landlord_bp.route('/landlord/<int:landlord_id>/createunit', methods=['GET', 'POST'])
def create_unit(landlord_id):
    # render create unit page
    pass

@landlord_bp.route('/landlord/<int:landlord_id>/expenses', methods=['GET'])
def landlord_expenses(landlord_id):
    # render all expenses for given landlord
    pass

@landlord_bp.route('/landlord/<int:landlord_id>/createexpense', methods=['POST'])
def create_expense(landlord_id):
    # create an expense, select unit from drop down menu
    pass

@landlord_bp.route('/landlord/<int:landlord_id>/payments', methods=['GET'])
def landlord_payments(landlord_id):
    # render payments table for all units
    pass