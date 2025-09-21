import pyodbc
from collections import defaultdict

###################################################################
# Datenbank Zugriff - Transportdaten ##############################
###################################################################

def get_transport_daten(transportid, verbindungs_i):

    transport_daten = {}
    try:
        # Verbindung herstellen
        conn = pyodbc.connect(verbindungs_i)
        cursor = conn.cursor()

        # SQL-Abfrage
        abfrage = """
            SELECT * 
            FROM dbo.coolchain 
            WHERE transportid = ? 
            ORDER BY datetime
        """
        cursor.execute(abfrage, transportid)

        zeilen = cursor.fetchall()

        # Dictionary erstellen
        transport_daten = {}
        for idx, zeile in enumerate(zeilen, start=1):
            # Row ist ein pyodbc.Row -> in Liste konvertieren
            transport_daten[idx] = list(zeile)

        transport_daten_len = len(transport_daten)

        return transport_daten, transport_daten_len

    except Exception as e:
        print("Fehler beim Datenbankzugriff - Transportdaten:", e)
        return None

    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()
        
        # Terminal Ausgabe

        print(transport_daten)

###################################################################
# Datenbank Zugriff - Temperaturdaten #############################
###################################################################

def _baue_intervalle(transport_daten: dict):
    # Ereignisse je (transportID, stationID) sammeln und zeitlich sortieren
    events = defaultdict(list)
    for _, row in sorted(transport_daten.items(), key=lambda kv: kv[1][5]):  # sort by datetime in row[5]
        transport_id = row[2]
        station_id   = row[3]
        direction    = str(row[4]).strip().strip("'").lower()  # "'in'" -> in
        dt           = row[5]
        events[(transport_id, station_id)].append((dt, direction))

    # in/out paaren → Intervalle
    intervalle = defaultdict(lambda: defaultdict(list))  # [transportID][stationID] -> list of (start, end)
    for (transport_id, station_id), evts in events.items():
        evts.sort(key=lambda t: t[0])
        start = None
        for dt, direction in evts:
            if direction == "in":
                start = dt
            elif direction == "out" and start is not None and dt >= start:
                intervalle[transport_id][station_id].append((start, dt))
                start = None
        # Falls am Ende ein offenes "in" ohne "out" steht, ignorieren wir es bewusst.
    return intervalle


def get_temperatur_daten(transport_daten: dict, verbindungs_i: str):
    if not transport_daten:
        return {}

    # 1) Verweil-Intervalle aus den Transportereignissen bilden
    intervalle = _baue_intervalle(transport_daten)
    if not intervalle:
        return {}

    temperatur_daten = {}

    try:
        conn = pyodbc.connect(verbindungs_i)
        cursor = conn.cursor()

        # 2) Für jedes (transportID, stationID) alle Intervalle abfragen
        sql = """
            SELECT transportstationID, datetime, temperature
            FROM dbo.tempdata
            WHERE transportstationID = ?
              AND datetime >= ?
              AND datetime <= ?
            ORDER BY datetime
        """

        for transport_id, stations in intervalle.items():
            temperatur_daten[transport_id] = {}

            for station_id, ranges in stations.items():
                laufend = 1
                temperatur_daten[transport_id][station_id] = {}

                for start_dt, end_dt in ranges:
                    cursor.execute(sql, station_id, start_dt, end_dt)
                    for row in cursor.fetchall():
                        # row: (transportstationID, datetime, temperature)
                        temperatur_daten[transport_id][station_id][laufend] = [row[0], row[1], row[2]]
                        laufend += 1

        temperatur_daten_len = len(temperatur_daten)

        return temperatur_daten, temperatur_daten_len

    except Exception as e:
        print("Fehler beim Datenbankzugriff - Temperaturdaten:", e)
        return {}

    finally:
        try:
            cursor.close()
        except Exception:
            pass
        try:
            conn.close()
        except Exception:
            pass
        
        # Terminal Ausgabe

        print(temperatur_daten)