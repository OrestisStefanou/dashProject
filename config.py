import database_controllers.mysql as mysql
#import database_controllers.mariadb as mariadb
#import database_controllers.postgres as postgres

database_sources = ["mysql"]#, "mariadb", "postgres"]

data_sources = database_sources + ["csv", "excel"]
plot_types = ["scatter", "line", "bar", "pie"]

# Create these dynamically
database_connection_functions = {"mysql": mysql.connect}#,"mariadb": mariadb.connect ,"postgres": postgres.connect}
database_execute_functions = {
    #"mariadb": mariadb.execute_query,
    "mysql": mysql.execute_query,
    #"postgres": postgres.execute_query,
}
