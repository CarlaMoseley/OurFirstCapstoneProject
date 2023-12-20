from flask import Blueprint, render_template, request, redirect, url_for
from flask import current_app as app


# Blueprint for home
home_bp = Blueprint(
    'home_bp', __name__,
    template_folder='templates',
    static_folder='static'
)




@home_bp.route('/', methods=['GET', 'POST'])
def home():
    button_clicked = None  # Default value for 'GET' requests
    if request.method == 'POST':
        data = request.json
        button_clicked = data.get('button')
        # Add any additional logic here if needed
        if button_clicked == 'tenant':
            return redirect(url_for('tenant_bp.tenant_login'))
        elif button_clicked == 'landlord':
            return redirect(url_for('landlord_bp.landlord_login'))

    # insert logic for home page
    # user selects tenant or landlord
    return render_template('start.html')
