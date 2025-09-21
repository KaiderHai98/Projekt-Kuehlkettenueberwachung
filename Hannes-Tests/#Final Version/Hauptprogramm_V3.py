###############################################################################################################
## Hauptprogramm: CoolChainProjekt
#  Datei: Hauptprogramm_V3.py
#
# Version: 3 vom: 21.09.2025
# Autoren:
#
# Zugehörige Libarys:
# - DB_Zugriff_Libary_V3.py
# - Verarbeitung_Libary_V3.py
# 
# Funktionsbeschreibung: 
# Hauptprogramm zur Steuerung der Datenbankabfrage und der Datenverarbeitung
###############################################################################################################

################################################################################################################
#     Testfälle:
#1.   72359278599178561029675 korrekt 
#2.   15668407856331648336231 Übergabe > 10 min  
#3.   73491878556297128760578 korrekt 
#4.   99346757838434834886542 Transportdauer > 48h und Übergabe > 10 min  
#5.   46204863139457546291334 korrekt 
#6.   77631003455214677542311 Übergabe > 10 min 
#7.   34778534098134729847267 korrekt 
#8.   64296734612883933474299 Auscheck-Zeitpunkt fehlt am Ende (kein Fehler., da nicht abgeschl.) 
#9.   84356113249506843372979 korrekt 
#10.  23964376768701928340034 Auscheck-Zeitpunkt fehlt in der Mitte 
#11.  55638471099438572108556 Einchecken Kühllager liegt zeitlich vor Auschecken LKW 
#12.  84552276793340958450995 Übergabe > 10 min 
#13.  96853785349211053482893 korrekt 
#14.  68345254400506854834562 Aus und wieder Einchecken im gleichen Kühllager 
#15.  67424886737245693583645 Doppelter Ausscheck-Zeitpunkt (Abstand 12 min) 
#16.  85746762813849598680239 korrekt 
#17.  56993454245564893300000 Es gibt gar keinen Eintrag 
#18.  95662334024905944384522 korrekt 
#19.  13456783852887496020345 korrekt 
#20.  76381745965049879836902 korrekt
################################################################################################################  

# Import-Block
from DB_Zugriff_Libary_V3 import get_transport_daten, get_temperatur_daten, get_company_daten, get_transportstation_daten
from Verarbeitung_Libary_V3 import verarbeite_transport

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

###################################################################
# Datenbank Zugriff ###############################################
###################################################################

print("infos in der variable transport_daten")
transport_daten,        transport_daten_len        = get_transport_daten        (transportid, verbindungs_i)
print("infos in der variable temperatur_daten")
temperatur_daten,       temoratur_daten_len        = get_temperatur_daten       (transport_daten, verbindungs_i)
print("infos in der variable company_daten")
company_daten,          company_daten_len          = get_company_daten          (transport_daten, verbindungs_i)
print("infos in der variable transportstation_daten")
transportstation_daten, transportstation_daten_len = get_transportstation_daten (transport_daten, verbindungs_i)

print ("Datenerfasssung erfolgreich abgeschlossen")

###################################################################
# Daten Kontrolle #################################################
###################################################################

meldungen = verarbeite_transport(transport_daten, temperatur_daten, company_daten, transportstation_daten)

print("--------------------------------------------------")
print("Transport-ID:", transportid)
for m in meldungen:
    print(" ->", m)
