###############################################################################################################
## Libary: CoolChainProjekt
#  Datei: Verarbeitung_Libary_V3.py
#
# Version: 3 vom: 21.09.2025
# Autoren:
#
# Zugehöriges Hauptprogramm:
# - Hauptprogramm_V3.py
# 
#
# Funktionsbeschreibung: 
# Libary zur einholung der Datenbankdaten
###############################################################################################################

import pyodbc

###################################################################
# Datenbank Zugriff - Transportdaten ##############################
###################################################################

def get_transport_daten(transportid, verbindungs_i):

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

        for idx, zeile in enumerate(zeilen, start=1):
            # Row ist ein pyodbc.Row -> in Liste konvertieren
            transport_daten[idx] = list(zeile)

        transport_daten_len = len(transport_daten)
        return transport_daten, transport_daten_len

    except Exception as e:
        print("Fehler beim Datenbankzugriff - Transportdaten:", e)
        return {}

    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()
        
        print(transport_daten)
    

###################################################################
# Datenbank Zugriff - Temperaturdaten #############################
###################################################################

def get_temperatur_daten(transport_daten, verbindungs_i):

    temperatur_daten = {}

    try:
        conn = pyodbc.connect(verbindungs_i)
        cursor = conn.cursor()

        # SQL-Abfragen
        sql_ohne_end = """
            SELECT *
            FROM dbo.tempdata
            WHERE transportstationID = ?
              AND datetime >= ?
            ORDER BY datetime
        """
        sql_mit_end = """
            SELECT *
            FROM dbo.tempdata
            WHERE transportstationID = ?
              AND datetime >= ?
              AND datetime < ?
            ORDER BY datetime
        """

        # Reihenfolge sicherstellen (dein transport_daten kommt i. d. R. schon sortiert)
        items = sorted(transport_daten.items(), key=lambda kv: kv[0])

        idx = 1
        for pos, (_, eintrag) in enumerate(items):
            station_id = eintrag[3]
            status_raw = str(eintrag[4])           # z.B. "'in'"
            status = status_raw.strip().strip("'").lower()
            start_dt = eintrag[5]

            # Nur wenn Ware eingecheckt ist
            if status != "in":
                continue

            # Nächsten 'out' für dieselbe Station suchen
            end_dt = None
            for _, next_entry in items[pos+1:]:
                if next_entry[3] == station_id:
                    next_status = str(next_entry[4]).strip().strip("'").lower()
                    if next_status == "out":
                        end_dt = next_entry[5]
                        break

            # Abfrage ausführen (mit oder ohne Endzeit)
            if end_dt is None:
                cursor.execute(sql_ohne_end, station_id, start_dt)
            else:
                cursor.execute(sql_mit_end, station_id, start_dt, end_dt)

            zeilen = cursor.fetchall()
            for zeile in zeilen:
                temperatur_daten[idx] = list(zeile)
                idx += 1

        temperatur_daten_len = len(temperatur_daten)
        return temperatur_daten, temperatur_daten_len

    except Exception as e:
        print("Fehler beim Datenbankzugriff - Temperaturdaten:", e)
        return {}

    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()

        print(temperatur_daten)


###################################################################
# Datenbank Zugriff - Company-Daten ###############################
###################################################################

def get_company_daten(transport_daten, verbindungs_i):

    company_daten = {}

    try:
        conn = pyodbc.connect(verbindungs_i)
        cursor = conn.cursor()

        sql = """
            SELECT *
            FROM dbo.company
            WHERE companyID = ?
        """

        # Eindeutige companyIDs aus transport_daten (Index 1 = zweite Spalte)
        company_ids = {eintrag[1] for eintrag in transport_daten.values()}

        idx = 1
        for companyID in company_ids:
            cursor.execute(sql, companyID)
            zeilen = cursor.fetchall()
            for zeile in zeilen:
                company_daten[idx] = list(zeile)
                idx += 1

        company_daten_len = len(company_daten)
        return company_daten, company_daten_len

    except Exception as e:
        print("Fehler beim Datenbankzugriff - Company Daten:", e)
        return {}, 0

    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()
        print(company_daten)  # optional


###################################################################
# Datenbank Zugriff - Transportstations-Daten #####################
###################################################################

def get_transportstation_daten(transport_daten, verbindungs_i):

    transportstation_daten = {}

    try:
        conn = pyodbc.connect(verbindungs_i)
        cursor = conn.cursor()

        sql = """
            SELECT *
            FROM dbo.transportstation
            WHERE transportstationID = ?
        """

        # Eindeutige transportstationIDs aus transport_daten (Index 3 = 4. Spalte)
        station_ids = {eintrag[3] for eintrag in transport_daten.values()}

        idx = 1
        for transportstationID in station_ids:
            cursor.execute(sql, transportstationID)
            zeilen = cursor.fetchall()
            for zeile in zeilen:
                transportstation_daten[idx] = list(zeile)
                idx += 1

        transportstation_daten_len = len(transportstation_daten)
        return transportstation_daten, transportstation_daten_len

    except Exception as e:
        print("Fehler beim Datenbankzugriff - transportstation Daten:", e)
        return {}, 0

    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()

        print(transportstation_daten)


