import mariadb


def get_connection(host, user, password, database):
    return mariadb.connect(user=user, password=password, host=host, database=database, port=3306)


def connect(host, user, password, database):
    """
    Function to connect to MariaDB database.
    It returns a tuple that contains:
    0. The tables of the database in a list
    1. MariaDB configuration dictionary
    """
    conn = get_connection(host, user, password, database)
    with conn.cursor() as cursor:
        cursor.execute("SHOW TABLES")
        tables = [x[0] for x in cursor]

    conn.close()

    # Mariadb information to store in browser memory for future use
    mariadb_info = {
        "user": user,
        "password": password,
        "host": host,
        "database": database,
    }

    return tables, mariadb_info


def execute_query(config, query):
    """
    Function to execure an sql query,config is a dictionary with connection information to connect to the database
    Returns a tuple that contains:
    0. A list with the column names of the result
    1. A list of the tuples with the rows of the result
    """
    conn = mariadb.connect(**config)
    with conn.cursor() as cursor:
        cursor.execute(query)
        columns = [i[0] for i in cursor.description]
        results = cursor.fetchall()

    conn.close()
    return columns, results
