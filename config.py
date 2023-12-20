"""Flask App configuration"""


class Config:
    # General config
    ENVIRONMENT = "development"
    FLASK_APP = "mack-app"
    FLASK_DEBUG = True
    STATIC_FOLDER = "static"
    TEMPLATES_FOLDER = "templates"