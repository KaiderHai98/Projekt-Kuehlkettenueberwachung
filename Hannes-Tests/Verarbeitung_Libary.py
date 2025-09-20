
###################################################################
# Daten Prüfen - IN / OUT Reihenfolge #############################
###################################################################

def pruefe_in_out(transport_daten):
    try:
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
    
    except Exception as e:
        print("Fehler bei der Verarbeitung - IN/OUT Prüfung:", e)
        return None

    finally:

        # Terminal Ausgabe

        if in_out_fehler:
            print("Fehler gefunden:")
            for i_o_f in in_out_fehler:
                print("-", i_o_f)
        else:
            print("Korrekte Reihenfolge")

        print("Letzter Buchungsstand:", in_out_aktuell)

###################################################################
# Daten Prüfen: Zeiträume 10min Max ohne Kühlung ##################
###################################################################

def check_zeitraeume_10minMax(transport_daten):
    try:
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
    
    except Exception as e:
        print("Fehler bei der Verarbeitung - Zeitraum Prüfung 10min Max:", e)
        return None

    finally:

        # Terminal Ausgabe

        print(ausgabe)

###################################################################
# Daten Prüfen: Transportdauer 48h Max ############################
###################################################################

def check_transportdauer(transport_daten):

    try:
        ausgabe = "Korrekte Transportdauer"
        startzeit = None
        endzeit = None

        for eintrag in transport_daten:
            status = (eintrag[4]).strip("'")
            zeitpunkt = eintrag[5]

            if status == "in" and startzeit is None:
                startzeit = zeitpunkt
            if status == "out":
                endzeit = zeitpunkt

        if startzeit and endzeit:
            diff = (endzeit - startzeit).total_seconds() / 3600
            if diff > 48:
                ausgabe = "Transportdauer > 48 h"

        return ausgabe
    
    except Exception as e:
        print("Fehler bei der Verarbeitung - Transportdauer 48h Max:", e)
        return None
    
    finally:

        # Terminal Ausgabe

        print(ausgabe) 

###################################################################
# Daten Prüfen: Transportstations - Konsistenzprüfung #############
###################################################################

###################################################################
# Daten Prüfen: Eintags -Prüfung ##################################
###################################################################

