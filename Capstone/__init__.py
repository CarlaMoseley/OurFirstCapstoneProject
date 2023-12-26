from flask import Flask
from sqlalchemy import inspect
# from flask_assets import Environment
from .db import db

def tables_exist():
    inspector = inspect(db.engine)
    return all(inspector.get_table_names())


def create_app():

    # create flask application
    app = Flask(__name__, instance_relative_config=False)
    app.config['SECRET_KEY'] = 'ShusshItsaSecret'
    app.config.from_object('config.Config')
    # assets = Environment() # create assets environment
    # assets.init_app(app) # initialize flask-assets
    
    db._engine_options=app.config['SNOWFLAKE_CONNECTION_ARGS']
    db.init_app(app)
    with app.app_context():
        # import parts of the application
        from .home import routes as home
        from .tenant import routes as tenant
        from .landlord import routes as landlord
        # from .assets import compile_static_assets

        # register blueprints
        app.register_blueprint(home.home_bp)
        app.register_blueprint(tenant.tenant_bp)
        app.register_blueprint(landlord.landlord_bp)

        
        db.create_all()
        # compile static assets
        # compile_static_assets(assets)

        return app
