import mysql.connector


def get_connection(host, user, password, database):
    return mysql.connector.connect(user=user, password=password, host=host, database=database)


def connect(host, user, password, database):
    """
    Function to connect to MySQL database.
    It returns a tuple that contains:
    0. The tables of the database in a list
    1. MySQL configuration dictionary
    """
    conn = get_connection(host, user, password, database)
    with conn.cursor() as cursor:
        cursor.execute("SHOW TABLES")
        tables = [x[0] for x in cursor]

    conn.close()

    # Mysql information to store in browser memory for future use
    mysql_info = {
        "user": user,
        "password": password,
        "host": host,
        "database": database,
        "raise_on_warnings": True,
    }

    return tables, mysql_info


def execute_query(config, query):
    """
    Function to execure an sql query,config is a dictionary with connection information to connect to the database
    Returns a tuple that contains:
    0. A list with the column names of the result
    1. A list of the tuples with the rows of the result
    """
    conn = mysql.connector.connect(**config)
    with conn.cursor() as cursor:
        cursor.execute(query)
        columns = cursor.column_names
        results = cursor.fetchall()

    conn.close()
    return columns, results
