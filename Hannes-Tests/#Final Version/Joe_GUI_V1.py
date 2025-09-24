###############################################################################################################
## Hauptprogramm: CoolChainProjekt
#  Datei: Joe_GUI_V1.py
#
# Version: 3 vom: 24.09.2025
# Autoren:jowoeste
#
# Zugehörige Libarys:
# - DB_Zugriff_Libary_V3.py
# - Verarbeitung_Libary_V3.py
# - Hauptprogramm_V3.py
# 
# Funktionsbeschreibung: 
# Hauptprogramm & Benutzeroberfläche zur Eingabe der Transport-ID und Anzeige der Ergebnisse
###############################################################################################################

# Import-Block
import tkinter as tk
from tkinter import messagebox, scrolledtext
from DB_Zugriff_Libary_V3 import (
    get_transport_daten,
    get_temperatur_daten,
    get_company_daten,
    get_transportstation_daten,
)
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


###################################################################
# GUI Aufbau
###################################################################

class TransportGUI:

    #Benutzeroberfläche initialisieren
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
        self.entry = tk.Entry(frame_top, width=40)
        self.entry.pack(side="left", padx=(6,8))

        # Button zum Prüfen
        self.check_btn = tk.Button(frame_top, text="Prüfen", command=self.on_pruefen)
        self.check_btn.pack(side="left")

        # Button Feld reinigen
        self.clear_btn = tk.Button(frame_top, text="Löschen", command=self.on_clear)
        self.clear_btn.pack(side="left", padx=6)

        # Textfeld für Ausgaben
        tk.Label(root, text="Meldungen:").pack(anchor="w", padx=12, pady=(10,0))
        self.output = scrolledtext.ScrolledText(root, wrap="word", height=18)
        self.output.pack(fill="both", expand=True, padx=12, pady=(0,12))

        # Statusleiste
        self.status = tk.StringVar()
        self.status.set("Bereit")
        tk.Label(root, textvariable=self.status, anchor="w").pack(fill="x", padx=12, pady=(0,6))


###################################################################
# Bedienfunktionen
###################################################################

# Funktion zur Prüfung der Transport-ID
    def on_pruefen(self):
        transportid = self.entry.get().strip()
        if not transportid:
            messagebox.showerror("Fehler", "Bitte eine Transport-ID eingeben!")
            return

        try:
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

        except Exception as e:
            messagebox.showerror("Fehler", f"Ein Fehler ist aufgetreten:\n{e}")

#Funktion zum Löschen der Eingabe und Ausgabe
    def on_clear(self):
        self.entry.delete(0, tk.END)
        self.output.delete("1.0", tk.END)
        self.status.set("Bereit")        


###################################################################
# Programmeinstieg
###################################################################

if __name__ == "__main__":
    root = tk.Tk()
    app = TransportGUI(root)
    root.mainloop()