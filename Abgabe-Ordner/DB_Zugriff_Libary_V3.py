###############################################################################################################
## Libary: CoolChainProjekt
#  Datei: Verarbeitung_Libary_V3.py
#
# Version: 3 vom: 07.10.2025
# Autoren: Josie Woeste, Hannes Ruhe, Kai Meiners
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

    '''
    @brief Liest Transportdaten aus der Datenbanktabelle *coolchain* anhand einer gegebenen Transport-ID.
    @details 
    Die Funktion stellt eine Verbindung zur angegebenen SQL-Datenbank her, führt eine Abfrage auf der Tabelle 
    *dbo.coolchain* aus und sammelt alle Datensätze mit der passenden Transport-ID.  
    Die Ergebnisse werden nach dem Zeitstempel (*datetime*) sortiert und als Dictionary zurückgegeben, 
    wobei der Schlüssel dem laufenden Index (beginnend bei 1) entspricht und der Wert eine Liste der Spaltenwerte ist.  
    Zusätzlich wird die Gesamtanzahl der gefundenen Datensätze ermittelt.  
    Bei einem Fehler wird eine Fehlermeldung ausgegeben und ein leeres Dictionary zurückgegeben.  
    Die Datenbankverbindung sowie der Cursor werden am Ende der Funktion zuverlässig geschlossen.
    '''

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

    '''
    @brief Liest Temperaturdaten zu Transportstationen aus der Tabelle *tempdata* basierend auf Transportdaten.
    @details 
    Die Funktion nutzt zuvor geladene Transportdaten, um für jede Station und jeden "Check-in"-Zeitpunkt 
    (*Status = 'in'*) die zugehörigen Temperaturmessungen aus der Tabelle *dbo.tempdata* abzurufen.  
    Dabei wird jeweils der Zeitraum zwischen dem "in"- und dem nächsten "out"-Eintrag derselben Station berücksichtigt.  
    Fehlt ein "out"-Eintrag, werden alle Messungen ab dem Startzeitpunkt einbezogen.  

    Die Ergebnisse werden als Dictionary mit fortlaufendem Index (beginnend bei 1) gespeichert, 
    wobei jede Zeile als Liste der Spaltenwerte vorliegt. Zusätzlich wird die Gesamtanzahl der gefundenen 
    Temperaturdatensätze zurückgegeben.  

    Bei einem Fehler im Datenbankzugriff wird eine Fehlermeldung ausgegeben und ein leeres Dictionary zurückgegeben.  
    Die Datenbankverbindung und der Cursor werden im `finally`-Block zuverlässig geschlossen.
    '''

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

def get_company_daten(transport_daten, verbindungs_i):#
    
    '''
    @brief Liest Firmendaten aus der Tabelle *company* basierend auf den in den Transportdaten enthaltenen Company-IDs.
    @details 
    Die Funktion extrahiert alle eindeutigen Company-IDs aus den übergebenen Transportdaten und 
    ruft für jede ID die zugehörigen Datensätze aus der Tabelle *dbo.company* ab.  
    Jede gefundene Zeile wird als Liste der Spaltenwerte in einem Dictionary gespeichert, 
    wobei der Schlüssel ein fortlaufender Index (beginnend bei 1) ist.  

    Zusätzlich wird die Gesamtanzahl der gefundenen Firmendatensätze zurückgegeben.  
    Bei einem Fehler im Datenbankzugriff wird eine Fehlermeldung ausgegeben und ein leeres Dictionary 
    sowie die Länge 0 zurückgegeben.  
    Die Datenbankverbindung und der Cursor werden im `finally`-Block zuverlässig geschlossen.
    '''

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

    '''
    @brief Liest Daten zu Transportstationen aus der Tabelle *transportstation* anhand der in den Transportdaten enthaltenen Station-IDs.
    @details 
    Die Funktion extrahiert alle eindeutigen Transportstations-IDs aus den übergebenen Transportdaten 
    und ruft für jede ID die zugehörigen Datensätze aus der Tabelle *dbo.transportstation* ab.  
    Jede gefundene Zeile wird als Liste der Spaltenwerte in einem Dictionary gespeichert, 
    wobei der Schlüssel ein fortlaufender Index (beginnend bei 1) ist.  

    Zusätzlich wird die Gesamtanzahl der gefundenen Transportstationsdatensätze zurückgegeben.  
    Bei einem Fehler im Datenbankzugriff wird eine Fehlermeldung ausgegeben und ein leeres Dictionary 
    sowie die Länge 0 zurückgegeben.  
    Die Datenbankverbindung und der Cursor werden im `finally`-Block zuverlässig geschlossen.
    '''

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


