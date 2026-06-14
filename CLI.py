import psycopg2
import getpass

from DML import (
    create_data, delete_data, update_data,
    read_data,
    aggregate_functions, sorting, grouping,
    joins, subqueries,
)


def connect():
    try:
        password = getpass.getpass("PostgreSQL password: ") # for "blanked out" password

        connection = psycopg2.connect(
            dbname="postgres",
            user="postgres",
            password=password,
            host="localhost",
            port="5432",
        )
        print("Connected to the database successfully")
        return connection
    
    except psycopg2.Error as e:
        print("Unable to connect to the database")
        raise e


def main():
    try:
        connection = connect()

        while True:
            print("\nWelcome to my CLI interface\n")
            print("Please select an option:")
            print("0. Create Data")
            print("1. Read Data")
            print("2. Update Data")
            print("3. Delete Data")
            print("4. Aggregate Functions")
            print("5. Sorting")
            print("6. Joins")
            print("7. Grouping")
            print("8. Subqueries")
            print("9. Exit")

            choice = input("\nEnter your choice (0-9): ")
            match choice:
                case '0':
                    create_data(connection)
                case '1':
                    read_data(connection)
                case '2':
                    update_data(connection)
                case '3':
                    delete_data(connection)
                case '4':
                    aggregate_functions(connection)
                case '5':
                    sorting(connection)
                case '6':
                    joins(connection)
                case '7':
                    grouping(connection)
                case '8':
                    subqueries(connection)
                case '9':
                    print("Exiting the CLI interface")
                    break
                case _:
                    print("Invalid choice. Please select a valid option.")

    except psycopg2.Error as e:
        print(f"An error occurred: {e}")
        return e

    finally:
        if (connection is not None):
            connection.close()


if __name__ == "__main__":
    main()
