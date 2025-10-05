# ##############################################################################################################
# Hauptprogramm: CoolChainProjekt
#  Datei: Hauptprogramm_V4.py
#
# Version: 4 vom: 24.09.2025
# Autoren:jowoeste
#
# Zugehörige Libarys:
# - DB_Zugriff_Libary_V3.py
# - Verarbeitung_Libary_V3.py
# 
# Funktionsbeschreibung: 
# Hauptprogramm & Benutzeroberfläche zur Eingabe der Transport-ID und Anzeige der Ergebnisse
# ##############################################################################################################

# Import-Block
import pyodbc
import tkinter as tk
from tkinter import messagebox, scrolledtext, ttk

"""\brief Importiert Funktionen zum Abrufen von Transport- und Temperaurdaten."""
from DB_Zugriff_Libary_V3 import (
    get_transport_daten,
    get_temperatur_daten,
    get_company_daten,
    get_transportstation_daten,
)

"""\brief Importiert die Funktion zur Verarbeitung der Transportdaten."""
from Verarbeitung_Libary_V3 import verarbeite_transport

# Verbindungsdaten
"""\brief SQL Server Hostname."""
server   = 'sc-db-server.database.windows.net'
"""\brief SQL Datenbankname."""
database = 'supplychain'
"""\brief Datenbank-Benutzername."""
username = 'rse'
"""\brief Datenbank-Passwort."""
password = 'Pa$$w0rd'

# Verbindungsstring
"""\brief ODBC-Verbindungsstring für pyodbc."""
verbindungs_i = (
    f"DRIVER={{ODBC Driver 18 for SQL Server}};"
    f"SERVER={server};"
    f"DATABASE={database};"
    f"UID={username};"
    f"PWD={password}"
)

# ##################################################################
# GUI Aufbau
# ##################################################################
'''
 @brief Grafische Benutzeroberfläche zur CoolChain Transportprüfung.
 @details 
 
 Grafische Benutzeroberfläche zur CoolChain Transportprüfung

 Dieses Programm bietet eine tkinter-GUI, um Transportdaten einzeln per ID oder
 alle Transporte aus der Datenbank abzurufen, zu verarbeiten und die
 Ergebnisse anzuzeigen.
'''
class TransportGUI:

    # ##################################################################
    # Benutzeroberfläche initialisieren
    # ##################################################################
    '''
    @brief Die Hauptklasse für die grafische Benutzeroberfläche (GUI).

    @details 

    Benutzeroberfläche initialisieren

    Initialisiert das Hauptfenster, die Widgets für die Eingabe,
    die Steuerung (Buttons) und die Ausgabe (ScrolledText) der Ergebnisse.
    '''
    def __init__(self, root):
        self.root = root
        self.root.title("CoolChain - Transportprüfung")
        self.root.geometry("720x480")
        self.root.resizable(True, True)

        # Überschrift
        tk.Label(root, text="CoolChain Transportprüfung", font=("Arial", 14, "bold")).pack(pady=(10,5))

        #Fenster in der breite ausfüllen
        frame_top = tk.Frame(root)
        frame_top.pack(fill="x", padx=12)

        # Eingabe-Feld für Transport-ID
        tk.Label(frame_top, text="Transport-ID:").pack(side="left")
        """\brief Das Eingabefeld für die Transport-ID. """
        self.entry = tk.Entry(frame_top, width=40)
        self.entry.pack(side="left", padx=(6,8))

        # Button zum Prüfen
        """\brief Button zum Starten der Prüfung einer einzelnen Transport-ID. """
        self.check_btn = tk.Button(frame_top, text="Prüfen", command=self.on_pruefen)
        self.check_btn.pack(side="left")

        # Button Feld reinigen
        """\brief Button zum Renigen der Eingabe und des Ausgabefeldes. """
        self.clear_btn = tk.Button(frame_top, text="Löschen", command=self.on_clear)
        self.clear_btn.pack(side="left", padx=6)

        # Button: Alle prüfen
        """Button zum Starten der Prüfung aller vorhandenen Transporte. """
        self.all_btn = tk.Button(frame_top, text="Alle prüfen", command=self.on_alle_pruefen)
        self.all_btn.pack(side="left", padx=6)

        # Textfeld für Ausgaben
        tk.Label(root, text="Meldungen:").pack(anchor="w", padx=12, pady=(10,0))
        """\brief ScrolledText-Widget zur Anzeige der Prüfergebnisse und Meldungen. """
        self.output = scrolledtext.ScrolledText(root, wrap="word", height=18)
        self.output.pack(fill="both", expand=True, padx=12, pady=(0,12))

        # Statusleiste
        """\brief Statusleiste zur Anzeige des aktuellen Status der Anwendung. """
        self.status = tk.StringVar()
        self.status.set("Bereit")
        tk.Label(root, textvariable=self.status, anchor="w").pack(fill="x", padx=12, pady=(0,6))


    # ##################################################################
    # Funktion zur Prüfung der Transport-ID
    # ##################################################################
    '''
    @brief Führt die Prüfung eines einzelnen Transports basierend auf der eingegebenen ID durch.

    @details Liest die Transport-ID aus dem Eingabefeld, ruft alle notwendigen Daten
    (Transport, Temperatur, Unternehmen, Station) aus der Datenbank ab und
    übergibt diese zur Verarbeitung. Die generierten Meldungen werden im
    Ausgabefeld angezeigt. Stellt Status-Updates bereit.
    '''
    def on_pruefen(self):



        transportid = self.entry.get().strip()
        if not transportid:
            messagebox.showerror("Fehler", "Bitte eine Transport-ID eingeben!")
            return

        try:
            # Status aktualisieren: Prüfung läuft
            self.status.set("Prüfe Transport-ID...")
            self.root.update_idletasks()


            # Datenbankzugriffe
            transport_daten, _        = get_transport_daten(transportid, verbindungs_i)
            temperatur_daten, _       = get_temperatur_daten(transport_daten, verbindungs_i)
            company_daten, _          = get_company_daten(transport_daten, verbindungs_i)
            transportstation_daten, _ = get_transportstation_daten(transport_daten, verbindungs_i)

            # Verarbeitung
            meldungen = verarbeite_transport(
                transport_daten, temperatur_daten, company_daten, transportstation_daten
            )

            # Ausgabe im Textfeld
            self.output.delete("1.0", tk.END)
            self.output.insert(tk.END, f"Transport-ID: {transportid}\n")
            self.output.insert(tk.END, "--------------------------------------------------\n")
            for m in meldungen:
                self.output.insert(tk.END, f" -> {m}\n")
            
            #Status aktualisieren
            self.status.set("Prüfung abgeschlossen")

        except Exception as e:
            messagebox.showerror("Fehler", f"Ein Fehler ist aufgetreten:\n{e}")

    # ##################################################################
    # Funktion: Alle Transporteid meldungen ausgeben
    # ##################################################################
    '''
    @brief Führt die Prüfung aller in der Datenbank vorhandenen Transporte durch.

    @details Ruft zunächst alle eindeutigen Transport-IDs ab. Iteriert dann
    über jede ID, holt die zugehörigen Daten, verarbeitet sie und sammelt
    alle generierten Meldungen. Die Ergebnisse werden nach Meldungstext sortiert
    und im Ausgabefeld angezeigt. Stellt Status-Updates bereit.
    '''
    def on_alle_pruefen(self):
        
        try:
            # Status aktualisieren: Prüfung läuft
            self.status.set("Bitte warten, alle Transporte werden geprüft ...")
            self.root.update_idletasks()

            # Datenbankverbindung herstellen
            conn = pyodbc.connect(verbindungs_i)
            cursor = conn.cursor()

            # Alle Transport-IDs aus der Datenbank holen
            cursor.execute("SELECT DISTINCT transportid FROM dbo.coolchain ORDER BY transportid")
            alle_ids = [row[0] for row in cursor.fetchall()]

            cursor.close()
            conn.close()

            ergebnisse = []

            # Für jede Transport-ID die Meldungen holen
            for i, tid in enumerate(alle_ids, start=1):
                transport_daten, _        = get_transport_daten(tid, verbindungs_i)
                temperatur_daten, _       = get_temperatur_daten(transport_daten, verbindungs_i)
                company_daten, _          = get_company_daten(transport_daten, verbindungs_i)
                transportstation_daten, _ = get_transportstation_daten(transport_daten, verbindungs_i)

                meldungen = verarbeite_transport(
                    transport_daten, temperatur_daten, company_daten, transportstation_daten
                )

                for m in meldungen:
                    ergebnisse.append((tid, m))
            

            # Ergebnisse sortieren nach Meldungstext
            ergebnisse.sort(key=lambda x: x[1])

            # Ausgabe ins Textfeld
            self.output.delete("1.0", tk.END)
            self.output.insert(tk.END, "Alle Transport-IDs - Prüfungen\n")
            self.output.insert(tk.END, "==================================================\n")

            for tid, m in ergebnisse:
                self.output.insert(tk.END, f"{tid} -> {m}\n")

            self.status.set(f"{len(alle_ids)} Transporte geprüft")

        except Exception as e:
            messagebox.showerror("Fehler", f"Ein Fehler ist aufgetreten:\n{e}")

    # ##################################################################
    # Funktion zum Löschen der Eingabe und Ausgabe
    # ##################################################################
    '''
    @brief Löscht die Eingabe im Transport-ID-Feld und leert das Ausgabefeld.

    @details Setzt den Status auf "Bereit" zurück.
    '''
    def on_clear(self):

        self.entry.delete(0, tk.END)
        self.output.delete("1.0", tk.END)
        self.status.set("Bereit")        


# ##################################################################
# Programmeinstieg
# ##################################################################
'''
@brief Hauptfunktion des Programms.

@details Erstellt das Hauptfenster (root) und instanziiert die TransportGUI-Klasse.
Startet die tkinter-Ereignisschleife (mainloop).
'''
if __name__ == "__main__":

    root = tk.Tk()
    app = TransportGUI(root)
    root.mainloop()