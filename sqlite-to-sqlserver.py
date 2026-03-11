import sqlite3
import pyodbc
import sys
from tqdm import tqdm

SQLITE_DB = sys.argv[1]

SQL_SERVER = "localhost"
SQL_DATABASE = "name_database" # Change this

conn_sqlite = sqlite3.connect(SQLITE_DB)
cursor_sqlite = conn_sqlite.cursor()

conn_sqlserver = pyodbc.connect(
    "DRIVER={ODBC Driver 17 for SQL Server};"
    "SERVER=localhost\\SQLEXPRESS;"
    "DATABASE=name_database;"  # Change this
    "Trusted_Connection=yes;"
)

cursor_sqlserver = conn_sqlserver.cursor()
cursor_sqlserver.fast_executemany = True

# obtener tablas
cursor_sqlite.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor_sqlite.fetchall()

BATCH_SIZE = 5000

for table in tables:
    table = table[0]
    print(f"\nMigrando tabla: {table}")

    # obtener columnas
    cursor_sqlite.execute(f"PRAGMA table_info({table})")
    columns = cursor_sqlite.fetchall()

    col_defs = []
    col_names = []

    for col in columns:
        name = col[1]
        type_sqlite = col[2].upper()

        if "INT" in type_sqlite:
            type_sqlserver = "INT"
        elif "CHAR" in type_sqlite or "TEXT" in type_sqlite:
            type_sqlserver = "NVARCHAR(MAX)"
        elif "REAL" in type_sqlite or "FLOA" in type_sqlite:
            type_sqlserver = "FLOAT"
        else:
            type_sqlserver = "NVARCHAR(MAX)"

        col_defs.append(f"[{name}] {type_sqlserver}")
        col_names.append(name)

    create_table = f"""
    IF OBJECT_ID('{table}', 'U') IS NULL
    CREATE TABLE [{table}] (
        {', '.join(col_defs)}
    )
    """

    cursor_sqlserver.execute(create_table)
    conn_sqlserver.commit()

    # contar filas
    cursor_sqlite.execute(f"SELECT COUNT(*) FROM {table}")
    total_rows = cursor_sqlite.fetchone()[0]

    print(f"Total filas: {total_rows}")

    # obtener datos
    cursor_sqlite.execute(f"SELECT * FROM {table}")

    placeholders = ",".join(["?"] * len(col_names))
    insert_sql = f"INSERT INTO [{table}] ({','.join(col_names)}) VALUES ({placeholders})"

    with tqdm(total=total_rows, desc=f"Insertando {table}", unit="rows") as pbar:

        while True:
            rows = cursor_sqlite.fetchmany(BATCH_SIZE)
            if not rows:
                break

            cursor_sqlserver.executemany(insert_sql, rows)
            conn_sqlserver.commit()

            pbar.update(len(rows))

print("\nMigración completa")