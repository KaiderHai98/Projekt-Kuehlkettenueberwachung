import pyodbc

#Varibalen
server = 'sc-db-server.database.windows.net'
database = 'supplychain'
username = 'rse'
password = 'Pa$$w0rd'

#Verbindung
conn_str = (
    f"DRIVER={{ODBC Driver 18 for SQL Server}};"
    f"SERVER={server};"
    f"DATABASE={database};"
    f"UID={username};"
    f"PWD={password}"
)

try:
    # Verbindung herstellen
    conn = pyodbc.connect(conn_str)
    print("Verbindung erfolgreich hergestellt")

    # Cursor erzeugen
    cursor = conn.cursor()

    # Benutzereingabe
    companyID = input("Bitte geben Sie eine Company-ID ein: ")

    # SQL-Abfrage
    abfrage = "SELECT * FROM dbo.company WHERE companyID = ?"
    cursor.execute(abfrage, companyID)


    # Ergebnisse abrufen und anzeigen
    daten = cursor.fetchall()
    if daten:
        print (f"\nDaten Company-ID {companyID}:")
        for datensatz in daten:
            print(datensatz)
    else:
        print(f"Keine Daten für Company-ID {companyID} gefunden.")


except Exception as e:
    print("Fehler beim Datenbankzugriff:", e)

finally:
    #Alles im finally:-Block wird immer ausgeführt, egal ob vorher ein Fehler passiert ist oder nicht
    # Verbindung schließen
    if 'cursor' in locals():
        cursor.close()
    if 'conn' in locals():
        conn.close()