import psycopg2

from .utils import fetch_query, GENERIC_QUERIES


def joins(connection):
    try:
        with connection.cursor() as cursor:
            print("Successfully entered a transaction.")
            print("To abort the current transaction at any time, type \"!a\".")

            # Fetch available tables to provide options for the user
            tables = fetch_query(connection, GENERIC_QUERIES['get_tables'])
            print(f"\nAvailable tables: \n{', '.join([t[0] for t in tables])}")

            table1_name = input("First table to join: ")
            if table1_name == "!a":
                print("Aborted")
                return
            table2_name = input("Second table to join: ")
            if table2_name == "!a":
                print("Aborted")
                return

            # Fetch columns from both tables to guide the user in writing the join condition
            columns1 = fetch_query(connection, GENERIC_QUERIES['get_table_columns'].format(table=table1_name))
            print(f"\nAvailable columns in {table1_name}: \n{columns1}")
            columns2 = fetch_query(connection, GENERIC_QUERIES['get_table_columns'].format(table=table2_name))
            print(f"\nAvailable columns in {table2_name}: \n{columns2}")

            join_type = input("Join type: (JOIN, LEFT JOIN, RIGHT JOIN, FULL OUTER JOIN): ").strip().upper()
            if join_type == "!A":
                print("Aborted")
                return
            join_condition = input("Join condition (Ex: table1.[column] = table2.[column]): ")
            if join_condition == "!a":
                print("Aborted")
                return

            if join_type == 'JOIN':
                query = f"SELECT * FROM {table1_name} INNER JOIN {table2_name} ON {join_condition}"
            elif join_type == 'LEFT JOIN':
                query = f"SELECT * FROM {table1_name} LEFT JOIN {table2_name} ON {join_condition}"
            elif join_type == 'RIGHT JOIN':
                query = f"SELECT * FROM {table1_name} RIGHT JOIN {table2_name} ON {join_condition}"
            elif join_type == 'FULL OUTER JOIN':
                query = f"SELECT * FROM {table1_name} FULL OUTER JOIN {table2_name} ON {join_condition}"
            else:
                print("Wrong join type. Aborted")
                return

            cursor.execute(query)
            rows = cursor.fetchall()

            if rows:
                print("Join results:")
                for row in rows:
                    print(row)
            else:
                print("No matching records found after join")

    except psycopg2.Error as e:
        connection.rollback()
        print(f"Error performing join: ({e})")


def subqueries(connection):
    try:
        with connection.cursor() as cursor:
            print("Successfully entered a transaction.")
            print("To abort the current transaction at any time, type \"!a\".")

            # Fetch available tables to provide options for the user
            tables = fetch_query(connection, GENERIC_QUERIES['get_tables'])
            print(f"\nAvailable tables: \n{', '.join([t[0] for t in tables])}")

            main_table = input("Table of the main query: ")
            if main_table == "!a":
                print("Aborted")
                return

            # Fetch columns of the main table to guide the user in providing correct input
            main_columns = fetch_query(connection, GENERIC_QUERIES['get_table_columns'].format(table=main_table))
            print(f"\nAvailable columns in {main_table}: \n{main_columns}")

            main_column = input("Column of the main table: ")
            if main_column == "!a":
                print("Aborted")
                return

            print(f"\nAvailable tables: \n{', '.join([t[0] for t in tables])}")

            sub_table = input("Table of the subquery: ")
            if sub_table == "!a":
                print("Aborted")
                return

            # Fetch columns of the subquery table to guide the user in providing correct input
            sub_columns = fetch_query(connection, GENERIC_QUERIES['get_table_columns'].format(table=sub_table))
            print(f"\nAvailable columns in {sub_table}: \n{sub_columns}")

            sub_column = input("Column of the subquery table: ")
            if sub_column == "!a":
                print("Aborted")
                return

            subquery = f"SELECT {sub_column} FROM {sub_table}"
            main_query = f"SELECT * FROM {main_table} WHERE {main_column} IN ({subquery})"

            cursor.execute(main_query)
            main_result = cursor.fetchall()

            if main_result:
                print("Main Query Result:")
                for row in main_result:
                    print(row)
            else:
                print("Main query returned no results")

    except psycopg2.Error as e:
        connection.rollback()
        print(f"Error executing subqueries: ({e})")
