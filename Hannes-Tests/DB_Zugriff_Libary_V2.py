import pyodbc

###################################################################
# Datenbank Zugriff - Transportdaten ##############################
###################################################################

def get_transport_daten(transportid, verbindungs_i):
# Holt alle Datensätze für eine Transport-ID als Dictionary #
    transport_daten = {}
    try:
        # Verbindung herstellen
        conn = pyodbc.connect(verbindungs_i)
        cursor = conn.cursor()

        # SQL-Abfrage
        abfrage = """
            SELECT * 
            FROM dbo.coolchain 
            WHERE transportid = ? 
            ORDER BY datetime
        """
        cursor.execute(abfrage, transportid)

        zeilen = cursor.fetchall()

        # Dictionary erstellen
        transport_daten = {}
        for idx, zeile in enumerate(zeilen, start=1):
            # Row ist ein pyodbc.Row -> in Liste konvertieren
            transport_daten[idx] = list(zeile)

        transport_daten_len = len(transport_daten)

        return transport_daten, transport_daten_len

    except Exception as e:
        print("Fehler beim Datenbankzugriff - Transportdaten:", e)
        return None

    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()
        
        # Terminal Ausgabe

        print(transport_daten)