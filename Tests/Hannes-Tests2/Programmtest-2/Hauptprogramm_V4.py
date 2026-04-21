# ##############################################################################################################
# Hauptprogramm: CoolChainProjekt
#  Datei: Hauptprogramm_V4.py
#
# Version: 4 vom: 21.04.2026
# Autoren: Josie Woeste, Hannes Ruhe, Kai Meiners
#
# Zugehörige Libarys:
# - DB_Zugriff_Libary_V4.py
# - Verarbeitung_Libary_V4.py
# 
# Funktionsbeschreibung: 
# Hauptprogramm & Benutzeroberfläche zur Eingabe der Transport-ID und Anzeige der Ergebnisse
# ##############################################################################################################

import tkinter as tk
from tkinter import messagebox, scrolledtext

from DB_Zugriff_Libary_V4 import (
    get_transport_daten,
    get_temperatur_daten,
    get_company_daten,
    get_transportstation_daten,
    get_alle_transport_ids,
)
from Verarbeitung_Libary_V4 import verarbeite_transport

server = 'sc-db-server1.database.windows.net'
database = 'supplychain'
username = 'rse'
password = 'Pa$$w0rd'

verbindungs_i = (
    f"DRIVER={{ODBC Driver 18 for SQL Server}};"
    f"SERVER={server};"
    f"DATABASE={database};"
    f"UID={username};"
    f"PWD={password};"
    f"Encrypt=yes;"
    f"TrustServerCertificate=no;"
    f"Connection Timeout=30;"
)

DEFAULT_VISUAL_CROSSING_API_KEY = ""

class TransportGUI:

    def __init__(self, root):
        '''
        @brief Die Hauptklasse für die grafische Benutzeroberfläche (GUI).
        @details Initialisiert das Hauptfenster, die Widgets für die Eingabe,
        die Steuerung (Buttons) und die Ausgabe der Ergebnisse.
        '''

        self.root = root
        self.root.title("CoolChain - Transportprüfung")
        self.root.geometry("900x620")
        self.root.resizable(True, True)

        tk.Label(root, text="CoolChain Transportprüfung", font=("Arial", 14, "bold")).pack(pady=(10, 5))

        frame_top = tk.Frame(root)
        frame_top.pack(fill="x", padx=12)

        tk.Label(frame_top, text="Transport-ID:").pack(side="left")
        self.entry = tk.Entry(frame_top, width=36)
        self.entry.pack(side="left", padx=(6, 8))

        self.check_btn = tk.Button(frame_top, text="Prüfen", command=self.on_pruefen)
        self.check_btn.pack(side="left")

        self.clear_btn = tk.Button(frame_top, text="Löschen", command=self.on_clear)
        self.clear_btn.pack(side="left", padx=6)

        self.all_btn = tk.Button(frame_top, text="Alle prüfen", command=self.on_alle_pruefen)
        self.all_btn.pack(side="left", padx=6)

        frame_api = tk.Frame(root)
        frame_api.pack(fill="x", padx=12, pady=(8, 0))

        tk.Label(frame_api, text="Visual-Crossing-API-Key:").pack(side="left")
        self.api_entry = tk.Entry(frame_api, width=55, show="*")
        self.api_entry.pack(side="left", padx=(6, 8), fill="x", expand=True)
        self.api_entry.insert(0, DEFAULT_VISUAL_CROSSING_API_KEY)

        tk.Label(root, text="Meldungen:").pack(anchor="w", padx=12, pady=(10, 0))
        self.output = scrolledtext.ScrolledText(root, wrap="word", height=24)
        self.output.pack(fill="both", expand=True, padx=12, pady=(0, 12))

        self.status = tk.StringVar()
        self.status.set("Bereit")
        tk.Label(root, textvariable=self.status, anchor="w").pack(fill="x", padx=12, pady=(0, 6))

    def on_pruefen(self):
        '''
        @brief Führt die Prüfung eines einzelnen Transports basierend auf der eingegebenen ID durch.
        @details Liest die Transport-ID aus dem Eingabefeld, ruft alle notwendigen Daten aus der Datenbank ab
        und übergibt diese zur Verarbeitung.
        '''

        transportid = self.entry.get().strip()
        api_key = self.api_entry.get().strip()

        if not transportid:
            messagebox.showerror("Fehler", "Bitte eine Transport-ID eingeben!")
            return

        try:
            self.status.set("Prüfe Transport-ID...")
            self.root.update_idletasks()

            transport_daten, _ = get_transport_daten(transportid, verbindungs_i)
            temperatur_daten, _ = get_temperatur_daten(transport_daten, verbindungs_i)
            company_daten, _ = get_company_daten(transport_daten, verbindungs_i)
            transportstation_daten, _ = get_transportstation_daten(transport_daten, verbindungs_i)

            meldungen = verarbeite_transport(
                transport_daten,
                temperatur_daten,
                company_daten,
                transportstation_daten,
                api_key,
            )

            self.output.delete("1.0", tk.END)
            self.output.insert(tk.END, f"Transport-ID: {transportid}\n")
            self.output.insert(tk.END, "--------------------------------------------------\n")
            for m in meldungen:
                self.output.insert(tk.END, f" -> {m}\n")

            self.status.set("Prüfung abgeschlossen")

        except Exception as e:
            messagebox.showerror("Fehler", f"Ein Fehler ist aufgetreten:\n{e}")

    def on_alle_pruefen(self):
        '''
        @brief Führt die Prüfung aller in der Datenbank vorhandenen Transporte durch.
        @details Ruft zunächst alle eindeutigen Transport-IDs ab, verarbeitet jede ID und zeigt die Ergebnisse an.
        '''

        api_key = self.api_entry.get().strip()

        try:
            self.status.set("Bitte warten, alle Transporte werden geprüft ...")
            self.root.update_idletasks()

            alle_ids = get_alle_transport_ids(verbindungs_i)
            ergebnisse = []

            for tid in alle_ids:
                transport_daten, _ = get_transport_daten(tid, verbindungs_i)
                temperatur_daten, _ = get_temperatur_daten(transport_daten, verbindungs_i)
                company_daten, _ = get_company_daten(transport_daten, verbindungs_i)
                transportstation_daten, _ = get_transportstation_daten(transport_daten, verbindungs_i)

                meldungen = verarbeite_transport(
                    transport_daten,
                    temperatur_daten,
                    company_daten,
                    transportstation_daten,
                    api_key,
                )

                for m in meldungen:
                    ergebnisse.append((tid, m))

            ergebnisse.sort(key=lambda x: (x[1], x[0]))

            self.output.delete("1.0", tk.END)
            self.output.insert(tk.END, "Alle Transport-IDs - Prüfungen\n")
            self.output.insert(tk.END, "==================================================\n")

            for tid, m in ergebnisse:
                self.output.insert(tk.END, f"{tid} -> {m}\n")

            self.status.set(f"{len(alle_ids)} Transporte geprüft")

        except Exception as e:
            messagebox.showerror("Fehler", f"Ein Fehler ist aufgetreten:\n{e}")

    def on_clear(self):
        '''
        @brief Löscht die Eingabe im Transport-ID-Feld und leert das Ausgabefeld.
        @details Setzt den Status auf "Bereit" zurück.
        '''

        self.entry.delete(0, tk.END)
        self.output.delete("1.0", tk.END)
        self.status.set("Bereit")

if __name__ == "__main__":
    root = tk.Tk()
    app = TransportGUI(root)
    root.mainloop()
