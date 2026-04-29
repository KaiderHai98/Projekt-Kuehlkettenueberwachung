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

key = b'mysecretpassword'                # 16 Byte Passwort
iv  = b'passwort-salzen!'                # 16 Byte Initialization Vektor

###################################################################
# Hilfsfunktionen #################################################
###################################################################

def decrypt_value(encrypted_data):

    '''
    @brief Entschlüsselt einen einzelnen Datenbankwert aus den verschlüsselten Tabellen.
    @details
    Diese Funktion wird immer dann benutzt, wenn Stammdaten nicht im Klartext,
    sondern als verschlüsselte Bytefolge aus der Datenbank gelesen werden.

    Was an dieser Stelle passiert:
    - Zuerst wird geprüft, ob überhaupt ein Wert vorhanden ist.
    - Danach wird ein AES-Cipher-Objekt mit dem vorgegebenen Passwort und
      dem vorgegebenen Initialisierungsvektor aufgebaut.
    - Anschließend wird der Binärwert entschlüsselt.
    - Zum Schluss wird das Padding entfernt und der Klartext als normaler String
      zurückgegeben.

    Warum das gebraucht wird:
    - Die Tabellen company_crypt und transportstation_crypt enthalten die Inhalte
      nicht direkt lesbar.
    - Die restliche Programmlogik benötigt aber lesbare Firmennamen, Stationsnamen,
      Kategorien und Postleitzahlen.
    - Ohne diese Entschlüsselung könnte das Hauptprogramm zwar Datensätze laden,
      aber nicht sinnvoll weiterverarbeiten oder verständlich ausgeben.

    @param encrypted_data Verschlüsselter Datenbankwert als Binärwert.
    @return Entschlüsselter Klartext als String.
    '''

    if encrypted_data is None:
        return ""

    cipher = AES.new(key, AES.MODE_CBC, iv)  # Verschlüsselung initialisieren
    return unpad(cipher.decrypt(encrypted_data), AES.block_size).decode()

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

def get_temperatur_daten(transport_daten, verbindungs_i):

    '''
    @brief Liest die Temperaturmessungen der im Transport verwendeten Stationen aus *tempdata*.
    @details
    Diese Funktion ermittelt nicht einfach alle Temperaturwerte einer Station,
    sondern gezielt nur die Messwerte aus dem Zeitraum, in dem sich die Ware
    tatsächlich an der jeweiligen Station befand.

    Was an dieser Stelle passiert:
    - Zuerst werden die schon geladenen Transportdaten zeitlich sortiert.
    - Danach läuft eine for-Schleife über alle Bewegungsereignisse.
    - Für jeden Eintrag mit Status *in* beginnt ein möglicher Aufenthaltszeitraum.
    - Anschließend sucht eine weitere Schleife den dazugehörigen nächsten *out*-Eintrag
      derselben Station.
    - Ist ein passendes *out* vorhanden, werden nur die Temperaturwerte zwischen
      Einchecken und Auschecken geladen.
    - Gibt es kein *out*, werden alle Werte ab dem Eincheck-Zeitpunkt geladen.

    Wie das Programm das grob handhabt:
    - Es werden also nur die Temperaturdaten mitgenommen, die wirklich zu dem
      konkreten Aufenthalt des Produkts passen.
    - Die Ergebnisse landen wieder gesammelt in einem Dictionary, damit die
      spätere Verarbeitung einfach über alle Temperaturmessungen laufen kann.

    Warum das gebraucht wird:
    - Die Temperaturprüfung soll nicht die gesamte Station bewerten,
      sondern den Abschnitt, in dem der geprüfte Transport dort gelagert war.
    - Genau diese Daten werden später benötigt, um festzustellen,
      ob die Temperaturgrenzen von +2 °C bis +4 °C eingehalten wurden.

    @param transport_daten Bereits geladene Bewegungsdaten des Transports.
    @param verbindungs_i SQL-Verbindungsstring für pyodbc.
    @return Tuple aus Dictionary mit Temperaturdaten und Anzahl der Datensätze.
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

def get_wetter_temperatur(plz, datetime_obj, api_key):
    
    '''
    @brief Ruft die Außentemperatur zu einem Ort und Zeitpunkt über die Visual-Crossing-API ab.
    @details
    Diese Funktion ergänzt einen gefundenen Kühlkettenverstoß um eine zusätzliche
    Umweltinformation: Wie warm war es außen am Auslagerungsort, als die Ware dort
    ohne Kühlung übergeben wurde?

    Was an dieser Stelle passiert:
    - Zuerst wird geprüft, ob überhaupt ein API-Key vorhanden ist.
    - Danach wird *requests* erst innerhalb der Funktion importiert.
      Dadurch startet das Gesamtprogramm auch dann noch, wenn die Bibliothek auf
      dem System fehlt und die Wetterfunktion gerade nicht benutzt wird.
    - Anschließend wird geprüft, ob eine sinnvolle PLZ vorhanden ist.
      Für Transportwagen mit PLZ 0 gibt es keine ortsbezogene Wetterabfrage.
    - Die Uhrzeit wird auf die nächste volle Stunde gerundet, weil die API mit
      stündlichen Wetterwerten arbeitet.
    - Danach wird die Anfrage-URL gebaut und an die Wetter-API gesendet.
    - Wenn Daten vorhanden sind, wird daraus die Temperatur gelesen und zurückgegeben.

    Wie das Programm das grob handhabt:
    - Die Funktion liefert nicht nur Temperaturwerte zurück,
      sondern im Fehlerfall auch eine verständliche Textmeldung.
    - Dadurch kann die Verarbeitung später entscheiden,
      ob eine Temperatur angezeigt oder stattdessen eine Hinweiszeile ausgegeben wird.

    Warum das gebraucht wird:
    - In Phase 2 soll bei einer zu langen Übergabezeit zusätzlich die Temperatur
      am Auslagerungsort ausgegeben werden.
    - Genau diese Information liefert diese Funktion an die Verarbeitungslogik.

    @param plz Postleitzahl der Auslagerungsstation.
    @param datetime_obj Zeitpunkt der Auslagerung als datetime-Objekt.
    @param api_key API-Schlüssel für Visual Crossing.
    @return Tuple aus Temperaturwert oder None und Status-/Fehlermeldung.
    '''

    if api_key is None or str(api_key).strip() == "":
        return None, "Wetterdaten konnten nicht abgefragt werden (API-Key fehlt)"

    try:
        import requests
    except ImportError:
        return None, "Wetterdaten konnten nicht abgefragt werden (Bibliothek requests fehlt)"

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



