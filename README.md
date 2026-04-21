# IoT-Kühlkettenüberwachung

Python-Projekt zur automatischen Prüfung von Transportdaten einer digitalen Kühlkette.

Das Programm wurde im Rahmen des ETS-Supplychain-Projekts entwickelt und dient der betriebsinternen Qualitätssicherung. Ziel ist es, Transportabläufe aus einer SQL-Datenbank auszulesen, fachlich zu prüfen und mögliche Verstöße gegen die Kühlkette übersichtlich auszugeben. Grundlage sind die Projektanforderungen aus Phase 1 und Phase 2. :contentReference[oaicite:2]{index=2} :contentReference[oaicite:3]{index=3}

---

## Projektüberblick

Bei der Kühlkettenüberwachung wird geprüft, ob ein Produkt während seines gesamten Transports korrekt behandelt wurde. Dazu wertet das Programm Ein- und Auscheckvorgänge, Aufenthaltszeiten, Temperaturdaten und ergänzende Informationen aus. Die Daten stammen aus einer Microsoft-SQL-Server-Datenbank. Phase 2 baut dabei auf dem Grundsystem aus Phase 1 auf und erweitert es um zusätzliche Qualitäts- und Sicherheitsfunktionen. :contentReference[oaicite:4]{index=4} :contentReference[oaicite:5]{index=5}

---

## Phase 1 – Grundprüfung der Kühlkette

In Phase 1 wird überprüft, ob die grundlegenden Bedingungen der Kühlkette eingehalten wurden. Dabei werden folgende Punkte kontrolliert:

- **Stimmigkeit der Kühlketteninformationen**  
  Es wird geprüft, ob Ein- und Auscheckvorgänge logisch und zeitlich sinnvoll aufgebaut sind.

- **Zeiträume ohne Kühlung**  
  Die Zeit zwischen dem Auschecken an einer Station und dem Einchecken an der nächsten Station darf **10 Minuten** nicht überschreiten.

- **Transportdauer**  
  Die gesamte Transportdauer eines Produkts darf **48 Stunden** nicht überschreiten. :contentReference[oaicite:6]{index=6}

Zusätzlich erkennt das Programm unter anderem folgende Auffälligkeiten:
- fehlende Auscheck-Zeitpunkte
- doppelte Auscheck-Vorgänge
- falsche Reihenfolge zwischen Kühltransporter und Kühllager
- erneutes Einchecken im gleichen Kühllager
- komplett fehlende Einträge

Die Ergebnisse werden für einzelne Transport-IDs oder gesammelt für alle vorhandenen Transporte ausgegeben. :contentReference[oaicite:7]{index=7}

---

## Phase 2 – Erweiterte Kühlkettenüberwachung

Phase 2 ergänzt das Grundprogramm um drei weitere Funktionen:

1. Temperaturüberwachung der Kühlstationen
Das Programm wertet zusätzlich Temperaturmessungen aus der Tabelle `tempdata` aus. Dabei wird geprüft, ob die Kühltemperatur jeder beteiligten Station im erlaubten Bereich zwischen **+2 °C und +4 °C** liegt. :contentReference[oaicite:8]{index=8}

2. Verarbeitung verschlüsselter Lieferdaten
Die Stammdaten der Firmen und Transportstationen liegen in Phase 2 verschlüsselt in den Tabellen `company_crypt` und `transportstation_crypt`. Das Programm entschlüsselt diese Daten per **AES-CBC**, damit Stationsnamen, Kategorien und Postleitzahlen weiterhin verarbeitet werden können. :contentReference[oaicite:9]{index=9}

3. Wetterdatenabfrage an den Auslagerorten
Wenn ein Zeitraum ohne Kühlung erkannt wird, ergänzt das Programm die Meldung um die Außentemperatur am Auslagerungsort zur Auslagerungszeit. Dafür wird die Postleitzahl der Station und eine Wetter-API verwendet. :contentReference[oaicite:10]{index=10}

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
- **Doxygen** für die Programmdokumentation :contentReference[oaicite:11]{index=11} :contentReference[oaicite:12]{index=12} :contentReference[oaicite:13]{index=13}

---

## Ziel des Projekts

Das Ziel des Projekts ist die automatische und nachvollziehbare Prüfung einer digitalen Kühlkette. Das Programm soll Verstöße zuverlässig erkennen, verständlich darstellen und dem Anwender eine einfache Bewertung des Transportverlaufs ermöglichen.

---

## Hinweis

Dieses Repository dokumentiert die Entwicklung des Projekts über mehrere Projektphasen hinweg. Phase 1 bildet die fachliche Grundprüfung der Kühlkette ab, während Phase 2 das System um Temperaturüberwachung, Verschlüsselung und Wetterdaten erweitert. :contentReference[oaicite:14]{index=14} :contentReference[oaicite:15]{index=15}
