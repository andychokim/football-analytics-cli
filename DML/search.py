import psycopg2

from .utils import fetch_query, GENERIC_QUERIES


def read_data(connection):
    try:
        tables = fetch_query(connection, GENERIC_QUERIES['get_tables'])
        if not tables:
            print("No tables returned or error occurred")
            return
        print(f"\nAvailable tables: \n{', '.join([t[0] for t in tables])}")

        table_input = input("Select the table to search from: ")

        if table_input not in [t[0] for t in tables]:
            print(f"Error: Table '{table_input}' does not exist")
            print("Aborted")
            return

        fields = fetch_query(connection, GENERIC_QUERIES['get_table_columns'].format(table=table_input))
        if fields is None:
            print("Error retrieving fields for the selected table")
            return
        print(f"\nAvailable columns in {table_input}: \n{fields}")

        field_input = input("Field to search (blank for selecting all fields): ")

        if field_input and field_input not in [c[0] for c in fields]:
            print(f"Error: Field '{field_input}' does not exist in the table '{table_input}'")
            print("Aborted")
            return

        if field_input == "":
            res = fetch_query(connection, GENERIC_QUERIES['search_all'].format(table=table_input))
        else:
            valid_operators = ['=', '>', '<', '>=', '<=', '!=', 'LIKE']
            print(f"\nAvailable operators: {', '.join(valid_operators)}")
            operator_input = input("Enter operator: ").strip().upper()

            if operator_input not in valid_operators:
                print("Invalid operator")
                print("Aborted")
                return

            value_input = input("Enter search value: ")
            res = fetch_query(connection, GENERIC_QUERIES['search_data'].format(
                table=table_input, field=field_input,
                operator=operator_input, value=value_input
            ))

        if res:
            print("\nSearch results:")
            for row in res:
                print(row)
        else:
            print("\nNo matching records found")

    except psycopg2.Error as e:
        print(f"Error searching data: ({e})")
