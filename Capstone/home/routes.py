from flask import Blueprint, render_template
from flask import current_app as app
from ..models import Tenant 

# Blueprint for home
home_bp = Blueprint(
    'home_bp', __name__,
    template_folder='templates',
    static_folder='static'
)

@home_bp.route('/')
def home():
    # insert logic for home page
    # user selects tenant or landlord 
    tenants = Tenant.query.all()
    return render_template('index.html', tenants=tenants)