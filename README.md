# CMPSC431W-CLI
This project features a CLI (Command-Line Interface) that enables users to manage a database through command prompts.

It utilizes Python for connecting to the database and PostgreSQL for storing and managing the database.

---
How to use:
- Install PostgreSQL if you do not have one installed
- Clone this repository into your local directory
- Using pgAdmin4, register a new PostgreSQL server with server name, host name, and password
- Navigate to your server -> Databases -> postgres -> Schemas -> public. Right click the public tab, and click CREATE Script
- Copy and paste the SQL commands in StagingTables.sql inside the PSQL-commands folder, and execute the script
- Refresh the public tab (by right clicking) to confirm you have a Tables(9) tab
- Right click the Tables(9) tab, and open PSQL Tool
- Following the instruction in IMPORT.sql, edit the path to the CSV files, then copy and paste the sql commands into the PSQL Tool
- Return to the Script window, replace the existing commands with the SQL commands from CREATE.sql, then execute the script.\
- Replace the commands with those from INSERT.sql, then execute the script.
- Finally, replace the commands with those from DROP.sql, then execute the script.
- Once no errors are showing, run the project_CLI.py file
