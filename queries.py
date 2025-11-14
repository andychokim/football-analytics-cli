QUERIES = {
    'get_tables': """
        SELECT table_name 
        FROM information_schema.tables 
        WHERE table_schema = 'public' 
        AND table_type = 'BASE TABLE'
    """,
    
    'get_table_columns': """
        SELECT column_name, data_type 
        FROM information_schema.columns 
        WHERE table_name = '{table_name}'
    """,

    'search_all': "SELECT * FROM {table}",
    
    'insert_data': "INSERT INTO {table} ({columns}) VALUES ({values})",
    
    'search_data': "SELECT * FROM {table} WHERE {field} {operator} {value}",
}