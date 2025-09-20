import pyodbc

###################################################################
# Datenbank Zugriff - Transportdaten ##############################
###################################################################

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
        print("Fehler beim Datenbankzugriff - Transportdaten:", e)
        return None

    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()

    # Terminal Ausgabe

        if transport_daten:
            print(f"{len(transport_daten)} Datensätze gefunden")
            # Datensatz: (ID, companyID, transportID, transportstationID, direction (Jahr, Monat, Tag, Stunde, Minute, Sekunde))
            for transport_datensatz in transport_daten:
                print(transport_datensatz)
        else:
            print("Keine Daten gefunden")
    

###################################################################
# Datenbank Zugriff - Temperaturdaten #############################
###################################################################

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
        print("Fehler beim Datenbankzugriff - Temperaturdaten:", e)
        return None

    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()

        # Terminal Ausgabe
    
        if temperatur_daten:
            print(f"{len(temperatur_daten)} Datensätze gefunden")
            # Datensatz: (ID (Jahr, Monat, Tag, Stunde, Minute) Temperatur)
            for temperatur_datensatz in temperatur_daten:
                print(temperatur_datensatz)
        else:
            print("Keine Daten gefunden")

###################################################################
# Datenbank Zugriff - Company-Daten ###############################
###################################################################

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
        print("Fehler beim Datenbankzugriff - Company Daten:", e)
        return None

    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()

        # Terminal Ausgabe
    
        if company_daten:
            print(f"{len(company_daten)} Datensätze gefunden")
            # Datensatz: (companyID, company, Straße, Ort, PLZ)
            for company_datensatz in company_daten:
                print(company_datensatz)
        else:
            print("Keine Daten gefunden")

