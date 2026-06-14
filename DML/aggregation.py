import psycopg2

from .utils import fetch_query, GENERIC_QUERIES


def aggregate_functions(connection):
    try:
        with connection.cursor() as cursor:
            print("Successfully entered a transaction.")
            print("To abort the current transaction at any time, type \"!a\".")

            # Fetch available tables to provide options for the user
            tables = fetch_query(connection, GENERIC_QUERIES['get_tables'])
            print(f"\nAvailable tables: \n{', '.join([t[0] for t in tables])}")

            table_name = input("Table to use the aggregate functions on: ")
            if table_name == "!a":
                print("Aborted")
                return

            # Fetch columns of the selected table to guide the user in providing correct input
            columns = fetch_query(connection, GENERIC_QUERIES['get_table_columns'].format(table=table_name))
            print(f"\nAvailable columns in {table_name}: \n{columns}")

            column_name = input("Column for aggregation: ")
            if column_name == "!a":
                print("Aborted")
                return
            function = input("Aggregate function to use (SUM, AVG, COUNT, MIN, MAX): ")
            if function == "!a":
                print("Aborted")
                return

            query = f"SELECT {function}({column_name}) FROM {table_name}"
            cursor.execute(query)
            result = cursor.fetchone()

            if result:
                print(f"{function}({column_name}): {result[0]}")
            else:
                print("No data available for aggregation")

    except psycopg2.Error as e:
        connection.rollback()
        print(f"Error performing aggregate function: ({e})")


def sorting(connection):
    try:
        with connection.cursor() as cursor:
            print("Successfully entered a transaction.")
            print("To abort the current transaction at any time, type \"!a\".")

            # Fetch available tables to provide options for the user
            tables = fetch_query(connection, GENERIC_QUERIES['get_tables'])
            print(f"\nAvailable tables: \n{', '.join([t[0] for t in tables])}")

            table_name = input("Table to sort the data: ")
            if table_name == "!a":
                print("Aborted")
                return

            # Fetch columns of the selected table to guide the user in providing correct input
            columns = fetch_query(connection, GENERIC_QUERIES['get_table_columns'].format(table=table_name))
            print(f"\nAvailable columns in {table_name}: \n{columns}")

            column_name = input("Column to sort: ")
            if column_name == "!a":
                print("Aborted")
                return
            order = input("Sorting order (Ex: ASC, DESC): ")
            if order == "!a":
                print("Aborted")
                return

            query = f"SELECT * FROM {table_name} ORDER BY {column_name} {order}"
            cursor.execute(query)
            rows = cursor.fetchall()

            if rows:
                print("Sorted results:")
                for row in rows:
                    print(row)
            else:
                print("No data available to sort")

    except psycopg2.Error as e:
        connection.rollback()
        print(f"Error sorting data: ({e})")


def grouping(connection):
    try:
        with connection.cursor() as cursor:
            print("Successfully entered a transaction.")
            print("To abort the current transaction at any time, type \"!a\".")

            # Fetch available tables to provide options for the user
            tables = fetch_query(connection, GENERIC_QUERIES['get_tables'])
            print(f"\nAvailable tables: \n{', '.join([t[0] for t in tables])}")

            table_name = input("Table to perform GROUP BY clause: ")
            if table_name == "!a":
                print("Aborted")
                return

            # Fetch columns of the selected table to guide the user in providing correct input
            columns = fetch_query(connection, GENERIC_QUERIES['get_table_columns'].format(table=table_name))
            print(f"\nAvailable columns in {table_name}: \n{columns}")

            column_name = input("Column to GROUP BY: ")
            if column_name == "!a":
                print("Aborted")
                return

            agg_functions = ["SUM", "AVG", "COUNT", "MIN", "MAX"]
            print(f"\nAggregate functions: \n{', '.join(agg_functions)}")

            agg_func = input("Aggregate function to apply (used in SELECT and HAVING):\n").strip().upper()
            if agg_func == "!A":
                print("Aborted")
                return

            print(f"\nAvailable columns in {table_name}: \n{columns}")
            agg_column = input("Column to apply the aggregate function on (use * for COUNT(*)):\n").strip()
            if agg_column == "!a":
                print("Aborted")
                return

            having_input = input("Add a HAVING clause? (y/n):\n").strip().lower()
            if having_input == "!a":
                print("Aborted")
                return

            if having_input == "y":

                operator_options = [">", "<", ">=", "<=", "="]
                print(f"\nOperators: \n{', '.join(operator_options)}")

                operator = input("Comparison operator:\n").strip()
                if operator == "!a":
                    print("Aborted")
                    return
                
                having_value = input("Value to compare against:\n")
                if having_value == "!a":
                    print("Aborted")
                    return
                
                query = f"SELECT {column_name}, {agg_func}({agg_column}) FROM {table_name} GROUP BY {column_name} HAVING {agg_func}({agg_column}) {operator} {having_value}"
            else:
                query = f"SELECT {column_name}, {agg_func}({agg_column}) FROM {table_name} GROUP BY {column_name}"

            cursor.execute(query)
            rows = cursor.fetchall()

            if rows:
                print("Grouping results:")
                for row in rows:
                    print(row)
            else:
                print("No data available for grouping")

    except psycopg2.Error as e:
        connection.rollback()
        print(f"Error performing grouping: ({e})")
