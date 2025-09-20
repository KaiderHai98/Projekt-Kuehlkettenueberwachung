
###################################################################
# Daten Prüfen - IN / OUT Reihenfolge #############################
###################################################################

def pruefe_in_out(transport_daten):
    in_out_fehler = []
    aktuell = None
    in_out_aktuell = None
    letzte_zeit = None

    for eintrag in transport_daten:
        status = eintrag[4].strip("'").lower()   # Status: ist im 3. Feld 
        zeitpunkt = eintrag[5]                   # Zeit:   ist im 6. Feld 

        if aktuell == status:

            diff = zeitpunkt - letzte_zeit
            minuten = diff.seconds // 60
            sekunden = diff.seconds % 60

            if status == "in":
                in_out_fehler.append(f"Doppelter Eincheck-Zeitpunkt, Abstand: {minuten} Minuten {sekunden} Sekunden")
            if status == "out":
                in_out_fehler.append(f"Doppelter Auscheck-Zeitpunkt, Abstand: {minuten} Minuten {sekunden} Sekunden")

        if status == "in":
            in_out_aktuell = "Eingecheckt"
        if status == "out":
            in_out_aktuell = "Ausgecheckt"

        aktuell = status
        letzte_zeit = zeitpunkt

    return in_out_fehler, in_out_aktuell

###################################################################
# Zeiträume ohne Kühlung ##########################################
###################################################################

def check_zeitraeume(transport_daten):
    ausgabe = "Korrekte Zeiteinhaltung bei Übergabe"
    letzte_zeit = None
    letzte_aktion = None

    for eintrag in transport_daten:
        status, zeitpunkt = (eintrag[4]).strip("'"), eintrag[5]

        if status == "in" and letzte_aktion == "out":
            diff = (zeitpunkt - letzte_zeit).total_seconds() / 60
            if diff > 10:
                ausgabe = "Übergabe > 10 min"
                break

        letzte_aktion = status
        letzte_zeit = zeitpunkt

    return ausgabe



