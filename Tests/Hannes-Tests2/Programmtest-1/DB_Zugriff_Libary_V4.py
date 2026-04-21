# #############################################################################################################
#  Libary: CoolChainProjekt
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
# #############################################################################################################

import requests
from datetime import timedelta
import pyodbc
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

###################################################################
# Konstanten ######################################################
###################################################################

AES_KEY = b'mysecretpassword'
AES_IV = b'passwort-salzen!'

###################################################################
# Hilfsfunktionen #################################################
###################################################################

def decrypt_value(encrypted_data):
    '''
    @brief Entschlüsselt einen einzelnen Datenbankwert aus den *_crypt-Tabellen.
    @details Die Funktion erwartet einen binären Datenbankwert, der per AES-CBC
    verschlüsselt wurde. Der Wert wird mit dem in der Projektaufgabe vorgegebenen
    Schlüssel und Initialisierungsvektor entschlüsselt und als String zurückgegeben.
    '''

    if encrypted_data is None:
        return ""

    cipher = AES.new(AES_KEY, AES.MODE_CBC, AES_IV)
    plaintext = unpad(cipher.decrypt(bytes(encrypted_data)), AES.block_size)
    return plaintext.decode("utf-8")

###################################################################
# Datenbank Zugriff - Transportdaten ##############################
###################################################################

def get_transport_daten(transportid, verbindungs_i):
    '''
    @brief Liest Transportdaten aus der Datenbanktabelle *coolchain* anhand einer gegebenen Transport-ID.
    @details Die Funktion stellt eine Verbindung zur angegebenen SQL-Datenbank her, führt eine Abfrage auf der Tabelle
    *dbo.coolchain* aus und sammelt alle Datensätze mit der passenden Transport-ID.
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

def get_temperatur_daten(transport_daten, verbindungs_i):
    '''
    @brief Liest Temperaturdaten zu Transportstationen aus der Tabelle *tempdata* basierend auf Transportdaten.
    @details Die Funktion nutzt zuvor geladene Transportdaten, um für jede Station und jeden "Check-in"-Zeitpunkt
    die zugehörigen Temperaturmessungen aus der Tabelle *dbo.tempdata* abzurufen.
    '''

    temperatur_daten = {}

    try:
        conn = pyodbc.connect(verbindungs_i)
        cursor = conn.cursor()

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

        items = sorted(transport_daten.items(), key=lambda kv: kv[1][5])

        idx = 1
        for pos, (_, eintrag) in enumerate(items):
            station_id = eintrag[3]
            status = str(eintrag[4]).strip().strip("'").lower()
            start_dt = eintrag[5]

            if status != "in":
                continue

            end_dt = None
            for _, next_entry in items[pos + 1:]:
                if next_entry[3] == station_id:
                    next_status = str(next_entry[4]).strip().strip("'").lower()
                    if next_status == "out":
                        end_dt = next_entry[5]
                        break

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
        return {}, 0

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
    '''
    @brief Liest Firmendaten aus der Tabelle *company_crypt* basierend auf den in den Transportdaten enthaltenen Company-IDs.
    @details Die verschlüsselten Inhalte werden sofort entschlüsselt und in der Form
    [companyID, company, strasse, ort, plz] zurückgegeben.
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
                company_daten[idx] = [
                    zeile[0],
                    decrypt_value(zeile[1]),
                    decrypt_value(zeile[2]),
                    decrypt_value(zeile[3]),
                    decrypt_value(zeile[4]),
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
    @brief Liest Daten zu Transportstationen aus der Tabelle *transportstation_crypt* anhand der in den Transportdaten enthaltenen Station-IDs.
    @details Die verschlüsselten Inhalte werden entschlüsselt. Die Rückgabestruktur lautet:
    [transportstationID, transportstation, category, plz].
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
                transportstation_daten[idx] = [
                    zeile[0],
                    decrypt_value(zeile[1]),
                    decrypt_value(zeile[2]),
                    decrypt_value(zeile[3]),
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
    @brief Liest alle eindeutigen Transport-IDs aus der Tabelle *coolchain*.
    @details Die Funktion gibt eine alphabetisch sortierte Liste aller in der Datenbank vorhandenen
    Transport-IDs zurück.
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

def get_wetter_temperatur(plz, datetime_obj, api_key):
    '''
    @brief Ruft die Außentemperatur für eine Postleitzahl und einen Zeitpunkt über Visual Crossing ab.
    @details Die Uhrzeit wird auf die nächste volle Stunde gerundet, da die API stündliche Wetterdaten liefert.
    Ist keine sinnvolle Postleitzahl vorhanden oder fehlt der API-Key, wird kein Temperaturwert zurückgegeben.
    '''

    if api_key is None or str(api_key).strip() == "":
        return None, "Wetterdaten konnten nicht abgefragt werden (API-Key fehlt)"

    plz_text = str(plz).strip()
    if plz_text == "" or plz_text == "0":
        return None, "Wetterdaten nicht verfügbar (keine PLZ für Transportwagen)"

    datetime_gerundet = datetime_obj.replace(minute=0, second=0, microsecond=0)
    if datetime_obj.minute >= 30:
        datetime_gerundet = datetime_gerundet + timedelta(hours=1)

    timestamp = datetime_gerundet.strftime('%Y-%m-%dT%H:%M:%S')
    location = f"{plz_text},DE"

    url = (
        "https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/"
        f"{location}/{timestamp}"
    )

    try:
        response = requests.get(
            url,
            params={'unitGroup': 'metric', 'key': api_key, 'include': 'hours'},
            timeout=15,
        )
        response.raise_for_status()
        data = response.json()

        temperatur = None
        if "days" in data and len(data["days"]) > 0:
            if "hours" in data["days"][0] and len(data["days"][0]["hours"]) > 0:
                temperatur = data["days"][0]["hours"][0].get("temp")
            if temperatur is None:
                temperatur = data["days"][0].get("temp")

        if temperatur is None:
            return None, "Wetterdaten konnten nicht ausgewertet werden"

        return temperatur, "ok"

    except Exception as e:
        return None, "Wetterdaten konnten nicht abgefragt werden (" + str(e) + ")"
