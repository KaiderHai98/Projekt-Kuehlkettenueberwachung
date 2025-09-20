import pyodbc

def get_transport_daten(transportid, verbindungs_i):
    """Holt alle Datensätze für eine Transport-ID"""
    try:
        # Verbindung herstellen
        conn = pyodbc.connect(verbindungs_i)
        print("Verbindung erfolgreich hergestellt")

        # Cursor erzeugen
        cursor = conn.cursor()

        # SQL-Abfrage
        abfrage = """
            SELECT * 
            FROM dbo.coolchain 
            WHERE transportid = ? 
            ORDER BY datetime
        """
        cursor.execute(abfrage, transportid)

        transport_daten = cursor.fetchall()
        return transport_daten

    except Exception as e:
        print("Fehler beim Datenbankzugriff:", e)
        return None

    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()

def get_temperatur_daten(transportstationID, verbindungs_i):
    """Holt alle Datensätze für eine TransportstationID"""
    try:
        # Verbindung herstellen
        conn = pyodbc.connect(verbindungs_i)
        print("Verbindung erfolgreich hergestellt")

        # Cursor erzeugen
        cursor = conn.cursor()

        # SQL-Abfrage
        abfrage = """
            SELECT * 
            FROM dbo.tempdata 
            WHERE transportstationID = ? 
            ORDER BY datetime
        """
        cursor.execute(abfrage, transportstationID)

        temperatur_daten = cursor.fetchall()
        return temperatur_daten

    except Exception as e:
        print("Fehler beim Datenbankzugriff:", e)
        return None

    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()
        
def get_company_daten(companyID, verbindungs_i):
    """Holt alle Datensätze für eine TransportstationID"""
    try:
        # Verbindung herstellen
        conn = pyodbc.connect(verbindungs_i)
        print("Verbindung erfolgreich hergestellt")

        # Cursor erzeugen
        cursor = conn.cursor()

        # SQL-Abfrage
        abfrage = """
            SELECT * 
            FROM dbo.company 
            WHERE companyID = ?
        """
        cursor.execute(abfrage, companyID)

        company_daten = cursor.fetchall()
        return company_daten

    except Exception as e:
        print("Fehler beim Datenbankzugriff:", e)
        return None

    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()
