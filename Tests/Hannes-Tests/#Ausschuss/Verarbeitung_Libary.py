###################################################################
# Daten Prüfen: Eingangs - Prüfung ##################################
###################################################################

def check_Daten_Eingang(transport_daten_len, temoratur_daten_len, company_daten_len, transportstation_daten_len):
    try:
        ausgabe = []
        fehler  = []

        if transport_daten_len == 0:
            fehler.append("Keine Transport-Daten vorhanden")
        if temoratur_daten_len == 0:
            fehler.append("Keine Temperatur-Daten vorhanden")
        if company_daten_len == 0:
            fehler.append("Keine Company-Daten vorhanden")
        if transportstation_daten_len == 0:
            fehler.append("Keine Transportstations-Daten vorhanden")

        ausgabe.append(fehler)

        return ausgabe
    
    except Exception as e:
        print("Fehler bei der Verarbeitung - Eingangs-Prüfung:", e)
        return None

    finally:

        # Terminal Ausgabe

        if fehler:
            print("Fehler gefunden:")
            for f in fehler:
                print("-", f)
        else:
            print("Korrekter Eingang der DB-Daten")

###################################################################
# Daten Prüfen - IN / OUT Reihenfolge #############################
###################################################################

def check_in_out(transport_daten):
    try:
        ausgabe        = []
        fehler         = []
        anfangs_status = None
        status         = None
        letzter_status = None
        zeitpunkt      = None
        letzte_zeit    = None

        for eintrag in transport_daten:
            status    = eintrag[4].strip("'").lower()   # [4] = Status: ist im 3. Feld 
            zeitpunkt = eintrag[5]                      # [5] = Zeit:   ist im 6. Feld 

            if anfangs_status == status:

                diff = zeitpunkt - letzte_zeit
                minuten = diff.seconds // 60
                sekunden = diff.seconds % 60

                if status == "in":
                    fehler.append(f"Doppelter Eincheck-Zeitpunkt, Abstand: {minuten} Minuten {sekunden} Sekunden")
                if status == "out":
                    fehler.append(f"Doppelter Auscheck-Zeitpunkt, Abstand: {minuten} Minuten {sekunden} Sekunden")

            if status == "in":
                letzter_status = "Eingecheckt"
            if status == "out":
                letzter_status = "Ausgecheckt"

            anfangs_status = status
            letzte_zeit = zeitpunkt

            ausgabe.append({"fehler": fehler, "status": letzter_status})

        return ausgabe
    
    except Exception as e:
        print("Fehler bei der Verarbeitung - IN/OUT Prüfung:", e)
        return None

    finally:

        # Terminal Ausgabe

        if fehler:
            print("Fehler gefunden:")
            for f in fehler:
                print("-", f)
        else:
            print("Korrekte Reihenfolge")

        print("Letzter Buchungsstand:", letzter_status)

###################################################################
# Daten Prüfen: Zeiträume 10min Max ohne Kühlung ##################
###################################################################

def check_zeitraeume_10minMax(transport_daten):
    try:
        ausgabe       = []
        fehler        = []
        status        = None
        letzte_status = None
        zeitpunkt     = None
        letzte_zeit   = None

        for eintrag in transport_daten:
            status    = (eintrag[4]).strip("'").lower() #[4] = Status 
            zeitpunkt = eintrag[5]                      #[5] = Zeitpunkt

            if status == "in" and letzte_status == "out":
                diff = (zeitpunkt - letzte_zeit).total_seconds() / 60
                if diff > 10:
                    fehler.append(f"Übergabe > 10 min")
                    break

            letzte_status = status
            letzte_zeit = zeitpunkt

            ausgabe.append(fehler)

        return ausgabe
    
    except Exception as e:
        print("Fehler bei der Verarbeitung - Zeitraum Prüfung 10min Max:", e)
        return None

    finally:

        # Terminal Ausgabe

        if fehler:
            print("Fehler gefunden:")
            for f in fehler:
                print("-", f)
        else:
            print("Korrekte Zeiträume (<= 10 min)")

###################################################################
# Daten Prüfen: Transportdauer 48h Max ############################
###################################################################

def check_transportdauer(transport_daten):

    try:
        ausgabe    = []
        fehler     = []
        status     = None
        startzeit  = None
        endzeit    = None
        zeitpunkt  = None

        for eintrag in transport_daten:
            status    = (eintrag[4]).strip("'").lower()  #[4] = Status
            zeitpunkt = eintrag[5]                       #[5] = Zeitpunkt

            if status == "in" and startzeit is None:
                startzeit = zeitpunkt
            if status == "out":
                endzeit = zeitpunkt

        if startzeit and endzeit:
            diff = (endzeit - startzeit).total_seconds() / 3600
            if diff > 48:
                fehler.append("Transportdauer > 48 h")

            ausgabe.append(fehler)

        return ausgabe
    
    except Exception as e:
        print("Fehler bei der Verarbeitung - Transportdauer 48h Max:", e)
        return None
    
    finally:

        # Terminal Ausgabe

        if fehler:
            print("Fehler gefunden:")
            for f in fehler:
                print("-", f)
        else:
            print("Korrekte Transportdauer (<= 48 h)")

###################################################################
# Daten Prüfen: Transportstations - Konsistenzprüfung #############
###################################################################

def check_GVZ_vor_KT(transport_daten, transportstation_daten):
    try:
        ausgabe       = []
        fehler        = []
        letzte_gvz_in = None  # Zeitpunkt des letzten GVZ-"in"

        for eintrag in transport_daten:
            station_id = eintrag[3]                     # [3] = TransportstationID
            status     = eintrag[4].strip("'").lower()  # [4] = "in" / "out"
            zeit       = eintrag[5]                     # [5] = Zeitstempel

            art = None
            for station in transportstation_daten:
                if station[0] == station_id:            # [0] = TransportstationID
                    art = station[2].strip("'").upper() # [2] = "GVZ" oder "KT"
                    break

            if art == "GVZ" and status == "in":
                letzte_gvz_in = zeit

            if art == "KT" and status == "out":
                if letzte_gvz_in is not None and letzte_gvz_in < zeit:
                    fehler.append("Einchecken Kühllager liegt zeitlich vor Auschecken LKW")

            ausgabe.append(fehler)

        return ausgabe

    except Exception as e:
        print("Fehler bei der Verarbeitung - GVZ_vor_KT:", e)
        return None

    finally:
        if fehler:
            print("Fehler gefunden:")
            for f in fehler:
                print("-", f)
        else:
            print("Korrekte Reihenfolge GVZ vor KT")


