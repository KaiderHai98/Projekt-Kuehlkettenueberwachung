import pyodbc
from    DB_Zugriff_Libary_V2 import get_transport_daten

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