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
            columns1_name = input("Columns from the first table to select (e.g., table1.column1, table1.column2) (comma separated, blank for all columns):\n")
            if columns1_name == "!a":
                print("Aborted")
                return

            columns2 = fetch_query(connection, GENERIC_QUERIES['get_table_columns'].format(table=table2_name))
            print(f"\nAvailable columns in {table2_name}: \n{columns2}")
            columns2_name = input("Columns from the second table to select (e.g., table2.column1, table2.column2) (comma separated, blank for all columns):\n")
            if columns2_name == "!a":
                print("Aborted")
                return

            # Determine the type of join and the join condition based on user input
            join_type = input("Join type: (JOIN, LEFT JOIN, RIGHT JOIN, FULL OUTER JOIN): ").strip().upper()
            if join_type == "!A":
                print("Aborted")
                return
            
            join_condition = input("Join condition (Ex: table1.[column] = table2.[column]): ")
            if join_condition == "!a":
                print("Aborted")
                return

            if join_type in ["JOIN", "LEFT JOIN", "RIGHT JOIN", "FULL OUTER JOIN"]:
                if not columns1_name and not columns2_name:
                    col_clause = "*"
                else:
                    cols1 = columns1_name if columns1_name else f"{table1_name}.*"
                    cols2 = columns2_name if columns2_name else f"{table2_name}.*"
                    col_clause = f"{cols1}, {cols2}"
                query = GENERIC_QUERIES['join_query'].format(
                    columns=col_clause,
                    table1=table1_name,
                    join_type=join_type,
                    table2=table2_name,
                    join_condition=join_condition
                )
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

            # Provide options for different types of subqueries to guide the user in writing the correct query
            subquery_types = ["1. IN subquery", "2. Aggregate comparison subquery"]
            print(f"\nSubquery types: \n{', '.join(subquery_types)}")

            subquery_type = input("Select subquery type (1 or 2):\n").strip()
            if subquery_type == "!a":
                print("Aborted")
                return

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

            if subquery_type == "1":
                query = f"SELECT * FROM {main_table} WHERE {main_column} IN (SELECT {sub_column} FROM {sub_table})"
            
            elif subquery_type == "2":

                agg_functions = ["AVG", "MAX", "MIN", "SUM"]
                print(f"\nAggregate functions: \n{', '.join(agg_functions)}")

                agg_func = input("Aggregate function for the subquery:\n").strip().upper()
                if agg_func == "!A":
                    print("Aborted")
                    return
                
                operator_options = [">", "<", ">=", "<=", "="]
                print(f"\nOperators: \n{', '.join(operator_options)}")

                operator = input("Comparison operator:\n").strip()
                if operator == "!a":
                    print("Aborted")
                    return
                
                query = f"SELECT * FROM {main_table} WHERE {main_column} {operator} (SELECT {agg_func}({sub_column}) FROM {sub_table})"
            else:
                print("Invalid subquery type. Aborted")
                return

            cursor.execute(query)
            result = cursor.fetchall()

            if result:
                print("Query result:")
                for row in result:
                    print(row)
            else:
                print("Query returned no results")

    except psycopg2.Error as e:
        connection.rollback()
        print(f"Error executing subqueries: ({e})")
