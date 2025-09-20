

def pruefe_in_out(transport_daten):
    fehler = []
    letzter = None
    index = 0

    for row in transport_daten:
        status = row[4].strip("'").lower()
        if letzter == status:
            fehler.append(f"Zeile {index}: doppelt {status}")
        letzter = status
        index += 1

    return fehler, letzter
