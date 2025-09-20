
###################################################################
# Daten Prüfen - IN / OUT Reihenfolge #############################
###################################################################

def pruefe_in_out(transport_daten):
    in_out_fehler = []
    aktuell = None
    in_out_aktuell = None
    letzte_zeit = None

    for Zeile in transport_daten:
        status = Zeile[4].strip("'").lower()   # Status ist im 3. Feld 
        zeitpunkt = Zeile[5]                   # Zeit ist im 6. Feld 

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

