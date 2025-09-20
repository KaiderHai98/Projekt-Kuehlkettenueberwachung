from Han_DB_Zugriff_Zeiten import get_transport_daten
from Han_DB_Zugriff_Zeiten import get_temperatur_daten
import pyodbc

# Variablen
server = 'sc-db-server.database.windows.net'
database = 'supplychain'
username = 'rse'
password = 'Pa$$w0rd'

# Verbindung
verbindungs_i = (
    f"DRIVER={{ODBC Driver 18 for SQL Server}};"
    f"SERVER={server};"
    f"DATABASE={database};"
    f"UID={username};"
    f"PWD={password}"
)

# Beispiel: Daten holen
transportid        = input("Transport-ID: ")
transportstationID = input("TransportstationID-ID: ")
transport_daten    = get_transport_daten(transportid: str, verbindungs_i)
temperatur_daten   = get_temperatur_daten(transportstationID: str, verbindungs_i)
        
if transport_daten:
    print(f"{len(transport_daten)} Datensätze gefunden")
    # Hier kannst du mit den Daten weiterarbeiten
    for transport_datensatz in transport_daten:
        print(transport_datensatz)
else:
    print("Keine Daten gefunden")

if temperatur_daten:
    print(f"{len(temperatur_daten)} Datensätze gefunden")
    # Hier kannst du mit den Daten weiterarbeiten
    for temperatur_datensatz in temperatur_daten:
        print(temperatur_datensatz)
else:
    print("Keine Daten gefunden")
