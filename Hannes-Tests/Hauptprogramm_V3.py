###################################################
## Kopfzeile: CoolChainProjekt
# 
# Hauptprogramm
# Version: XX vom: XX
# Autoren:
#
# Zugehörige Libarys:
# - DB_Zugriff_Libary.py
# - Verarbeitung_Libary.py
# 
# Funktionsbeschreibung: XX
###################################################

#   72359278599178561029675

# Import-Block
from DB_Zugriff_Libary_V3 import get_transport_daten
from DB_Zugriff_Libary_V3 import get_temperatur_daten
from DB_Zugriff_Libary_V3 import get_company_daten
from DB_Zugriff_Libary_V3 import get_transportstation_daten

import pyodbc

# Verbindungsdaten
server   = 'sc-db-server.database.windows.net'
database = 'supplychain'
username = 'rse'
password = 'Pa$$w0rd'

# Verbindungsstring
verbindungs_i = (
    f"DRIVER={{ODBC Driver 18 for SQL Server}};"
    f"SERVER={server};"
    f"DATABASE={database};"
    f"UID={username};"
    f"PWD={password}"
)

# Transport-Daten einholen
transportid        = input("Transport-ID: ")
companyID          = 1703 #input("Company-ID: ")

###################################################################
# Datenbank Zugriff ###############################################
###################################################################
   
transport_daten,        transport_daten_len        = get_transport_daten        (transportid, verbindungs_i)
temperatur_daten,       temoratur_daten_len        = get_temperatur_daten       (transport_daten, verbindungs_i)
company_daten,          company_daten_len          = get_company_daten          (transport_daten, verbindungs_i)
transportstation_daten, transportstation_daten_len = get_transportstation_daten (transport_daten, verbindungs_i)

print ("Datenerfasssung erfolgreich abgeschlossen")

###################################################################
# Daten Kontrolle #################################################
###################################################################
