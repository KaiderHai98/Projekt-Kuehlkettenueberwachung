# IoT-Kühlkettenüberwachung

Python-Projekt zur automatischen Prüfung von Transportdaten einer digitalen Kühlkette.

Das Programm wurde im Rahmen des ETS-Supplychain-Projekts entwickelt und dient der betriebsinternen Qualitätssicherung. Ziel ist es, Transportabläufe aus einer SQL-Datenbank auszulesen, fachlich zu prüfen und mögliche Verstöße gegen die Kühlkette übersichtlich auszugeben. Grundlage sind die Projektanforderungen aus Phase 1 und Phase 2.

---

## Projektüberblick

Bei der Kühlkettenüberwachung wird geprüft, ob ein Produkt während seines gesamten Transports korrekt behandelt wurde. Dazu wertet das Programm Ein- und Auscheckvorgänge, Aufenthaltszeiten, Temperaturdaten und ergänzende Informationen aus. Die Daten stammen aus einer Microsoft-SQL-Server-Datenbank. Phase 2 baut dabei auf dem Grundsystem aus Phase 1 auf und erweitert es um zusätzliche Qualitäts- und Sicherheitsfunktionen.

---

## Phase 1 – Grundprüfung der Kühlkette

In Phase 1 wird überprüft, ob die grundlegenden Bedingungen der Kühlkette eingehalten wurden. Dabei werden folgende Punkte kontrolliert:

- **Stimmigkeit der Kühlketteninformationen**  
  Es wird geprüft, ob Ein- und Auscheckvorgänge logisch und zeitlich sinnvoll aufgebaut sind.

- **Zeiträume ohne Kühlung**  
  Die Zeit zwischen dem Auschecken an einer Station und dem Einchecken an der nächsten Station darf **10 Minuten** nicht überschreiten.

- **Transportdauer**  
  Die gesamte Transportdauer eines Produkts darf **48 Stunden** nicht überschreiten.
  Zusätzlich erkennt das Programm unter anderem folgende Auffälligkeiten:
- fehlende Auscheck-Zeitpunkte
- doppelte Auscheck-Vorgänge
- falsche Reihenfolge zwischen Kühltransporter und Kühllager
- erneutes Einchecken im gleichen Kühllager
- komplett fehlende Einträge

Die Ergebnisse werden für einzelne Transport-IDs oder gesammelt für alle vorhandenen Transporte ausgegeben.

---

## Phase 2 – Erweiterte Kühlkettenüberwachung

Phase 2 ergänzt das Grundprogramm um drei weitere Funktionen:

1. Temperaturüberwachung der Kühlstationen
Das Programm wertet zusätzlich Temperaturmessungen aus der Tabelle `tempdata` aus. Dabei wird geprüft, ob die Kühltemperatur jeder beteiligten Station im erlaubten Bereich zwischen **+2 °C und +4 °C** liegt.

2. Verarbeitung verschlüsselter Lieferdaten
Die Stammdaten der Firmen und Transportstationen liegen in Phase 2 verschlüsselt in den Tabellen `company_crypt` und `transportstation_crypt`. Das Programm entschlüsselt diese Daten per **AES-CBC**, damit Stationsnamen, Kategorien und Postleitzahlen weiterhin verarbeitet werden können.

3. Wetterdatenabfrage an den Auslagerorten
Wenn ein Zeitraum ohne Kühlung erkannt wird, ergänzt das Programm die Meldung um die Außentemperatur am Auslagerungsort zur Auslagerungszeit. Dafür wird die Postleitzahl der Station und eine Wetter-API verwendet.

---

## Funktionen des Programms

Das Projekt bietet unter anderem folgende Funktionen:

- Prüfung einer einzelnen Transport-ID
- Prüfung aller vorhandenen Transporte
- Ausgabe verständlicher Fehlermeldungen
- grafische Benutzeroberfläche zur einfachen Nutzung
- Auswertung von Transportdaten, Temperaturdaten und Wetterdaten
- Verarbeitung verschlüsselter Stammdaten aus Phase 2

---

## Projektstruktur

Beispielhafter Aufbau des Projekts:

- `Hauptprogramm_V4.py`  
  Startet das Programm und enthält die grafische Benutzeroberfläche.

- `DB_Zugriff_Libary_V4.py`  
  Liest Transport-, Temperatur-, Firmen- und Stationsdaten aus der Datenbank.

- `Verarbeitung_Libary_V4.py`  
  Enthält die eigentliche Prüflogik für die Kühlkette.

- `Doxyfile`  
  Konfigurationsdatei für die automatische Programmdokumentation mit Doxygen.

---

## Verwendete Technologien

- **Python**
- **Tkinter** für die grafische Benutzeroberfläche
- **pyodbc** für den Zugriff auf den Microsoft SQL Server
- **pycryptodome** für die Entschlüsselung der verschlüsselten Daten
- **requests** für die Wetterdatenabfrage
- **Doxygen** für die Programmdokumentation

---

## Ziel des Projekts

Das Ziel des Projekts ist die automatische und nachvollziehbare Prüfung einer digitalen Kühlkette. Das Programm soll Verstöße zuverlässig erkennen, verständlich darstellen und dem Anwender eine einfache Bewertung des Transportverlaufs ermöglichen.

---

## Hinweis

Dieses Repository dokumentiert die Entwicklung des Projekts über mehrere Projektphasen hinweg. Phase 1 bildet die fachliche Grundprüfung der Kühlkette ab, während Phase 2 das System um Temperaturüberwachung, Verschlüsselung und Wetterdaten erweitert.

---

## Doxygen-Dokumentation lokal starten

1. Terminal im Projekt-Hauptordner öffnen
2. Alte Doxygen-Ausgabe löschen
3. Doxygen mit der vorhandenen `Doxyfile` ausführen
4. In den erzeugten Ordner `docs/html` wechseln
5. Dort einen lokalen Python-Webserver starten
6. Die Dokumentation im Browser unter `http://127.0.0.1:8000` öffnen

### Beispielbefehl: Doxygen-Doku öffen unter Windows mit Automatischen Start

**Visual Studios starten, Folder Projekt-Hauptordner ("Projekt-Kuelkettenueberwachung") öffnen und folgendes im Terminal ausführen:**

#### Befehl:
```$doxyfile = Get-ChildItem -Path . -Filter "Doxyfile" -File -Recurse | Select-Object -First 1

if (-not $doxyfile) {
    Write-Host "Keine Doxyfile gefunden. Bitte PowerShell im Projektordner oder einem übergeordneten Ordner öffnen."
    exit
}

Set-Location $doxyfile.Directory.FullName

if (Test-Path ".\docs") {
    Remove-Item ".\docs" -Recurse -Force
}

doxygen Doxyfile

if (-not (Test-Path ".\docs\html\index.html")) {
    Write-Host "Doxygen wurde nicht korrekt erzeugt. docs/html/index.html fehlt."
    exit
}

Set-Location ".\docs\html"

Start-Process "http://127.0.0.1:8000/index.html"

python -m http.server 8000