import psycopg2
import misc_handler
import lookups

def create_connection():
    db_session = None
    try:
        keys_to_keep = ['db_host', 'db_user', 'db_pass', 'db_port', 'db_name']
        config_dict = misc_handler.parse_and_filter_configuration(keys_to_keep)
        connection_params = {
            'host': config_dict.get('db_host'),
            'user': config_dict.get('db_user'),
            'password': config_dict.get('db_pass'),
            'port': config_dict.get('db_port'),
            'dbname': config_dict.get('db_name'),
        }
        db_session = psycopg2.connect(**connection_params)
    except Exception as e:
        print(str(e))
    finally:
        return db_session

def execute_query(db_session, query):
    status = lookups.FunctionReturn.FAIL.value
    try:
        cursor = db_session.cursor()
        cursor.execute(query)
        db_session.commit()
        status = lookups.FunctionReturn.SUCCESS.value
    except Exception as e:
        print(str(e))
    finally:
        return status

def close_connection(db_session):
    try:
        if db_session:
            db_session.close()
    except Exception as e:
        print(str(e))

def create_schema(db_session, schema_name):
    query = f"CREATE SCHEMA IF NOT EXISTS {schema_name}"
    status = execute_query(db_session, query)
    print(status)