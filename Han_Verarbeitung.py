from Han_DB_Zugriff_Zeiten import get_transport_daten
from Han_DB_Zugriff_Zeiten import get_temperatur_daten

# Beispiel: Daten holen
transport_id       = input("Transport-ID: ")
transportstationID = input("TransportstationID-ID: ")
daten_transport    = get_transport_daten(transport_id)
daten_temperatur   = get_temperatur_daten(transportstationID)




    # Ergebnisse abrufen und anzeigen
    daten = cursor.fetchall()
    if daten:
        print (f"\nDaten Transport-ID {transport_id}:")
        for datensatz in daten:
            print(datensatz)
    else:
        print(f"Keine Daten für Transport-ID {transport_id} gefunden.")


        
if daten_transport:
    print(f"{len(daten_transport)} Datensätze gefunden")
    # Hier kannst du mit den Daten weiterarbeiten
    for row in daten_transport:
        # z.B. einzelne Werte nutzen
        print(row.datetime, row.temperatur, row.feuchtigkeit)
else:
    print("Keine Daten gefunden")

if daten_temperatur:
    print(f"{len(daten_temperatur)} Datensätze gefunden")
    # Hier kannst du mit den Daten weiterarbeiten
    for row in daten_temperatur:
        # z.B. einzelne Werte nutzen
        print(row.datetime, row.temperatur, row.feuchtigkeit)
else:
    print("Keine Daten gefunden")
