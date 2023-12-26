"""Flask App configuration"""
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend
from snowflake.sqlalchemy import URL


class Config:
    # General config
    ENVIRONMENT = "development"
    FLASK_APP = "mack-app"
    FLASK_DEBUG = True
    STATIC_FOLDER = "static"
    TEMPLATES_FOLDER = "templates"
    SNOWFLAKE_PARAMETERS = {
        'user':'dev_snowflake_training_svc',
        'private_key_file':r'./Capstone/dev_snowflake_training_rsa_key.p8',
        'private_key_file_pwd':'B7GX$en3Pz#fSw8yi!pv',
        'account':'fiservbanksolutionsawslow1.us-east-1.privatelink',
        'database':'TECHNICAL_TRAINEE',
        'warehouse':'DEV_TECHNICAL_TRAINEE_WH',
        'schema':'AMACMASTER',
        'role':'FR_DEV_TECHNICAL_TRAINEE_DEVELOPER'
    }
    SQLALCHEMY_DATABASE_URI = URL(
        account=SNOWFLAKE_PARAMETERS['account'],
        warehouse=SNOWFLAKE_PARAMETERS['warehouse'],
        database=SNOWFLAKE_PARAMETERS['database'],
        schema=SNOWFLAKE_PARAMETERS['schema'],
        role=SNOWFLAKE_PARAMETERS['role'],
        user=SNOWFLAKE_PARAMETERS['user'],
    )
    SNOWFLAKE_PRIVATE_KEY = serialization.load_pem_private_key(
                open(SNOWFLAKE_PARAMETERS['private_key_file'], 'rb').read(),
                password=SNOWFLAKE_PARAMETERS['private_key_file_pwd'].encode(),
                backend=default_backend()
    )
    SNOWFLAKE_CONNECTION_ARGS={
        'connect_args': {
            'private_key':SNOWFLAKE_PRIVATE_KEY.private_bytes(
            encoding=serialization.Encoding.DER,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        )
        }
    }

    