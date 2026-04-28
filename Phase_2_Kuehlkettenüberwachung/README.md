# Phase 2 – IoT-Kühlkettenüberwachung

Diese Projektphase erweitert die Kühlkettenüberwachung aus Phase 1 um zusätzliche Funktionen zur Qualitäts- und Sicherheitsprüfung.

Das Programm liest Transportdaten aus einer SQL-Datenbank aus, wertet diese aus und gibt dem Anwender verständliche Meldungen zur Kühlkette aus. In Phase 2 kommen zusätzlich Temperaturüberwachung, Entschlüsselung verschlüsselter Stammdaten und Wetterdatenabfrage hinzu.

---

## Funktion

Das Programm prüft für einzelne oder mehrere Transport-IDs, ob die Kühlkette eingehalten wurde.

Dabei werden in Phase 2 folgende Funktionen umgesetzt:

### 1. Temperaturüberwachung der Kühlstationen
Das Programm liest Temperaturdaten aus der Tabelle `tempdata` und prüft, ob sich die Temperatur einer Kühlstation immer im erlaubten Bereich zwischen **+2 °C und +4 °C** befindet. Jede Abweichung wird als Temperaturfehler ausgegeben.

### 2. Verarbeitung verschlüsselter Lieferdaten
Die Stammdaten liegen in Phase 2 nicht mehr unverschlüsselt vor, sondern in den Tabellen `company_crypt` und `transportstation_crypt`.  
Das Programm entschlüsselt diese Daten mit **AES-CBC**, damit Firmennamen, Stationsnamen, Kategorien und Postleitzahlen weiterhin verwendet werden können.

### 3. Wetterdatenabfrage an den Auslagerorten
Wenn ein Zeitraum ohne Kühlung erkannt wird, kann das Programm zusätzlich die Außentemperatur am Auslagerungsort zur Auslagerungszeit anzeigen. Dafür wird die Postleitzahl der Station und eine Wetter-API verwendet.

### 4. Grundprüfungen aus Phase 1 bleiben erhalten
Zusätzlich bleiben die Prüfungen aus Phase 1 aktiv:

- Stimmigkeit der Kühlketteninformationen
- Zeiträume ohne Kühlung
- Transportdauer

---

## Enthaltene Dateien

- `Hauptprogramm_V4.py`  
  Startet das Programm und enthält die grafische Benutzeroberfläche.

- `DB_Zugriff_Libary_V4.py`  
  Liest Transportdaten, Temperaturdaten, Firmendaten und Stationsdaten aus der Datenbank aus.

- `Verarbeitung_Libary_V4.py`  
  Enthält die eigentliche Prüflogik für die Kühlkette.

- `README.md`  
  Diese Projekterklärung für Phase 2.

---

## Voraussetzungen

Damit das Programm funktioniert, müssen einige Bibliotheken und Systemkomponenten installiert sein.

### Benötigt werden

- Python 3
- `pyodbc`
- `pycryptodome`
- `requests`
- Microsoft ODBC Driver für SQL Server

---

## Installation

### 1. Python installieren
Installiere zuerst eine aktuelle Python-Version.

**Wichtig:**  
Bei der Installation sollte Python korrekt in Windows eingebunden sein.

### 2. Benötigte Bibliotheken installieren
Öffne ein Terminal oder die Eingabeaufforderung und installiere:

    py -m pip install pyodbc pycryptodome requests

### 2. Vorhandene Bibliotheken Prüfen
Öffne ein Terminal oder die Eingabeaufforderung und Prüfe die Installationen mit:

    py -m pip list

### 4. ODBC-Treiber prüfen bzw. installieren
Für den SQL-Zugriff muss zusätzlich ein passender Microsoft ODBC Driver für SQL Server vorhanden sein.

**Hinweis:**  
Falls das Programm bei dir bereits eine Verbindung zur Datenbank aufbauen kann, ist dieser Treiber schon vorhanden und du musst hier nichts weiter machen.

Ohne diesen Treiber kann `pyodbc` keine Verbindung zur Datenbank aufbauen.

---

## Start in Visual Studio Code

Das Projekt wurde für die Nutzung mit **Visual Studio Code** vorbereitet.

### Vorgehen

1. Projektordner in **Visual Studio Code** öffnen  
2. Prüfen, ob unten rechts der richtige Python-Interpreter ausgewählt ist  
3. Terminal in VS Code öffnen  
4. Das Hauptprogramm starten mit:

    py Hauptprogramm_V4.py

Falls mehrere Python-Versionen installiert sind, kann auch gezielt gestartet werden mit:

    py -3.13 Hauptprogramm_V4.py

---

## Bedienung des Programms

Nach dem Start öffnet sich die grafische Benutzeroberfläche.

### Möglichkeiten

- **Transport-ID eingeben**  
  Prüft genau einen Transport.

- **Prüfen**  
  Startet die Auswertung für die eingegebene Transport-ID.

- **Alle prüfen**  
  Prüft alle in der Datenbank vorhandenen Transport-IDs.

- **Löschen**  
  Setzt Eingabe und Ausgabefeld zurück.

- **Visual-Crossing-API-Key eingeben**  
  Wird benötigt, wenn bei Verstößen ohne Kühlung zusätzlich Wetterdaten abgefragt werden sollen.

---

## Wetter-API

Für die Wetterdatenabfrage wird ein API-Key von **Visual Crossing** benötigt.

### Vorgehen

1. Kostenlos bei Visual Crossing registrieren  
2. API-Key aus dem Account kopieren  
3. API-Key im Programm in das Feld **Visual-Crossing-API-Key** einfügen

Ohne API-Key läuft das Programm trotzdem weiter. In diesem Fall wird statt der Außentemperatur eine Hinweis-Meldung ausgegeben.

---

## Start über eine EXE-Datei

1. Die Datei `CoolChain.exe` per Doppelklick starten  
2. Die Benutzeroberfläche öffnet sich direkt  
3. Transport-ID eingeben  
4. Optional API-Key eintragen  
5. Prüfung starten  

---

## Hinweise

### Datenbankzugriff
Das Programm greift auf eine Microsoft-SQL-Server-Datenbank zu.  
Dafür müssen Server, Datenbankname, Benutzername und Passwort korrekt im Code hinterlegt sein.

### Wetterdaten
Die Wetterabfrage funktioniert nur mit gültigem API-Key.  
Ohne API-Key läuft das Programm trotzdem weiter, gibt aber statt einer Außentemperatur eine entsprechende Hinweis-Meldung aus.

### Verschlüsselung
Die verschlüsselten Stammdaten werden mit AES-CBC entschlüsselt.  
Verwendet werden dabei das vorgegebene Passwort und der vorgegebene Initialization Vector.

### Temperaturdaten
Temperaturwerte außerhalb des Bereichs von +2 °C bis +4 °C werden als Fehler erkannt und ausgegeben.

---

## Ziel dieser Projektphase

Phase 2 erweitert die reine Ablaufprüfung aus Phase 1 um zusätzliche Informationen zur Produktqualität und Datensicherheit.  
Dadurch kann nicht nur erkannt werden, **dass** ein Fehler vorliegt, sondern oft auch **warum** er kritisch ist.