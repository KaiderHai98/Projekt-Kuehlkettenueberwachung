from DB_Zugriff_Libary import get_transport_daten
from DB_Zugriff_Libary import get_temperatur_daten
from DB_Zugriff_Libary import get_company_daten
from Verarbeitung_Libary import pruefe_in_out
from Verarbeitung_Libary import check_zeitraeume_10minMax
import pyodbc

# Verbindungsdaten
server = 'sc-db-server.database.windows.net'
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

# Daten holen
transportid        = input("Transport-ID: ")
transportstationID = input("TransportstationID-ID: ")
companyID          = input("Company-ID: ")

###################################################################
# Datenbank Zugriff ###############################################
###################################################################
   
transport_daten    = get_transport_daten(transportid, verbindungs_i)
temperatur_daten   = get_temperatur_daten(transportstationID, verbindungs_i)
company_daten      = get_company_daten(companyID, verbindungs_i)

###################################################################
# Daten Kontrolle #################################################
###################################################################

in_out_fehler, in_out_aktuell = pruefe_in_out(transport_daten)
zeitraum_check = check_zeitraeume_10minMax(transport_daten)

