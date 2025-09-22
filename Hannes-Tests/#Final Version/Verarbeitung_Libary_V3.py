
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
# Libary zur Verarbeitung der Transportdaten
###############################################################################################################

def verarbeite_transport(transport_daten, temperatur_daten, company_daten, transportstation_daten):
    meldungen = []

    # #########################################
    # 1. Kein Transport vorhanden
    # #########################################

    if len(transport_daten) == 0:
        meldungen.append("Es gibt gar keinen Eintrag")
        return meldungen

    events = []

    for key in transport_daten:
        events.append(transport_daten[key])
    events.sort(key=lambda x: x[5])

    def get_status(eintrag):
        return str(eintrag[4]).replace("'", "").lower()

    def get_art(station_id):
        for key in transportstation_daten:
            if transportstation_daten[key][0] == station_id:
                return str(transportstation_daten[key][2]).replace("'", "").upper()
        return ""

    # #########################################
    # 2. Übergabe > 10 min
    # #########################################

    letzte_out = None

    for e in events:
        status = get_status(e)
        zeit = e[5]
        if status == "out":
            letzte_out = zeit
        if status == "in" and letzte_out != None:
            diff = (zeit - letzte_out).total_seconds() / 60
            if diff > 10:
                meldungen.append("Übergabe > 10 min")
            letzte_out = None

    # ##########################################
    # 3. Transportdauer > 48h
    # ##########################################

    erstes_in = None
    letztes_out = None

    for e in events:
        status = get_status(e)
        zeit = e[5]
        if status == "in" and erstes_in == None:
            erstes_in = zeit
        if status == "out":
            letztes_out = zeit
    if erstes_in != None and letztes_out != None:
        stunden = (letztes_out - erstes_in).total_seconds() / 3600
        if stunden > 48:
            meldungen.append("Transportdauer > 48h")

    # ##########################################
    # 4. Doppelter Auscheck-Zeitpunkt
    # ##########################################

    letzte_aktion = {}

    for e in events:
        station = e[3]
        status = get_status(e)
        zeit = e[5]
        if station in letzte_aktion:
            if letzte_aktion[station][0] == "out" and status == "out":
                diff = int((zeit - letzte_aktion[station][1]).total_seconds() / 60)
                meldungen.append("Doppelter Auscheck-Zeitpunkt (Abstand " + str(diff) + " min)")
        letzte_aktion[station] = [status, zeit]

    # ##########################################
    # 5. Fehlende OUTs - Konsitenzprüfung
    # ##########################################

    letzter_status = get_status(events[-1])
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
    # 6. Aus und wieder Einchecken im gleichen Kühllager - Konsitenzprüfung
    # ##########################################

    zyklus_gesehen = {}          # station_id -> True/False
    letzter_status_station = {}  # station_id -> 'in'/'out'

    for e in events:
        station = e[3]
        status  = get_status(e)
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
    # 7. GVZ vor KT prüfen - Konsitenzprüfung
    # ##########################################

    kt_aktiv = False

    for e in events:
        art = get_art(e[3])
        status = get_status(e)

        if art == "KT":
            if status == "in":
                kt_aktiv = True
            elif status == "out":
                kt_aktiv = False

        elif art == "GVZ" and status == "in":
            if kt_aktiv and "Einchecken Kühllager liegt zeitlich vor Auschecken LKW" not in meldungen:
                meldungen.append("Einchecken Kühllager liegt zeitlich vor Auschecken LKW")

    # ##########################################
    # 8. Wenn keine Fehler -> korrekt
    # ##########################################

    if len(meldungen) == 0:
        meldungen.append("korrekt")

    return meldungen
