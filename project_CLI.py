import psycopg2

# Function to establish a connection to the PostgreSQL database
def connect():
    try:
        conn = psycopg2.connect(
            dbname="postgres",
            user="postgres",
            password="dydwls51", # Replace with your PostgreSQL password
            host="localhost",
            port="5432", # Default PostgreSQL port
        )
        print("Connected to the database successfully")
        return conn
    except psycopg2.Error as e:
        print("Unable to connect to the database")
        print(e)
        return None

# Function to execute a query and fetch all results
def execute_query(conn, query):
    try:
        cur = conn.cursor()
        cur.execute(query)
        rows = cur.fetchall()
        return rows
    except psycopg2.Error as e:
        print("Error executing query")
        print(e)
        return None

# Function to insert data into the database
def insert_data(conn):
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
        conn.rollback()
        print("Error inserting data")
        print(e)
    pass

# Function to delete data from the database
def delete_data(conn):
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
        conn.rollback()
        print("Error deleting data")
        print(e)
    pass


# Function to update data in the database
def update_data(conn):
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
        conn.rollback()
        print("Error updating data")
        print(e)
    pass


# Function to search data in the database
def search_data(conn):
    try:
        cur = conn.cursor()

        # Show available tables
        cur.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public' 
            AND table_type = 'BASE TABLE'
        """)
        tables = cur.fetchall()
        
        print("\nAvailable tables:")
        for table in tables:
            print(f"- {table[0]}")
        print()

        table_name = input("Select the table to search from: ")
        
        if table_name not in [t[0] for t in tables]:
            print("Aborted")
            return

        # Show available columns in the selected table
        cur.execute(f"""
            SELECT column_name, data_type 
            FROM information_schema.columns 
            WHERE table_name = '{table_name}'
        """)
        columns = cur.fetchall()
        
        if columns:
            print(f"\nAvailable fields in {table_name}:")
            for col in columns:
                print(f"- {col[0]}")
            print()
        
        field_name = input("Field to search (blank for selecting all fields): ")

        if field_name and field_name not in [c[0] for c in columns]:
            print(f"Error: Field '{field_name}' does not exist in table '{table_name}'")
            return
        
        # Construct the search query
        if field_name == "":
            query = f"SELECT * FROM {table_name}"
            cur.execute(query)
        else:
            print("\nAvailable operators: =, >, <, >=, <=, !=, LIKE")
            operator = input("Enter operator: ").strip().upper()
            
            # Validate operator
            valid_operators = ['=', '>', '<', '>=', '<=', '!=', 'LIKE']
            if operator not in valid_operators:
                print("Invalid operator")
                return
                
            value = input("Enter search value: ")
            
            # Use parameterized query to prevent SQL injection
            query = f"SELECT * FROM {table_name} WHERE {field_name} {operator} %s"
            cur.execute(query, (value,))
            
        rows = cur.fetchall()
        
        if rows:
            print("\nSearch results:")
            for row in rows:
                print(row)
        else:
            print("\nNo matching records found")
    except psycopg2.Error as e:
        print("Error searching data")
        print(e)
    pass


# Function for aggregate functions
def aggregate_functions(conn):
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
        print("Error performing aggregate function")
        print(e)
    pass

# Function for sorting
def sorting(conn):
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
        print("Error sorting data")
        print(e)
    pass

# Function for joins
def joins(conn):
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
        print("Error performing join")
        print(e)
    pass

# Function for grouping
def grouping(conn):
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
        print("Error performing grouping")
        print(e)
    pass

# Function for subqueries
def subqueries(conn):
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
        print("Error executing subqueries")
        print(e)
    pass

# Function for transactions
def transactions(conn):
    try:
        cur = conn.cursor()

        # Begin the transaction
        print("Transaction started")
        cur.execute("BEGIN TRANSACTION;")
        query = ''

        # Example of operations within the transaction
        # You can replace this with your actual transaction operations
        # For example:
        # cur.execute("INSERT INTO TableName (Column1, Column2) VALUES (%s, %s)", (value1, value2))
        # cur.execute("UPDATE TableName SET Column1 = %s WHERE Condition", (new_value,))
        # cur.execute("DELETE FROM TableName WHERE Condition")
        
        while 1 :
            print("\nSelect operation\n")
            print("1. Insert Data")
            print("2. Delete Data")
            print("3. Update Data")
            print("4. Search Data")
            print("5. Aggregate Functions")
            print("6. Sorting")
            print("7. Commit")
            choice = input("\nEnter your choice (1-7): ")

            if choice == "1":
                table_name = input("Table to insert data into: ")
                columns_str = input("Column(s) to insert data into (separated by comma): ")
                values_str = input("Value(s) to insert into (separated by comma): ")

                if (table_name or columns_str or values_str) == "abort" :
                    print("Aborted")
                else :
                    query += f"INSERT INTO {table_name} ({columns_str}) VALUES ({values_str}); "
            elif choice == "2":
                table_name = input("Table to delete from: ")
                condition = input("Condition (WHERE clause) for deleting the data: ")

                if (table_name or condition) == "abort" :
                    print("Aborted")
                else :
                    query += f"DELETE FROM {table_name} WHERE {condition}; "
            elif choice == "3":
                table_name = input("Table to update the data in: ")
                set_clause = input("SET clause (Ex: [Column1 = Value1, Column2 = Value2, ...]): ")
                condition = input("Condition for the update: ")

                if (table_name or set_clause or condition) == "abort" :
                    print("Aborted")
                else :
                    query += f"UPDATE {table_name} SET {set_clause} WHERE {condition}; "
            elif choice == "4":
                table_name = input("Table to search the data from: ")
                condition = input("Condition for searching (blank if WHERE clause is not desired): ")

                if (table_name or condition) == "abort" :
                    print("Aborted")
                else :
                    if condition:
                        query += f"SELECT * FROM {table_name} WHERE {condition}; "
                    else:
                        query += f"SELECT * FROM {table_name}; "
            elif choice == "5":
                table_name = input("Table to use the aggregate functions on: ")
                column_name = input("Column for aggregation: ")
                function = input("Aggregate function to use (SUM, AVG, COUNT, MIN, MAX): ")

                if (table_name or column_name or function) == "abort" :
                    print("Aborted")
                else : 
                    query += f"SELECT {function}({column_name}) FROM {table_name}; "
            elif choice == "6":
                table_name = input("Table to sort the data: ")
                column_name = input("Column to sort: ")
                order = input("Sorting order (Ex: ASC, DESC): ")

                if (table_name or column_name or order) == "abort" :
                    print("Aborted")
                else :
                    query += f"SELECT * FROM {table_name} ORDER BY {column_name} {order}; "
            elif choice == "7":
                print("Committing")
                cur.execute(query + f"COMMIT;")
                #conn.commit()
                break
            else :
                print("Invalid choice. Please select a valid option.")

        # Commit the transaction
        conn.commit()
        print("Transaction committed successfully")

    except psycopg2.Error as e:
        # Rollback the transaction in case of error
        conn.rollback()
        print("Error executing transaction. Rolling back.")
        print(f"Error: {e}")
    except Exception as e:
        # Handle unexpected exceptions
        conn.rollback()
        print("Unexpected error occurred. Rolling back.")
        print(f"Error: {e}")
    finally:
        # Close the cursor and connection
        cur.close()
        conn.close()
    pass

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
        print("10. Transactions")
        print("11. Exit")

        choice = input("\nEnter your choice (1-11): ")

        if choice == "1":
            insert_data(conn)
        elif choice == "2":
            delete_data(conn)
        elif choice == "3":
            update_data(conn)
        elif choice == "4":
            search_data(conn)
        elif choice == "5":
            aggregate_functions(conn)
        elif choice == "6":
            sorting(conn)
        elif choice == "7":
            joins(conn)
        elif choice == "8":
            grouping(conn)
        elif choice == "9":
            subqueries(conn)
        elif choice == "10":
            transactions(conn)
        elif choice == "11":
            print("Exiting the CLI interface")
            break
        else:
            print("Invalid choice. Please select a valid option.")

    conn.close()

if __name__ == "__main__":
    main()
