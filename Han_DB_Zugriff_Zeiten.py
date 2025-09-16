import pyodbc

# Variablen
server = 'sc-db-server.database.windows.net'
database = 'supplychain'
username = 'rse'
password = 'Pa$$w0rd'

# Verbindung
conn_str = (
    f"DRIVER={{ODBC Driver 18 for SQL Server}};"
    f"SERVER={server};"
    f"DATABASE={database};"
    f"UID={username};"
    f"PWD={password}"
)


def get_transport_daten(transport_id: str):
    """Holt alle Datensätze für eine Transport-ID"""
    try:
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()

        abfrage = """
            SELECT * 
            FROM dbo.coolchain 
            WHERE transportid = ? 
            ORDER BY datetime
        """
        cursor.execute(abfrage, transport_id)

        daten = cursor.fetchall()
        return daten

    except Exception as e:
        print("Fehler beim Datenbankzugriff:", e)
        return None

    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()

def get_temperatur_daten(transportstationID: str):
    """Holt alle Datensätze für eine Transport-ID"""
    try:
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()

        abfrage = """
            SELECT * 
            FROM dbo.coolchain 
            WHERE transportstationID = ? 
            ORDER BY datetime
        """
        cursor.execute(abfrage, transportstationID)

        daten = cursor.fetchall()
        return daten

    except Exception as e:
        print("Fehler beim Datenbankzugriff:", e)
        return None

    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()
