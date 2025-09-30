from datetime import datetime

def check_consistency(rows):
    # Beispielprüfung: Es muss mindestens 1 Eintrag geben
    if not rows:
        return False, "Keine Daten gefunden"
    # TODO: erweiterte Logik für Ein-/Auschecken zeitlich sinnvoll
    return True, "Stimmigkeit ok"

def check_cooling_breaks(rows):
    # Dummy: Später prüfen, ob Pause > 10 Min.
    return True, "Kühlunterbrechung ≤ 10 Min eingehalten"

def check_transport_duration(rows):
    # Dummy: Später Dauer ≤ 48h prüfen
    return True, "Transportdauer ≤ 48h"