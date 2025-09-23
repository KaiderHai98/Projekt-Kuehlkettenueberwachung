###############################################################################################################
## Hauptprogramm: CoolChainProjekt
#  Datei: Joe_GUI_V1.py
#
# Version: 3 vom: 2.09.2025
# Autoren:
#
# Zugehörige Libarys:
# - DB_Zugriff_Libary_V3.py
# - Verarbeitung_Libary_V3.py
# 
# Funktionsbeschreibung: 
# Benutzeroberfläche zur Eingabe der Transport-ID und Anzeige der Ergebnisse
###############################################################################################################

import tkinter as tk
from tkinter import messagebox
from Hauptprogramm_V3 import hole_transport_meldungen


class TransportGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("CoolChain Transportprüfung")
        self.root.geometry("600x400")

        # Eingabe-Feld für Transport-ID
        self.label = tk.Label(root, text="Transport-ID eingeben:")
        self.label.pack(pady=10)

        self.entry = tk.Entry(root, width=40)
        self.entry.pack(pady=5)

        # Button zum Starten
        self.button = tk.Button(root, text="Prüfen", command=self.pruefe_transport)
        self.button.pack(pady=10)

        # Textfeld für Ausgaben
        self.output = tk.Text(root, wrap="word", width=70, height=15)
        self.output.pack(pady=10)