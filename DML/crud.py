import psycopg2

from .utils import fetch_query, GENERIC_QUERIES


def create_data(connection):
    try:
        with connection.cursor() as cursor:
            print("Successfully entered a transaction.")
            print("To abort the current transaction at any time, type \"!a\".")

            # Fetch available tables to provide options for the user
            tables = fetch_query(connection, GENERIC_QUERIES['get_tables'])
            print(f"\nAvailable tables: \n{', '.join([t[0] for t in tables])}")

            table_name = input("Table to insert data into:\n")
            if table_name == "!a":
                print("Aborted")
                return

            # Fetch columns of the selected table to guide the user in providing correct input
            columns = fetch_query(connection, GENERIC_QUERIES['get_table_columns'].format(table=table_name))
            print(f"\nAvailable columns in {table_name}: \n{columns}")

            columns_name = input("Column(s) to insert data into (separated by comma):\n")
            if columns_name == "!a":
                print("Aborted")
                return
            
            values_name = input("Value(s) to insert into each column, in order (separated by comma). Wrap strings in single quotes (Ex: 'Arsenal', 100):\n")
            if values_name == "!a":
                print("Aborted")
                return

            query = f"INSERT INTO {table_name} ({columns_name}) VALUES ({values_name})"
            cursor.execute(query)
            connection.commit()
            print("Data inserted successfully")

    except psycopg2.Error as e:
        connection.rollback()
        print(f"Error inserting data: ({e})")


def update_data(connection):
    try:
        with connection.cursor() as cursor:
            print("Successfully entered a transaction.")
            print("To abort the current transaction at any time, type \"!a\".")

            # Fetch available tables to provide options for the user
            tables = fetch_query(connection, GENERIC_QUERIES['get_tables'])
            print(f"\nAvailable tables: \n{', '.join([t[0] for t in tables])}")

            table_name = input("Table to update the data in:\n")
            if table_name == "!a":
                print("Aborted")
                return
            
            # Fetch columns of the selected table to guide the user in providing correct input
            columns = fetch_query(connection, GENERIC_QUERIES['get_table_columns'].format(table=table_name))
            print(f"\nAvailable columns in {table_name}: \n{columns}")

            set_clause = input("Values to update. Wrap strings in single quotes. (Ex: Column1 = 'Value1', Column2 = Value2, ...):\n")
            if set_clause == "!a":
                print("Aborted")
                return
            
            condition = input("Condition for the row(s) to update. Wrap strings in single quotes. (Ex: Column1 = 'Value1'): \n")
            if condition == "!a":
                print("Aborted")
                return

            query = f"UPDATE {table_name} SET {set_clause} WHERE {condition}"
            cursor.execute(query)
            connection.commit()
            print("Data updated successfully")

    except psycopg2.Error as e:
        connection.rollback()
        print(f"Error updating data: ({e})")


def delete_data(connection):
    try:
        with connection.cursor() as cursor:
            print("Successfully entered a transaction.")
            print("To abort the current transaction at any time, type \"!a\".")

            # Fetch available tables to provide options for the user
            tables = fetch_query(connection, GENERIC_QUERIES['get_tables'])
            print(f"\nAvailable tables: \n{', '.join([t[0] for t in tables])}")

            table_name = input("Table to delete from:\n")
            if table_name == "!a":
                print("Aborted")
                return

            # Fetch columns of the selected table to guide the user in providing correct input
            columns = fetch_query(connection, GENERIC_QUERIES['get_table_columns'].format(table=table_name))
            print(f"\nAvailable columns in {table_name}: \n{columns}")

            condition = input("Condition for the row(s) to delete. Wrap strings in single quotes. (Ex: Column1 = 'Value1'): \n")
            if condition == "!a":
                print("Aborted")
                return

            query = f"DELETE FROM {table_name} WHERE {condition}"
            cursor.execute(query)
            connection.commit()
            print("Data deleted successfully")

    except psycopg2.Error as e:
        connection.rollback()
        print(f"Error deleting data: ({e})")
