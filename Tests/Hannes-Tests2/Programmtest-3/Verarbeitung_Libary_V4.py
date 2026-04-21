# ================================
# Datei: Verarbeitung_Libary_V4.py
# ================================
# #############################################################################################################
#  Libary: CoolChainProjekt
#  Datei: Verarbeitung_Libary_V4.py
#
# Version: 4 vom: 21.04.2026
# Autoren: Josie Woeste, Hannes Ruhe, Kai Meiners
#
# Zugehöriges Hauptprogramm:
# - Hauptprogramm_V4.py
# 
# Funktionsbeschreibung: 
# Libary zur Verarbeitung der Transportdaten
# #############################################################################################################

"""
@brief Verarbeitungsbibliothek zur fachlichen Prüfung eines Transports.
@details

Diese Datei enthält die eigentliche Prüflogik des Projekts.
Hier wird entschieden, ob ein Transport korrekt ist oder ob Verstöße gegen
die Kühlkette vorliegen.

Die Datei arbeitet nicht direkt mit SQL-Befehlen oder der GUI,
sondern mit bereits geladenen Datenstrukturen.

Grob gesagt passiert hier Folgendes:
- Hilfsfunktionen lesen aus den Dictionaries einzelne Eigenschaften heraus,
  zum Beispiel Status, Stationsname, Kategorie oder Postleitzahl.
- Die Hauptfunktion *verarbeite_transport()* läuft Schritt für Schritt über
  die geladenen Transport- und Temperaturdaten.
- In mehreren Prüfblöcken wird untersucht, ob die Kühlkette fachlich stimmig ist.
- Jeder gefundene Fehler wird als verständliche Meldung gespeichert.
- Am Ende wird entweder eine Liste mit Fehlern oder die Meldung *korrekt* zurückgegeben.
"""

from DB_Zugriff_Libary_V4 import get_wetter_temperatur

def _get_status(eintrag):

    '''
    @brief Liefert den Bewegungsstatus eines Datensatzes als sauberen String zurück.
    @details
    Diese Hilfsfunktion liest aus einem Transporteintrag den Status *in* oder *out* heraus.

    Was an dieser Stelle passiert:
    - Der Statuswert wird aus dem übergebenen Datensatz gelesen.
    - Eventuelle Hochkommas werden entfernt.
    - Der Text wird in Kleinbuchstaben umgewandelt.

    Warum das gebraucht wird:
    - Die spätere Prüflogik vergleicht sehr oft mit *in* und *out*.
    - Durch die Bereinigung wird sichergestellt, dass diese Vergleiche
      zuverlässig funktionieren.

    @param eintrag Einzelner Datensatz aus den Transportdaten.
    @return Bereinigter Statuswert als String.
    '''

    return str(eintrag[4]).replace("'", "").lower()

def _get_station_name(station_id, transportstation_daten):

    '''
    @brief Sucht zu einer Stations-ID den lesbaren Stationsnamen.
    @details
    Die Funktion läuft mit einer for-Schleife durch alle geladenen Stationsdaten,
    bis die passende ID gefunden wird.
    '''
        
    for key in transportstation_daten:
        if transportstation_daten[key][0] == station_id:
            return str(transportstation_daten[key][1]).replace("'", "")
    return ""

def _get_art(station_id, transportstation_daten):

    '''
    @brief Sucht zu einer Stations-ID die Stationsart, also z. B. *GVZ* oder *KT*.
    @details
    Die Funktion durchläuft die Stationsdaten so lange, bis zur gesuchten ID
    die Kategorie gefunden wurde.
    '''
        
    for key in transportstation_daten:
        if transportstation_daten[key][0] == station_id:
            return str(transportstation_daten[key][2]).replace("'", "").upper()
    return ""

def _get_plz(station_id, transportstation_daten):

    '''
    @brief Sucht zu einer Stations-ID die Postleitzahl.
    @details
    Die Funktion läuft über die geladenen Stationsdaten und gibt die PLZ der
    passenden Station zurück.
    '''
        
    for key in transportstation_daten:
        if transportstation_daten[key][0] == station_id:
            return str(transportstation_daten[key][3]).replace("'", "")
    return ""

def verarbeite_transport(transport_daten, temperatur_daten, company_daten, transportstation_daten, api_key=""):

    '''
    @brief Prüft einen Transport auf fachliche Fehler in der Kühlkette.
    @details
    Diese Funktion ist das Herzstück des gesamten Projekts.
    Hier wird aus den geladenen Daten ermittelt, ob der Transport regelkonform war.

    Was die Funktion grundsätzlich macht:
    - Sie sammelt und sortiert die Bewegungsdaten und Temperaturdaten.
    - Danach arbeitet sie nacheinander mehrere Prüfblöcke ab.
    - Jeder Block untersucht einen bestimmten fachlichen Aspekt,
      zum Beispiel Übergabezeiten, Transportdauer oder Temperaturgrenzen.
    - Für jeden gefundenen Verstoß wird eine Meldung in die Liste *meldungen* geschrieben.
    - Wenn kein Verstoß gefunden wird, wird am Ende *korrekt* eingetragen.
    '''
    
    meldungen = []

    # #########################################
    # 1. Kein Transport vorhanden
    # #########################################
    if len(transport_daten) == 0:
        meldungen.append("Es gibt gar keinen Eintrag")
        return meldungen

    # #########################################
    # 2. Daten sammeln und sortieren
    # #########################################
    transport_daten_liste = []
    temperatur_daten_liste = []

    for key in transport_daten:
        transport_daten_liste.append(transport_daten[key])
    transport_daten_liste.sort(key=lambda x: x[5])

    for key in temperatur_daten:
        temperatur_daten_liste.append(temperatur_daten[key])
    temperatur_daten_liste.sort(key=lambda x: x[1])

    # #########################################
    # 3. Übergabe > 10 min + Wetterdaten
    # #########################################
    letzte_out = None
    letzte_out_station = None

    for bewegung in transport_daten_liste:
        status = _get_status(bewegung)
        zeit = bewegung[5]

        if status == "out":
            letzte_out = zeit
            letzte_out_station = bewegung[3]

        if status == "in" and letzte_out is not None:
            diff = (zeit - letzte_out).total_seconds() / 60
            if diff > 10:
                meldung = "Übergabe > 10 min"
                plz = _get_plz(letzte_out_station, transportstation_daten)
                station_name = _get_station_name(letzte_out_station, transportstation_daten)
                temperatur_aussen, wetter_meldung = get_wetter_temperatur(plz, letzte_out, api_key)

                if temperatur_aussen is not None:
                    meldung = (
                        meldung
                        + " | Auslagerungsort: " + station_name
                        + " | Außentemperatur: " + str(temperatur_aussen) + " °C"
                    )
                else:
                    meldung = (
                        meldung
                        + " | Auslagerungsort: " + station_name
                        + " | " + wetter_meldung
                    )

                meldungen.append(meldung)

            letzte_out = None
            letzte_out_station = None

    # ##########################################
    # 4. Transportdauer > 48h
    # ##########################################
    erstes_in = None
    letztes_out = None

    for bewegung in transport_daten_liste:
        status = _get_status(bewegung)
        zeit = bewegung[5]
        if status == "in" and erstes_in is None:
            erstes_in = zeit
        if status == "out":
            letztes_out = zeit

    if erstes_in is not None and letztes_out is not None:
        stunden = (letztes_out - erstes_in).total_seconds() / 3600
        if stunden > 48:
            meldungen.append("Transportdauer > 48h")

    # ##########################################
    # 5. Doppelter Auscheck-Zeitpunkt
    # ##########################################
    letzte_aktion = {}

    for bewegung in transport_daten_liste:
        station = bewegung[3]
        status = _get_status(bewegung)
        zeit = bewegung[5]
        if station in letzte_aktion:
            if letzte_aktion[station][0] == "out" and status == "out":
                diff = int((zeit - letzte_aktion[station][1]).total_seconds() / 60)
                meldungen.append("Doppelter Auscheck-Zeitpunkt (Abstand " + str(diff) + " min)")
        letzte_aktion[station] = [status, zeit]

    # ##########################################
    # 6. Fehlende OUTs - Konsitenzprüfung
    # ##########################################
    letzter_status = _get_status(transport_daten_liste[-1])
    fehlt_in_mitte = False

    for station in letzte_aktion:
        if letzte_aktion[station][0] == "in":
            if letzter_status == "in":
                meldungen.append("Auscheck-Zeitpunkt fehlt am Ende (kein Fehler., da nicht abgeschlossen.)")
            else:
                fehlt_in_mitte = True
    if fehlt_in_mitte:
        meldungen.append("Auscheck-Zeitpunkt fehlt in der Mitte")

    # ##########################################
    # 7. Aus und wieder Einchecken im gleichen Kühllager - Konsitenzprüfung
    # ##########################################
    zyklus_gesehen = {}
    letzter_status_station = {}

    for bewegung in transport_daten_liste:
        station = bewegung[3]
        status = _get_status(bewegung)
        art = _get_art(station, transportstation_daten)

        if station not in zyklus_gesehen:
            zyklus_gesehen[station] = False

        if station in letzter_status_station:
            if letzter_status_station[station] == "in" and status == "out":
                zyklus_gesehen[station] = True

        if status == "in" and zyklus_gesehen[station] and art == "GVZ":
            if "Aus und wieder Einchecken im gleichen Kühllager" not in meldungen:
                meldungen.append("Aus und wieder Einchecken im gleichen Kühllager")

        letzter_status_station[station] = status

    # ##########################################
    # 8. GVZ vor KT prüfen - Konsitenzprüfung
    # ##########################################
    kt_aktiv = False

    for bewegung in transport_daten_liste:
        art = _get_art(bewegung[3], transportstation_daten)
        status = _get_status(bewegung)

        if art == "KT":
            if status == "in":
                kt_aktiv = True
            elif status == "out":
                kt_aktiv = False

        elif art == "GVZ" and status == "in":
            if kt_aktiv and "Einchecken Kühllager liegt zeitlich vor Auschecken LKW" not in meldungen:
                meldungen.append("Einchecken Kühllager liegt zeitlich vor Auschecken LKW")

    # ##########################################
    # 9. Temperaturüberwachung 2°C bis 4°C
    # ##########################################
    temperatur_fehler = []

    for temp_eintrag in temperatur_daten_liste:
        station_id = temp_eintrag[0]
        zeit = temp_eintrag[1]
        temperatur = float(temp_eintrag[2])
        station_name = _get_station_name(station_id, transportstation_daten)

        if temperatur < 2 or temperatur > 4:
            temperatur_fehler.append(
                "Temperaturfehler in Station "
                + station_name
                + " am "
                + zeit.strftime("%d.%m.%Y %H:%M:%S")
                + " -> "
                + str(temperatur)
                + " °C"
            )

    for fehler in temperatur_fehler:
        meldungen.append(fehler)

    # ##########################################
    # 10. Wenn keine Fehler -> korrekt
    # ##########################################
    if len(meldungen) == 0:
        meldungen.append("korrekt")

    return meldungen

