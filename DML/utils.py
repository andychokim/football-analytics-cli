import psycopg2


GENERIC_QUERIES = {
    # information_schema stores metadata about the database, including tables and columns
    # by default, the public schema is where user-created tables are stored in PostgreSQL
    # filter for BASE TABLE to exclude other types (e.g., views, foreign, or temporary tables)
    'get_tables': """
        SELECT t.table_name
        FROM information_schema.tables t
        WHERE t.table_schema = 'public' AND t.table_type = 'BASE TABLE'
    """,

    'get_table_columns': """
        SELECT c.column_name, c.data_type
        FROM information_schema.columns c
        WHERE c.table_name = '{table}'
    """,

    'search_all': "SELECT * FROM {table}",

    'search_data': "SELECT * FROM {table} WHERE {field} {operator} {value}",
}


def fetch_query(connection, query_type, params=None):
    try:
        with connection.cursor() as cursor:
            if params is not None:
                cursor.execute(query_type, params)
            else:
                cursor.execute(query_type)

            return cursor.fetchall()

    except psycopg2.Error as e:
        print(f"Error executing query: {e}")
        connection.rollback()
        return None
