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

        if transport_daten:
            # Datensatz-Aufbau: (ID, CompanyID, TransportID, TransportstationID, direction (Jahr, Monat, Tag, Stunde, Minute, Sekunde))
            print("######### Transport-Daten #########")
            print(f"{transport_daten_len} Datensätze gefunden")
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
        temoratur_daten_len = len(temperatur_daten) 
        return temperatur_daten, temoratur_daten_len

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
            # Datensatz-Aufbau: (ID (Jahr, Monat, Tag, Stunde, Minute) Temperatur)
            print("######### Temperatur-Daten #########")
            print(f"{temoratur_daten_len} Datensätze gefunden")
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
        company_daten_len = len(company_daten)
        return company_daten, company_daten_len

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
            # Datensatz-Aufbau: (CompanyID, Company, Straße, Ort, PLZ)
            print("######### Company-Daten #########")
            print(f"{company_daten_len} Datensätze gefunden")
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
        transportstation_daten_len = len(transportstation_daten)
        return transportstation_daten, transportstation_daten_len

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
            # Datensatz-Aufbau: (TransportstationID, Transportstation, Kategorie, PLZ)
            print("######### Transportstation-Daten #########")
            print(f"{transportstation_daten_len} Datensätze gefunden")
            for transportstation_datensatz in transportstation_daten:
                print(transportstation_datensatz)
            print("##########################################")
        else:
            print("Keine Transportstations-Daten gefunden")
