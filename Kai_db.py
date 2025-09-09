import pyodbc

def get_connection():
    conn_str = (
        "DRIVER={ODBC Driver 17 for SQL Server};"
        "SERVER=sc-db-server.database.windows.net;"
        "DATABASE=supplychain;"
        "UID=rse;PWD=Pa$$w0rd"
    )
    return pyodbc.connect(conn_str)

def fetch_transport_data(transport_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM dbo.coolchain WHERE transportid = ?", transport_id)
    rows = cursor.fetchall()
    conn.close()
    return rows