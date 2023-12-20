import snowflake.connector


def get_snowflake_connection():
    con_params = {
    'user': 'dev_snowflake_training_svc',
    'account': 'fiservbanksolutionsawslow1.us-east-1.privatelink',
    'warehouse': 'DEV_TECHNICAL_TRAINEE_WH',
    'database': 'TECHNICAL_TRAINEE',
    'schema': 'CMOSELEY_HOMES',
    'role': 'FR_DEV_TECHNICAL_TRAINEE_DEVELOPER',
    'private_key_file': 'C:/Users/f96gakm/Desktop/Capstone/todolist-flask-/Capstone/dev_snowflake_training_rsa_key.p8',
    'private_key_file_pwd': 'B7GX$en3Pz#fSw8yi!pv'.encode('utf-8'),
    }
    connection = snowflake.connector.connect(**con_params)
    return connection



