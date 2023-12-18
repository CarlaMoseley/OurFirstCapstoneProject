from flask import Blueprint
from flask import current_app as app

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
    return "home"