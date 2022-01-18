import psycopg2


def get_connection(host, user, password, database):
    return psycopg2.connect(user=user, password=password, host=host, dbname=database)


def connect(host, user, password, database):
    """
    Function to connect to Postgres database.
    It returns a tuple that contains:
    0. The tables of the database in a list
    1. Postgres configuration dictionary
    """
    conn = get_connection(host, user, password, database)
    with conn.cursor() as cursor:
        cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'")
        tables = [x[0] for x in cursor]

    conn.close()

    # Postgres information to store in browser memory for future use
    postgres_info = {
        "user": user,
        "password": password,
        "host": host,
        "dbname": database,
    }

    return tables, postgres_info


def execute_query(config, query):
    """
    Function to execure an sql query,config is a dictionary with connection information to connect to the database
    Returns a tuple that contains:
    0. A list with the column names of the result
    1. A list of the tuples with the rows of the result
    """
    conn = psycopg2.connect(**config)
    with conn.cursor() as cursor:
        cursor.execute(query)
        columns = [i[0] for i in cursor.description]
        results = cursor.fetchall()

    conn.close()
    return columns, results
