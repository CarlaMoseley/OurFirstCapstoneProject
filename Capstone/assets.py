# compile static assets
from flask import current_app as app
from flask_assets import Bundle


def compile_static_assets(assets):
    # create stylesheet bundles
    assets.auto_build = True
    assets.debug = False
    common_style_bundle = Bundle(
        'css/*.css'
    )
    home_style_bundle = Bundle(
        'home_bp/css/home.css'
    )
    landlord_style_bundle = Bundle(
        'landlord_bp/css/landlord.css'
    )
    tenant_style_bundle = Bundle(
        'tenant_bp/css/tenant.css'
    )
    assets.register('common_style_bundle', common_style_bundle)
    assets.register('home_style_bundle', home_style_bundle)
    assets.register('landlord_style_bundle', landlord_style_bundle)
    assets.register('tenant_style_bundle', tenant_style_bundle)
    if app.config['FLASK_ENV'] == 'development':
        common_style_bundle.build()
        home_style_bundle.build()
        landlord_style_bundle.build()
        tenant_style_bundle.build()
    return assets