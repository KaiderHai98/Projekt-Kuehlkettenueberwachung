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
# Benutzeroberfläche zur Eingabe der Transport-ID und Anzeige der Ergebnisse
###############################################################################################################

import tkinter as tk
from tkinter import messagebox, scrolledtext
import threading
from Hauptprogramm_V3 import hole_transport_meldungen, verbindungs_i, get_transport_daten

class TransportGUI:

    #Benutzeroberfläche
    def __init__(self, root):
        self.root = root
        self.root.title("CoolChain Transportprüfung")
        self.root.geometry("600x400")
        self.root.resizable(True, True)

        # Überschrift
        tk.Label(root, text="CoolChain Transportprüfung", font=("Arial", 14, "bold")).pack(pady=(10,5))

        #Fenster in der breite ausfüllen
        frame_top = tk.Frame(root)
        frame_top.pack(fill="x", padx=12)

        # Eingabe-Feld für Transport-ID
        self.label = tk.Label(root, text="Transport-ID eingeben:")
        self.label.pack(pady=10)

        self.entry = tk.Entry(root, width=40)
        self.entry.pack(pady=5)

        # Button zum Prüfen
        self.button = tk.Button(root, text="Prüfen", command=self.pruefe_transport)
        self.button.pack(pady=10)

        # Button Feld reinigen
        self.clear_btn = tk.Button(frame_top, text="Löschen", command=self.on_clear)
        self.clear_btn.pack(side="left", padx=6)

        # Textfeld für Ausgaben
        self.output = tk.Text(root, wrap="word", width=70, height=15)
        self.output = scrolledtext.ScrolledText(root, wrap="word", height=18)
        self.output.pack(fill="both", expand=True, padx=12, pady=(0,12))
    
    # Funktion zur Prüfung der Transport-ID
    def pruefe_transport(self):
        transportid = self.entry.get().strip()
        if not transportid:
            messagebox.showerror("Fehler", "Bitte eine Transport-ID eingeben!")
            return