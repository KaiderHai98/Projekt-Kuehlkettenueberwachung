
###############################################################################################################
#  Libary: CoolChainProjekt
#  Datei: Verarbeitung_Libary_V3.py
#
# Version: 4 vom: 30.09.2025
# Autoren:
#
# Zugehöriges Hauptprogramm:
# - Hauptprogramm_V4.py
# 
#
# Funktionsbeschreibung: 
# Libary zur Verarbeitung der Transportdaten
###############################################################################################################

'''
@brief def verarbeite_transport Verarbeitet und überprüft die Transportdaten auf Fehler.
@details Diese Funktion führt verschiedene Prüfungen auf den Ablauf
         eines Transports durch (z. B. Übergabezeiten, Transportdauer,
         doppelte OUTs, fehlende OUTs, GVZ/KT-Reihenfolge).
         Alle gefundenen Auffälligkeiten werden als Textmeldungen
         zurückgegeben.
         
         Eine Liste mit Fehler-Meldungen (Strings):
         - Wenn Fehler gefunden wurden: entsprechende Fehlermeldungen.
         - Wenn keine Fehler gefunden wurden: ["korrekt"].
'''

def verarbeite_transport(transport_daten, temperatur_daten, company_daten, transportstation_daten):
    meldungen = []

    # #########################################
    # 1. Kein Transport vorhanden
    # #########################################

    '''
    @brief Schritt 1: Kein Transport vorhanden
    @details Wenn in transport_daten keine Einträge gespeichert sind,
             gibt es keinen Transport. In diesem Fall wird sofort die
             Meldung "Es gibt gar keinen Eintrag" zurückgegeben und
             die Funktion beendet.
    '''

    if len(transport_daten) == 0:
        meldungen.append("Es gibt gar keinen Eintrag")
        return meldungen

    # #########################################
    # 2. Daten sammeln und sortieren 
    # #########################################

    '''
    @brief Schritt 2: Daten sammeln und sortieren
    @details Alle Transport-Einträge werden aus transport_daten herausgesucht,
             in eine Liste "transport_daten_liste" gepackt und zeitlich sortiert.
             Dazu gibt es zwei Hilfsfunktionen:
             - get_status(): liefert 'in' oder 'out' zurück.
             - get_art(): bestimmt die Art der Station (GVZ oder KT).
    '''

    transport_daten_liste = []

    for key in transport_daten:
        transport_daten_liste.append(transport_daten[key])
    transport_daten_liste.sort(key=lambda x: x[5])

    def get_status(eintrag):
        return str(eintrag[4]).replace("'", "").lower()

    def get_art(station_id):
        for key in transportstation_daten:
            if transportstation_daten[key][0] == station_id:
                return str(transportstation_daten[key][2]).replace("'", "").upper()
        return ""

    # #########################################
    # 3. Übergabe > 10 min
    # #########################################

    '''
    @brief Schritt 3: Übergabe > 10 min
    @details Nach jedem OUT-Ereignis wird die Zeit bis zum nächsten IN gemessen.
             Liegt dieser Abstand über 10 Minuten, wird die Meldung
             "Übergabe > 10 min" erstellt. Danach wird der OUT-Zeitpunkt zurückgesetzt.
    '''

    letzte_out = None

    for bewegung in transport_daten_liste:
        status = get_status(bewegung)
        zeit = bewegung[5]
        if status == "out":
            letzte_out = zeit
        if status == "in" and letzte_out != None:
            diff = (zeit - letzte_out).total_seconds() / 60
            if diff > 10:
                meldungen.append("Übergabe > 10 min")
            letzte_out = None

    # ##########################################
    # 4. Transportdauer > 48h
    # ##########################################

    '''
    @brief Schritt 4: Transportdauer > 48h
    @details Es wird die Zeit zwischen dem ersten IN und dem letzten OUT berechnet.
             Überschreitet die Transportdauer 48 Stunden, wird die Meldung
             "Transportdauer > 48h" hinzugefügt.
    '''

    erstes_in = None
    letztes_out = None

    for bewegung in transport_daten_liste:
        status = get_status(bewegung)
        zeit = bewegung[5]
        if status == "in" and erstes_in == None:
            erstes_in = zeit
        if status == "out":
            letztes_out = zeit
    if erstes_in != None and letztes_out != None:
        stunden = (letztes_out - erstes_in).total_seconds() / 3600
        if stunden > 48:
            meldungen.append("Transportdauer > 48h")

    # ##########################################
    # 5. Doppelter Auscheck-Zeitpunkt
    # ##########################################

    '''
    @brief Schritt 5: Doppelter Auscheck-Zeitpunkt
    @details Hier wird geprüft, ob an derselben Station zweimal direkt
             hintereinander ein OUT gespeichert wurde. Wenn ja, wird der
             Zeitunterschied berechnet und in der Meldung ausgegeben.
    '''

    letzte_aktion = {}

    for bewegung in transport_daten_liste:
        station = bewegung[3]
        status = get_status(bewegung)
        zeit = bewegung[5]
        if station in letzte_aktion:
            if letzte_aktion[station][0] == "out" and status == "out":
                diff = int((zeit - letzte_aktion[station][1]).total_seconds() / 60)
                meldungen.append("Doppelter Auscheck-Zeitpunkt (Abstand " + str(diff) + " min)")
        letzte_aktion[station] = [status, zeit]

    # ##########################################
    # 6. Fehlende OUTs - Konsitenzprüfung
    # ##########################################

    '''
    @brief Schritt 6: Fehlende OUTs
    @details Falls ein Transport an einer Station mit "in" endet, aber
             kein "out" folgt, wird dies überprüft:
             - Am Ende des Transports -> Meldung "Auscheck-Zeitpunkt fehlt am Ende".
             - Mitten im Transport -> Meldung "Auscheck-Zeitpunkt fehlt in der Mitte".
    '''

    letzter_status = get_status(transport_daten_liste[-1])
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

    '''
    @brief Schritt 7: Aus und wieder Einchecken im gleichen Kühllager
    @details Wurde ein Zyklus (IN -> OUT) an einer GVZ-Station abgeschlossen
             und danach erfolgt erneut ein IN an derselben Station,
             wird eine Meldung hinzugefügt.
    '''

    zyklus_gesehen = {}          # station_id -> True/False
    letzter_status_station = {}  # station_id -> 'in'/'out'

    for bewegung in transport_daten_liste:
        station = bewegung[3]
        status  = get_status(bewegung)
        art     = get_art(station)

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

    '''
    @brief Schritt 8: GVZ vor KT prüfen
    @details Wenn ein KT noch aktiv ist (KT-IN ohne KT-OUT) und in dieser Zeit
             ein GVZ-IN passiert, stimmt die Reihenfolge nicht. In diesem Fall
             wird eine Meldung erstellt.
    '''

    kt_aktiv = False

    for bewegung in transport_daten_liste:
        art = get_art(bewegung[3])
        status = get_status(bewegung)

        if art == "KT":
            if status == "in":
                kt_aktiv = True
            elif status == "out":
                kt_aktiv = False

        elif art == "GVZ" and status == "in":
            if kt_aktiv and "Einchecken Kühllager liegt zeitlich vor Auschecken LKW" not in meldungen:
                meldungen.append("Einchecken Kühllager liegt zeitlich vor Auschecken LKW")

    # ##########################################
    # 9. Wenn keine Fehler -> korrekt
    # ##########################################

    '''
    @brief Schritt 9: Keine Fehler gefunden
    @details Wenn nach allen Prüfungen keine Meldungen in der Liste stehen,
             wird stattdessen "korrekt" zurückgegeben.
    '''

    if len(meldungen) == 0:
        meldungen.append("korrekt")

    return meldungen
