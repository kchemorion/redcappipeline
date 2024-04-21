import pyodbc
import pandas as pd
import sqlite3

# Connect to Access database
db_file = r'HOLOA_off_line_FINAL.accdb'
conn_str = 'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=' + db_file
conn = pyodbc.connect(conn_str)

# Connect to SQLite database (it will be created if it doesn't exist)
sqlite_conn = sqlite3.connect('your_database_name.db')

# Function to copy all tables
def export_tables():
    cursor = conn.cursor()
    cursor.execute("SELECT Name FROM MSysObjects WHERE Type IN (1,4) AND Name NOT LIKE 'MSys%'")
    tables = [row.Name for row in cursor]

    for table in tables:
        print(f'Exporting {table}')
        df = pd.read_sql(f'SELECT * FROM [{table}]', conn)
        df.to_sql(table, sqlite_conn, if_exists='replace', index=False)
    cursor.close()

export_tables()

# Close connections
conn.close()
sqlite_conn.close()
