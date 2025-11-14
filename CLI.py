import psycopg2
import getpass

from queries import QUERIES

### helper functions for query executions
# Function to execute a query and fetch all results
def execute_query(conn, query, params=None):
    cur = None
    try:
        cur = conn.cursor()
        if params is not None:
            cur.execute(query, params)
        else:
            cur.execute(query)
        rows = cur.fetchall()
        return rows
    except psycopg2.Error as e:
        # Ensure the transaction is aborted and reset so the connection stays usable
        print("Error executing query:")
        print(e)
        try:
            conn.rollback()
        except Exception:
            pass
        return None
    finally:
        try:
            if cur is not None:
                cur.close()
        except Exception:
            pass

# Function to insert data into the database
def insert_data(conn):
    cur = None
    try:
        cur = conn.cursor()

        table_name = input("Table to insert data into: ")

        columns_str = input("Column(s) to insert data into (separated by comma): ")
        values_str = input("Value(s) to insert into (separated by comma): ")

        if (table_name or columns_str or values_str) == "abort" :
            print("Aborted")
        else :
            query = f"INSERT INTO {table_name} ({columns_str}) VALUES ({values_str})"
            cur.execute(query)

            conn.commit()
            print("Data inserted successfully")
    except psycopg2.Error as e:
        try:
            conn.rollback()
        except Exception:
            pass
        print("Error inserting data")
        print(e)
    finally:
        try:
            if cur is not None:
                cur.close()
        except Exception:
            pass

# Function to delete data from the database
def delete_data(conn):
    cur = None
    try:
        cur = conn.cursor()

        table_name = input("Table to delete from: ")
        condition = input("Condition (WHERE clause) for deleting the data: ")

        if (table_name or condition) == "abort" :
            print("Aborted")
        else :
            query = f"DELETE FROM {table_name} WHERE {condition}"
            cur.execute(query)

            conn.commit()
            print("Data deleted successfully")
    except psycopg2.Error as e:
        try:
            conn.rollback()
        except Exception:
            pass
        print("Error deleting data")
        print(e)
    finally:
        try:
            if cur is not None:
                cur.close()
        except Exception:
            pass


# Function to update data in the database
def update_data(conn):
    cur = None
    try:
        cur = conn.cursor()

        table_name = input("Table to update the data in: ")
        set_clause = input("SET clause (Ex: [Column1 = Value1, Column2 = Value2, ...]): ")
        condition = input("Condition for the update: ")

        if (table_name or set_clause or condition) == "abort" :
            print("Aborted")
        else :
            query = f"UPDATE {table_name} SET {set_clause} WHERE {condition}"
            cur.execute(query)

            conn.commit()
            print("Data updated successfully")
    except psycopg2.Error as e:
        try:
            conn.rollback()
        except Exception:
            pass
        print("Error updating data")
        print(e)
    finally:
        try:
            if cur is not None:
                cur.close()
        except Exception:
            pass


# Function to search data in the database
def search_data(conn):
    try:
        # select table to search for
        tables = execute_query(conn, QUERIES['get_tables'])
        if not tables:
            print("No tables returned or error occurred")
            return
        print("\nAvailable tables:")
        for t in tables:
            print(f"- {t[0]}")

        table_input = input("Select the table to search from: ")
        
        if table_input not in [t[0] for t in tables]:
            print(f"Error: Table '{table_input}' does not exist")
            print("Aborted")
            return

        # select field to search for
        fields = execute_query(conn, QUERIES['get_table_columns'].format(table_name=table_input))
        if fields is None:
            print("Error retrieving fields for the selected table")
            return
        print("\nAvailable fields:")
        for field in fields:
            print(f"- {field[0]}")        
            
        field_input = input("Field to search (blank for selecting all fields): ")

        if field_input and field_input not in [c[0] for c in fields]:
            print(f"Error: Field '{field_input}' does not exist in the table '{table_input}'")
            print("Aborted")
            return
        
        # Construct the search query
        if field_input == "":
            res = execute_query(conn, QUERIES['search_all'].format(table=table_input))
        else:
            valid_operators = ['=', '>', '<', '>=', '<=', '!=', 'LIKE']

            print(f"\nAvailable operators: {', '.join(valid_operators)}")
            operator_input = input("Enter operator: ").strip().upper()
            
            # Validate operator
            if operator_input not in valid_operators:
                print("Invalid operator")
                print("Aborted")
                return
                
            value_input = input("Enter search value: ")
            
            res = execute_query(conn, QUERIES['search_data'].format(table=table_input, field=field_input, operator=operator_input, value=value_input))
            
        if res:
            print("\nSearch results:")
            for row in res:
                print(row)
        else:
            print("\nNo matching records found")
    except psycopg2.Error as e:
        print("Error searching data")
        print(e)
    pass


# Function for aggregate functions
def aggregate_functions(conn):
    cur = None
    try:
        cur = conn.cursor()

        table_name = input("Table to use the aggregate functions on: ")
        column_name = input("Column for aggregation: ")
        function = input("Aggregate function to use (SUM, AVG, COUNT, MIN, MAX): ")

        if (table_name or column_name or function) == "abort" :
            print("Aborted")
        else : 
            query = f"SELECT {function}({column_name}) FROM {table_name}"
            cur.execute(query)
            result = cur.fetchone()

            if result:
                print(f"{function}({column_name}): {result[0]}")
            else:
                print("No data available for aggregation")
    except psycopg2.Error as e:
        try:
            conn.rollback()
        except Exception:
            pass
        print("Error performing aggregate function")
        print(e)
    finally:
        try:
            if cur is not None:
                cur.close()
        except Exception:
            pass

# Function for sorting
def sorting(conn):
    cur = None
    try:
        cur = conn.cursor()

        table_name = input("Table to sort the data: ")
        column_name = input("Column to sort: ")
        order = input("Sorting order (Ex: ASC, DESC): ")

        if (table_name or column_name or order) == "abort" :
            print("Aborted")
        else :
            query = f"SELECT * FROM {table_name} ORDER BY {column_name} {order}"
            cur.execute(query)
            rows = cur.fetchall()

            if rows:
                print("Sorted results:")
                for row in rows:
                    print(row)
            else:
                print("No data available to sort")
    except psycopg2.Error as e:
        try:
            conn.rollback()
        except Exception:
            pass
        print("Error sorting data")
        print(e)
    finally:
        try:
            if cur is not None:
                cur.close()
        except Exception:
            pass

# Function for joins
def joins(conn):
    cur = None
    try:
        cur = conn.cursor()

        table1_name = input("First table to join: ")
        table2_name = input("Second table to join: ")
        join_type = input("Join type: (JOIN, LEFT JOIN, RIGHT JOIN, FULL OUTER JOIN): ")
        join_condition = input("Join condition (Ex: table1.[column] = table2.[column]): ")

        if (table1_name or table2_name or join_condition) == "abort" :
            print("Aborted")
        else :
            if join_type == ('JOIN' or 'join') : 
                query = f"SELECT * FROM {table1_name} INNER JOIN {table2_name} ON {join_condition}"
            elif join_type == ('LEFT JOIN' or 'left join') : 
                query = f"SELECT * FROM {table1_name} LEFT JOIN {table2_name} ON {join_condition}"
            elif join_type == ('RIGHT JOIN' or 'right join') : 
                query = f"SELECT * FROM {table1_name} RIGHT JOIN {table2_name} ON {join_condition}"
            elif join_type == ('FULL OUTER JOIN' or 'full outer join') : 
                query = f"SELECT * FROM {table1_name} FULL OUTER JOIN {table2_name} ON {join_condition}"
            else :
                print("Wrong join type. Aborted")
            cur.execute(query)
            rows = cur.fetchall()

            if rows:
                print("Join results:")
                for row in rows:
                    print(row)
            else:
                print("No matching records found after join")
    except psycopg2.Error as e:
        try:
            conn.rollback()
        except Exception:
            pass
        print("Error performing join")
        print(e)
    finally:
        try:
            if cur is not None:
                cur.close()
        except Exception:
            pass

# Function for grouping
def grouping(conn):
    cur = None
    try:
        cur = conn.cursor()

        table_name = input("Table to perform GROUP BY clause: ")
        column_name = input("Column to GROUP BY: ")

        if (table_name or column_name) == "abort" :
            print("Aborted")
        else :
            query = f"SELECT {column_name}, COUNT(*) FROM {table_name} GROUP BY {column_name}"
            cur.execute(query)
            rows = cur.fetchall()

            if rows:
                print("Grouping results:")
                for row in rows:
                    print(row)
            else:
                print("No data available for grouping")
    except psycopg2.Error as e:
        try:
            conn.rollback()
        except Exception:
            pass
        print("Error performing grouping")
        print(e)
    finally:
        try:
            if cur is not None:
                cur.close()
        except Exception:
            pass

# Function for subqueries
def subqueries(conn):
    cur = None
    try:
        cur = conn.cursor()

        # Prompt the user to enter the main table name and column
        main_table = input("Table of the main query: ")
        main_column = input("Column of the main table: ")

        # Prompt the user to enter the subquery table name and column
        sub_table = input("Table of the subquery: ")
        sub_column = input("Column of the subquery table: ")

        if (main_table or main_column or sub_table or sub_column) == "abort" :
            print("Aborted")
        else :
            # Construct the subquery
            subquery = f"SELECT {sub_column} FROM {sub_table}"

            # Construct the main query with subquery
            main_query = f"SELECT * FROM {main_table} WHERE {main_column} IN ({subquery})"

            # Execute the main query and fetch its result
            cur.execute(main_query)
            main_result = cur.fetchall()

            if main_result:
                # Display the results of the main query
                print("Main Query Result:")
                for row in main_result:
                    print(row)
            else:
                print("Main query returned no results")
    except psycopg2.Error as e:
        try:
            conn.rollback()
        except Exception:
            pass
        print("Error executing subqueries")
        print(e)
    finally:
        try:
            if cur is not None:
                cur.close()
        except Exception:
            pass


### launch CLI interface ###
# Function to establish a connection to the PostgreSQL database
def connect():
    try:
        # Prefer PASSWORD environment variable; otherwise prompt the user securely
        password = getpass.getpass("PostgreSQL password: ")

        conn = psycopg2.connect(
            dbname="postgres",
            user="postgres",
            password=password,
            host="localhost",
            port="5432", # Default PostgreSQL port
        )
        print("Connected to the database successfully")
        return conn
    except psycopg2.Error as e:
        print("Unable to connect to the database")
        print(e)
        return None

# Main function to run the CLI interface
def main():
    conn = connect()
    if conn is None:
        return

    while True:
        print("\nWelcome to my CLI interface\n")
        print("Please select an option:")
        print("1. Insert Data")
        print("2. Delete Data")
        print("3. Update Data")
        print("4. Search Data")
        print("5. Aggregate Functions")
        print("6. Sorting")
        print("7. Joins")
        print("8. Grouping")
        print("9. Subqueries")
        print("10. Exit")

        choice = input("\nEnter your choice (1-10): ")

        match choice:
            case '1':
                insert_data(conn)
            case '2':
                delete_data(conn)
            case '3':
                update_data(conn)
            case '4':
                search_data(conn)
            case '5':
                aggregate_functions(conn)
            case '6':
                sorting(conn)
            case '7':
                joins(conn)
            case "8":
                grouping(conn)
            case "9":
                subqueries(conn)
            case "10":
                print("Exiting the CLI interface")
                break
            case _:
                print("Invalid choice. Please select a valid option.")

    conn.close()

if __name__ == "__main__":
    main()
