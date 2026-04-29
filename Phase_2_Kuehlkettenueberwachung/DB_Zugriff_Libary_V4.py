# ###############################################################################################################
## Libary: CoolChainProjekt
#  Datei: DB_Zugriff_Libary_V4.py
#
# Version: 4 vom: 21.04.2026
# Autoren: Josie Woeste, Hannes Ruhe, Kai Meiners
#
# Zugehöriges Hauptprogramm:
# - Hauptprogramm_V4.py
# 
# Funktionsbeschreibung: 
# Libary zur einholung der Datenbankdaten
# ###############################################################################################################

from datetime import timedelta
import pyodbc
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

###################################################################
# Initialisierung #################################################
###################################################################



###################################################################
# Hilfsfunktionen #################################################
###################################################################

# def decrypt_value(encrypted_data):

###################################################################
# Datenbank Zugriff - Transportdaten ##############################
###################################################################

def get_transport_daten(transportid, verbindungs_i):

    '''
    @brief Liest alle Bewegungsdaten eines Transports aus der Tabelle *coolchain*.
    @details
    Diese Funktion holt die eigentlichen Ablaufdaten eines Transports aus der Datenbank.
    Gemeint sind die Ein- und Auscheck-Vorgänge der Ware an den verschiedenen Stationen.

    Was an dieser Stelle passiert:
    - Es wird eine Verbindung zur SQL-Datenbank aufgebaut.
    - Danach wird mit einem SELECT-Befehl nach genau der Transport-ID gesucht,
      die der Benutzer eingegeben hat.
    - Die Datensätze werden zeitlich nach *datetime* sortiert geladen.
    - Anschließend läuft eine for-Schleife über alle gefundenen Zeilen.
      Jede Zeile wird in eine Liste umgewandelt und in einem Dictionary gespeichert.

    Wie das Programm das grob handhabt:
    - Das Dictionary bekommt fortlaufende Schlüssel 1, 2, 3, ...
    - Dadurch kann die Verarbeitung später einfach über alle Bewegungen iterieren.
    - Die zeitliche Sortierung ist sehr wichtig, weil die Prüfungen nur dann sinnvoll
      funktionieren, wenn die Ereignisse in der tatsächlichen Reihenfolge vorliegen.

    Warum das gebraucht wird:
    - Diese Daten sind die Grundlage fast aller Prüfungen im Projekt:
      Übergabezeit, Transportdauer, Reihenfolgefehler, fehlende Auscheck-Vorgänge
      und ähnliche Auffälligkeiten.
    - Ohne diese Funktion gäbe es keine Transporthistorie, die geprüft werden könnte.

    @param transportid Zu prüfende Transport-ID.
    @param verbindungs_i SQL-Verbindungsstring für pyodbc.
    @return Tuple aus Dictionary mit Transportdaten und Anzahl der Datensätze.
    '''

    transport_daten = {}

    try:
        conn = pyodbc.connect(verbindungs_i)
        cursor = conn.cursor()

        abfrage = """
            SELECT *
            FROM dbo.coolchain
            WHERE transportID = ?
            ORDER BY datetime
        """
        cursor.execute(abfrage, transportid)

        zeilen = cursor.fetchall()

        for idx, zeile in enumerate(zeilen, start=1):
            transport_daten[idx] = list(zeile)

        transport_daten_len = len(transport_daten)
        return transport_daten, transport_daten_len

    except Exception as e:
        print("Fehler beim Datenbankzugriff - Transportdaten:", e)
        return {}, 0

    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()

        print(transport_daten)

###################################################################
# Datenbank Zugriff - Temperaturdaten #############################
###################################################################

# def get_temperatur_daten(transport_daten, verbindungs_i):

###################################################################
# Datenbank Zugriff - Company-Daten ###############################
###################################################################

def get_company_daten(transport_daten, verbindungs_i):

    '''
    @brief Liest die verschlüsselten Firmendaten aus *company_crypt* und entschlüsselt sie sofort.
    @details
    Diese Funktion kümmert sich um die Stammdaten der Firma, die zum Transport gehört.
    Die Tabelle enthält die Werte verschlüsselt. Deshalb reicht ein normales Auslesen
    allein nicht aus.

    Was an dieser Stelle passiert:
    - Aus den Transportdaten werden zuerst alle benötigten Company-IDs gesammelt.
    - Danach läuft eine for-Schleife über diese IDs.
    - Für jede ID wird der passende Datensatz aus *company_crypt* geladen.
    - Die einzelnen Felder wie Firmenname, Straße, Ort und PLZ werden anschließend
      nacheinander mit *decrypt_value()* entschlüsselt.
    - Die lesbaren Werte werden danach in einem Dictionary gespeichert.

    Wie das Programm das grob handhabt:
    - Die Funktion trennt also die technische Aufgabe „Daten holen“ von der
      fachlichen Aufgabe „Daten lesbar machen“ nicht vollständig,
      sondern erledigt beides direkt hintereinander.
    - Dadurch bekommt der restliche Programmablauf sofort Klartextdaten
      und muss sich später nicht mehr mit Bytewerten oder Entschlüsselung befassen.

    Warum das gebraucht wird:
    - Die Phase 2 verlangt, dass die verschlüsselten Stammdaten verarbeitet werden können.
    - Diese Funktion stellt sicher, dass spätere Programmteile mit normalen,
      verständlichen Firmendaten weiterarbeiten können.

    @param transport_daten Bereits geladene Bewegungsdaten des Transports.
    @param verbindungs_i SQL-Verbindungsstring für pyodbc.
    @return Tuple aus Dictionary mit entschlüsselten Firmendaten und Anzahl der Datensätze.
    '''

    company_daten = {}

    try:
        conn = pyodbc.connect(verbindungs_i)
        cursor = conn.cursor()

        sql = """
            SELECT companyID, company, strasse, ort, plz
            FROM dbo.company_crypt
            WHERE companyID = ?
        """

        company_ids = {eintrag[1] for eintrag in transport_daten.values()}

        idx = 1
        for companyID in company_ids:
            cursor.execute(sql, companyID)
            zeilen = cursor.fetchall()
            for zeile in zeilen:
                companyID, encrypted_company, encrypted_strasse, encrypted_ort, encrypted_plz = zeile

                decrypted_company = decrypt_value(encrypted_company)
                decrypted_strasse = decrypt_value(encrypted_strasse)
                decrypted_ort = decrypt_value(encrypted_ort)
                decrypted_plz = decrypt_value(encrypted_plz)

                company_daten[idx] = [
                    companyID,
                    decrypted_company,
                    decrypted_strasse,
                    decrypted_ort,
                    decrypted_plz,
                ]
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
        print(company_daten)

###################################################################
# Datenbank Zugriff - Transportstations-Daten #####################
###################################################################

def get_transportstation_daten(transport_daten, verbindungs_i):

    '''
    @brief Liest die verschlüsselten Stationsdaten aus *transportstation_crypt* und entschlüsselt sie.
    @details
    Diese Funktion beschafft die Stammdaten der Kühlstationen, die im Transport vorkommen.
    Dazu gehören vor allem Stationsname, Stationsart und Postleitzahl.

    Was an dieser Stelle passiert:
    - Aus den Bewegungsdaten werden zuerst alle benötigten Stations-IDs gesammelt.
    - Danach läuft eine for-Schleife über diese IDs.
    - Für jede Station wird der Datensatz aus *transportstation_crypt* geladen.
    - Anschließend werden Stationsname, Kategorie und PLZ entschlüsselt.
    - Die lesbaren Informationen werden wieder in einem Dictionary abgelegt.

    Wie das Programm das grob handhabt:
    - Die Funktion wandelt verschlüsselte Daten frühzeitig in Klartext um.
    - Dadurch können spätere Prüfschritte ganz normal mit Stationsnamen,
      Kategorien wie *GVZ* oder *KT* und Postleitzahlen arbeiten.

    Warum das gebraucht wird:
    - Die Verarbeitungslogik benötigt die Stationsart, um z. B. Reihenfolgefehler
      zwischen Kühltransporter und Kühllager zu erkennen.
    - Die Postleitzahl wird später für die Wetterabfrage gebraucht.
    - Der Stationsname wird benötigt, damit Fehlermeldungen für den Benutzer verständlich sind.

    @param transport_daten Bereits geladene Bewegungsdaten des Transports.
    @param verbindungs_i SQL-Verbindungsstring für pyodbc.
    @return Tuple aus Dictionary mit entschlüsselten Stationsdaten und Anzahl der Datensätze.
    '''

    transportstation_daten = {}

    try:
        conn = pyodbc.connect(verbindungs_i)
        cursor = conn.cursor()

        sql = """
            SELECT transportstationID, transportstation, category, plz
            FROM dbo.transportstation_crypt
            WHERE transportstationID = ?
        """

        station_ids = {eintrag[3] for eintrag in transport_daten.values()}

        idx = 1
        for transportstationID in station_ids:
            cursor.execute(sql, transportstationID)
            zeilen = cursor.fetchall()
            for zeile in zeilen:
                transportstationID, encrypted_transportstation, encrypted_category, encrypted_plz = zeile

                decrypted_transportstation = decrypt_value(encrypted_transportstation)
                decrypted_category = decrypt_value(encrypted_category)
                decrypted_plz = decrypt_value(encrypted_plz)

                transportstation_daten[idx] = [
                    transportstationID,
                    decrypted_transportstation,
                    decrypted_category,
                    decrypted_plz,
                ]
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

###################################################################
# Datenbank Zugriff - Alle Transport-IDs ##########################
###################################################################

def get_alle_transport_ids(verbindungs_i):

    '''
    @brief Liest alle vorhandenen Transport-IDs aus der Tabelle *coolchain*.
    @details
    Diese Funktion wird für die Schaltfläche *Alle prüfen* gebraucht.
    Dabei soll das Programm nicht nur einen einzelnen Transport,
    sondern alle bekannten Transporte nacheinander untersuchen.

    Was an dieser Stelle passiert:
    - Es wird eine Datenbankverbindung geöffnet.
    - Danach wird mit einem SELECT DISTINCT jede Transport-ID nur einmal geladen.
    - Die Ergebnismenge wird sortiert zurückgegeben.

    Wie das Programm das grob handhabt:
    - Es entsteht eine einfache Liste aller IDs.
    - Über diese Liste kann das Hauptprogramm später mit einer for-Schleife laufen
      und für jede ID dieselbe Prüfung ausführen.

    Warum das gebraucht wird:
    - Ohne diese Funktion könnte das Programm nur Einzelprüfungen durchführen.
    - Für eine vollständige Datenbankübersicht braucht das Hauptprogramm aber eine
      Startliste, mit der alle Transporte abgearbeitet werden können.

    @param verbindungs_i SQL-Verbindungsstring für pyodbc.
    @return Liste aller vorhandenen Transport-IDs.
    '''

    alle_ids = []

    try:
        conn = pyodbc.connect(verbindungs_i)
        cursor = conn.cursor()

        cursor.execute("SELECT DISTINCT transportID FROM dbo.coolchain ORDER BY transportID")
        alle_ids = [row[0] for row in cursor.fetchall()]
        return alle_ids

    except Exception as e:
        print("Fehler beim Datenbankzugriff - Alle Transport-IDs:", e)
        return []

    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()

        print(alle_ids)

###################################################################
# Wetterdatenabfrage ##############################################
###################################################################

# def get_wetter_temperatur(plz, datetime_obj, api_key):


