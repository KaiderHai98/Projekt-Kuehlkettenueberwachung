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

# Import-Block
from DB_Zugriff_Libary import get_transport_daten
from DB_Zugriff_Libary import get_temperatur_daten
from DB_Zugriff_Libary import get_company_daten
from DB_Zugriff_Libary import get_transportstation_daten
from Verarbeitung_Libary import check_Daten_Eingang
from Verarbeitung_Libary import check_in_out
from Verarbeitung_Libary import check_zeitraeume_10minMax
from Verarbeitung_Libary import check_transportdauer
from Verarbeitung_Libary import check_GVZ_vor_KT
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
company_daten,          company_daten_len          = get_company_daten          (companyID, verbindungs_i)
transportstation_daten, transportstation_daten_len = get_transportstation_daten (transport_daten, verbindungs_i, transport_daten)

print ("Datenerfasssung erfolgreich abgeschlossen")

###################################################################
# Daten Kontrolle #################################################
###################################################################

eingangs_check                = check_Daten_Eingang      (transport_daten_len, temoratur_daten_len, company_daten_len, transportstation_daten_len)
in_out_check                  = check_in_out             (transport_daten)
zeitraum_check                = check_zeitraeume_10minMax(transport_daten)
transportdauer_check          = check_transportdauer     (transport_daten)
gvz_vor_kt_check              = check_GVZ_vor_KT         (transport_daten, transportstation_daten)


