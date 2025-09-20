import pyodbc

###################################################################
# Datenbank Zugriff - Transportdaten ##############################
###################################################################

def get_transport_daten(transportid, verbindungs_i):
    """Holt alle Datensätze für eine Transport-ID"""
    try:
        # Verbindung herstellen
        conn = pyodbc.connect(verbindungs_i)

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
            print("######### Transport-Daten #########")
            print(f"{len(transport_daten)} Datensätze gefunden")
            # Datensatz: (ID, CompanyID, TransportID, TransportstationID, direction (Jahr, Monat, Tag, Stunde, Minute, Sekunde))
            for transport_datensatz in transport_daten:
                print(transport_datensatz)
            print("###################################")
        else:
            print("Keine Transport-Daten gefunden")
    

###################################################################
# Datenbank Zugriff - Temperaturdaten #############################
###################################################################

def get_temperatur_daten(transportstationID, verbindungs_i):
    """Holt alle Datensätze für eine TransportstationID"""
    try:
        # Verbindung herstellen
        conn = pyodbc.connect(verbindungs_i)

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
            print("######### Temperatur-Daten #########")
            print(f"{len(temperatur_daten)} Datensätze gefunden")
            # Datensatz: (ID (Jahr, Monat, Tag, Stunde, Minute) Temperatur)
            for temperatur_datensatz in temperatur_daten:
                print(temperatur_datensatz)
            print("####################################")
        else:
            print("Keine Temperatur-Daten gefunden")

###################################################################
# Datenbank Zugriff - Company-Daten ###############################
###################################################################

def get_company_daten(companyID, verbindungs_i):
    """Holt alle Datensätze für eine TransportstationID"""
    try:
        # Verbindung herstellen
        conn = pyodbc.connect(verbindungs_i)

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
            print("######### Company-Daten #########")
            print(f"{len(company_daten)} Datensätze gefunden")
            # Datensatz: (CompanyID, Company, Straße, Ort, PLZ)
            for company_datensatz in company_daten:
                print(company_datensatz)
            print("#################################")
        else:
            print("Keine Company-Daten gefunden")

###################################################################
# Datenbank Zugriff - Transportstations-Daten #####################
###################################################################

def get_transportstation_daten(transportstationID, verbindungs_i):
    """Holt alle Datensätze für eine TransportstationID"""
    try:
        # Verbindung herstellen
        conn = pyodbc.connect(verbindungs_i)

        # Cursor erzeugen
        cursor = conn.cursor()

        # SQL-Abfrage
        abfrage = """
            SELECT * 
            FROM dbo.transportstation 
            WHERE transportstationID = ?
        """
        cursor.execute(abfrage, transportstationID)

        transportstation_daten = cursor.fetchall()
        return transportstation_daten

    except Exception as e:
        print("Fehler beim Datenbankzugriff - transportstation Daten:", e)
        return None

    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()

        # Terminal Ausgabe
    
        if transportstation_daten:
            print("######### Transportstation-Daten #########")
            print(f"{len(transportstation_daten)} Datensätze gefunden")
            # Datensatz: (TransportstationID, Transportstation, Kategorie, PLZ)
            for transportstation_datensatz in transportstation_daten:
                print(transportstation_datensatz)
            print("##########################################")
        else:
            print("Keine Transportstations-Daten gefunden")
