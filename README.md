# ###############################################################################
# Projekt-Kühlkettenüberwachung
# Schulprojekt:
# Eine betriebsinterne Qualitätssicherung zur automatischen Kühlkettenüberwachung
# ###############################################################################

# ##################################################################
# Doxygen
# ##################################################################

1. FILTER_PATTERNS in Doxyfile anpassen
2. Doxygen aktualiesieren: doxygen Doxyfile
3. Doxygen aufrufen: start docs\html\index.html

# ##################################################################
# Projektbeschreibung
# ##################################################################

Projektbeschreibung:

Das Projekt „Kühlkettenüberwachung“ prüft Transportvorgänge auf Grundlage von in einer SQL-Datenbank gespeicherten Ereignissen. Die Verarbeitung erfolgt über die Funktion verarbeite_transport, die Transportdaten sammelt, zeitlich sortiert und anschließend definierte Prüfungen ausführt. Zunächst wird erkannt, ob kein Transport vorhanden ist („Es gibt gar keinen Eintrag“). Anschließend werden die drei Kernvorgaben kontrolliert: die Vollständigkeit und zeitliche Stimmigkeit der Kühlketteneinträge (u. a. Erkennung fehlender Auscheck-Zeitpunkte am Ende bzw. in der Mitte eines Vorgangs), die zulässige Unterbrechungsdauer ohne Kühlung von höchstens zehn Minuten zwischen einem out und dem folgenden in („Übergabe > 10 min“) sowie die maximale Transportdauer von 48 Stunden zwischen erstem in und letztem out („Transportdauer > 48h“). Darüber hinaus umfasst die Verarbeitung weitere Konsistenzprüfungen: doppelter Auscheck-Zeitpunkt an derselben Station (Meldung mit Minutenabstand), Aus und wieder Einchecken im gleichen Kühllager nach abgeschlossenem GVZ-Zyklus sowie die Reihenfolge KT vor GVZ, d. h. es wird beanstandet, wenn ein GVZ-Einchecken zeitlich vor dem Auschecken des LKW liegt („Einchecken Kühllager liegt zeitlich vor Auschecken LKW“). Alle festgestellten Auffälligkeiten werden als Textmeldungen zurückgegeben; sind keine vorhanden, lautet das Ergebnis „korrekt“. Die Funktion arbeitet auf den übergebenen Datenstrukturen (transport_daten, temperatur_daten, company_daten, transportstation_daten) und bestimmt Status (in/out) sowie die Art der Station (GVZ/KT) zur Einordnung der Ereignisse.
