# ##############################################################################################################
# Hauptprogramm: CoolChainProjekt
#  Datei: Hauptprogramm_V5.py
#
# Version: 5 vom: 04.05.2026
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
import customtkinter as ctk
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

DEFAULT_VISUAL_CROSSING_API_KEY = "6S444QCZ2WRAWJHLAUR7SX3WE"

class TransportGUI:

    '''
    @brief Kapselt die komplette grafische Benutzeroberfläche des Programms.
    @details
    Diese Klasse steuert die Benutzerseite des Projekts.
    Sie sorgt also dafür, dass ein Anwender eine Transport-ID eingeben,
    die Prüfung starten und die Ergebnisse verständlich lesen kann.

    Was diese Klasse grob übernimmt:
    - Aufbau aller sichtbaren GUI-Elemente
    - Entgegennahme von Benutzereingaben
    - Start der Datenbankabfragen
    - Übergabe der geladenen Daten an die Verarbeitungslogik
    - Anzeige der gefundenen Meldungen im Textfeld

    Warum das wichtig ist:
    - Das Fachprogramm soll laut Aufgabenstellung einfach nutzbar sein.
    - Deshalb trennt die Klasse die Bedienoberfläche von der eigentlichen
      Datenverarbeitung.
    '''
    
    def __init__(self, root):

        '''
        @brief Baut die grafische Oberfläche des Programms auf.
        @details
        In dieser Methode wird das komplette Fenster vorbereitet.

        Was an dieser Stelle passiert:
        - Das Hauptfenster bekommt Titel, Größe und Verhalten.
        - Danach werden nacheinander alle sichtbaren GUI-Elemente erzeugt:
          Eingabefeld, Buttons, API-Key-Feld, Haken für Standard-API-Key,
          Ausgabefeld, Ladebalken (Progressbar) und Statuszeile.
        - Die Widgets werden direkt mit ihren Funktionen verbunden,
          zum Beispiel der Button *Prüfen* mit der Methode *on_pruefen()*.

        Wie das Programm das grob handhabt:
        - Die GUI wird einmal beim Programmstart aufgebaut.
        - Danach wartet sie auf Benutzereingaben.
        - Erst wenn ein Button gedrückt wird, beginnt die eigentliche Arbeit
          mit Datenbankzugriff und Auswertung.

        Warum das gebraucht wird:
        - Diese Methode schafft die Arbeitsoberfläche, über die der Anwender
          das gesamte Prüfprogramm bedient.

        @param root Hauptfenster der Tkinter-Anwendung.
        '''

        self.root = root
        self.root.title("CoolChain - Transportprüfung")
        self.root.geometry("900x620")
        self.root.resizable(True, True)

        ctk.CTkLabel(root, text="CoolChain Transportprüfung", font=("Arial", 14, "bold")).pack(pady=(10, 5))

        frame_top = ctk.CTkFrame(root, fg_color="transparent")
        frame_top.pack(fill="x", padx=12)

        ctk.CTkLabel(frame_top, text="Transport-ID:").pack(side="left")
        self.entry = ctk.CTkEntry(frame_top, width=176)
        self.entry.pack(side="left", padx=(6, 8))

        self.check_btn = ctk.CTkButton(frame_top, text="Prüfen", command=self.on_pruefen)
        self.check_btn.pack(side="left")

        self.clear_btn = ctk.CTkButton(frame_top, text="Löschen", command=self.on_clear, fg_color="gray", hover_color="darkgray")
        self.clear_btn.pack(side="left", padx=6)

        self.all_btn = ctk.CTkButton(frame_top, text="Alle prüfen", command=self.on_alle_pruefen)
        self.all_btn.pack(side="left", padx=6)

        frame_api = ctk.CTkFrame(root, fg_color="transparent")
        frame_api.pack(fill="x", padx=12, pady=(8, 0))

        ctk.CTkLabel(frame_api, text="Visual-Crossing-API-Key:").pack(side="left")

        self.api_entry = ctk.CTkEntry(frame_api, width=40, show="*")
        self.api_entry.pack(side="left", padx=(6, 8), fill="x", expand=True)
        self.api_entry.insert(0, DEFAULT_VISUAL_CROSSING_API_KEY)

        self.use_default_api_key = tk.BooleanVar()
        self.use_default_api_key.set(True)

        self.default_api_check = ctk.CTkCheckBox(
            frame_api,
            text="Standard API-Key verwenden",
            variable=self.use_default_api_key,
            command=self.on_toggle_api_key_mode
        )
        self.default_api_check.pack(side="left", padx=(4, 0))

        ctk.CTkLabel(root, text="Meldungen:").pack(anchor="w", padx=12, pady=(10, 0))
        self.output = ctk.CTkTextbox(root, wrap="word", height=24)
        self.output.pack(fill="both", expand=True, padx=12, pady=(0, 12))

        # Farben für Ausgaben definieren
        self.output.tag_config("gruen", foreground="green")
        self.output.tag_config("rot", foreground="red")

        # Ladebalken
        self.progressbar = ctk.CTkProgressBar(root, mode="determinate")
        self.progressbar.pack(fill="x", padx=15, pady=(0, 10))
        self.progressbar.set(0) # Setzt den Balken am Anfang auf 0

        self.status = tk.StringVar()
        self.status.set("Bereit")
        ctk.CTkLabel(root, textvariable=self.status, anchor="w").pack(fill="x", padx=12, pady=(0, 6))

        self.on_toggle_api_key_mode()

    def on_toggle_api_key_mode(self):

        '''
        @brief Schaltet zwischen Standard-API-Key und manuell eingegebenem API-Key um.
        @details
        Diese Methode reagiert auf den Haken in der Oberfläche.

        Was an dieser Stelle passiert:
        - Ist der Haken gesetzt, wird automatisch der Standard-API-Key verwendet.
        - Gleichzeitig wird das Eingabefeld für den API-Key gesperrt,
          damit klar ist, dass der Standardwert aktiv ist.
        - Ist der Haken nicht gesetzt, wird das Eingabefeld wieder freigegeben,
          damit der Benutzer einen eigenen API-Key eintragen kann.

        Warum das gebraucht wird:
        - Der Anwender soll schnell mit einem vordefinierten API-Key arbeiten können.
        - Gleichzeitig bleibt die Möglichkeit erhalten, bei Bedarf einen
          individuellen API-Key einzutragen.
        '''

        if self.use_default_api_key.get():
            self.api_entry.configure(state="normal")
            self.api_entry.delete(0, tk.END)
            self.api_entry.insert(0, DEFAULT_VISUAL_CROSSING_API_KEY)
            self.api_entry.configure(state="disabled")
        else:
            self.api_entry.configure(state="normal")
            self.api_entry.delete(0, tk.END)

    def get_aktuellen_api_key(self):

        '''
        @brief Liefert den aktuell zu verwendenden API-Key zurück.
        @details
        Diese Methode entscheidet zentral, welcher API-Key tatsächlich an die
        Verarbeitungslogik übergeben wird.

        Was an dieser Stelle passiert:
        - Wenn der Haken gesetzt ist, wird immer der Standard-API-Key zurückgegeben.
        - Wenn der Haken nicht gesetzt ist, wird der Text aus dem Eingabefeld gelesen.

        Warum das gebraucht wird:
        - Dadurch muss die Unterscheidung zwischen Standardwert und Benutzereingabe
          nicht mehrfach im Programm wiederholt werden.
        - Die Methoden *on_pruefen()* und *on_alle_pruefen()* können einfach
          denselben Helfer benutzen.

        @return API-Key als String.
        '''

        if self.use_default_api_key.get():
            return DEFAULT_VISUAL_CROSSING_API_KEY
        return self.api_entry.get().strip()

    def ausgabe_meldung_einfuegen(self, text):

        '''
        @brief Fügt eine Meldung farblich formatiert in das Ausgabefeld ein.
        @details
        - Nur das Wort "korrekt" wird grün dargestellt.
        - Bei Fehlermeldungen bleiben Transport-ID, Pfeil und andere Bestandteile weiss.
        - Nur der eigentliche Meldungstext hinter dem Pfeil wird rot dargestellt.
        '''

        if " -> " in text:
            prefix, meldung = text.split(" -> ", 1)
            self.output.insert(tk.END, prefix + " -> ")

            if meldung.strip().lower() == "korrekt":
                self.output.insert(tk.END, meldung, "gruen")
            else:
                self.output.insert(tk.END, meldung, "rot")
        else:
            if text.strip().lower() == "korrekt":
                self.output.insert(tk.END, text, "gruen")
            else:
                self.output.insert(tk.END, text)

    def on_pruefen(self):

        '''
        @brief Prüft genau einen Transport anhand der eingegebenen Transport-ID.
        @details
        Diese Methode ist der zentrale Ablauf für die Einzelprüfung.

        Was an dieser Stelle passiert:
        - Zuerst wird die Eingabe aus dem Feld gelesen, auf Zeichenmenge/ Ziffern geprüft und von Leerzeichen bereinigt.
        - Zusätzlich wird der aktuell gültige API-Key ermittelt.
        - Wenn keine Transport-ID eingegeben wurde, bricht die Methode sofort
          mit einer Fehlermeldung ab.
        - Danach lädt das Programm nacheinander:
          1. die Bewegungsdaten,
          2. die Temperaturdaten,
          3. die Firmendaten,
          4. die Stationsdaten.
        - Diese Daten werden anschließend an *verarbeite_transport()* übergeben.
        - Die Rückgabemeldungen werden dann Zeile für Zeile im Ausgabefeld angezeigt.

        Wie das Programm das grob handhabt:
        - Das Hauptprogramm selbst prüft die Kühlkette nicht fachlich.
        - Es sammelt nur alle benötigten Daten ein und reicht sie an die
          Verarbeitungsfunktion weiter.
        - Danach übernimmt es wieder die Ausgabe an den Benutzer.

        Warum das gebraucht wird:
        - Diese Methode bildet die normale Alltagsnutzung des Programms ab:
          Benutzer gibt eine ID ein, Programm wertet sie aus, Ergebnis wird angezeigt.

        @return Kein Rückgabewert. Die Ergebnisse werden direkt in der GUI angezeigt.
        '''

        transportid = self.entry.get().strip()
        api_key = self.get_aktuellen_api_key()

        if not transportid.isdigit() or len(transportid) != 23:
            messagebox.showwarning("Fehler", "Die Transport-ID muss aus exakt 23 Ziffern bestehen!")
            return

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
            self.output.insert(tk.END, f"Transport-ID: {transportid}\n", "standard")
            self.output.insert(tk.END, "--------------------------------------------------\n", "standard")

            for m in meldungen:
                self.ausgabe_meldung_einfuegen(f" -> {m}\n")

            self.status.set("Prüfung abgeschlossen")

        except Exception as e:
            messagebox.showerror("Fehler", f"Ein Fehler ist aufgetreten:\n{e}")

    def on_alle_pruefen(self):

        '''
        @brief Führt dieselbe Prüfung nacheinander für alle vorhandenen Transport-IDs durch.
        @details
        Diese Methode ist die Sammelprüfung des Programms.

        Was an dieser Stelle passiert:
        - Zuerst wird der aktuell gültige API-Key gelesen und der Ladebalken zurückgesetzt..
        - Danach holt das Programm mit *get_alle_transport_ids()* eine Liste
          aller bekannten Transporte aus der Datenbank.
        - Anschließend läuft eine for-Schleife über jede einzelne ID.
        - Während der Schleife: Der Ladebalken (Progressbar) wird kontinuierlich aktualisiert, 
          damit der Anwender den Fortschritt sieht. Gleichzeitig wird für die Statistik mitgezählt.
        - Für jede ID werden wieder alle benötigten Daten geladen und an
          *verarbeite_transport()* übergeben.
        - Die gefundenen Meldungen werden gesammelt und am Ende sortiert ausgegeben.
        - Zum Schluss wird eine Statistik (Anzahl Korrekt/Fehlerhaft) angehängt.

        Wie das Programm das grob handhabt:
        - Die Methode benutzt für alle Transporte denselben Prüfablauf wie bei
          der Einzelprüfung.
        - Der Unterschied ist nur, dass dieser Ablauf automatisiert in einer Schleife
          für jede Transport-ID wiederholt wird.
        - Dadurch eignet sich die Funktion gut für einen Gesamtüberblick
          über alle Datensätze in der Datenbank.

        Warum das gebraucht wird:
        - Der Anwender soll nicht jede Transport-ID einzeln per Hand prüfen müssen.
        - Diese Methode ermöglicht eine vollständige Gesamtprüfung der Datenbank.
        - Die zusätzliche Statistik und der Ladebalken verbessern die Benutzerfreundlichkeit.

        @return Kein Rückgabewert. Die Ergebnisse werden gesammelt in der GUI ausgegeben.
        '''

        api_key = self.get_aktuellen_api_key()

        try:
            self.status.set("Bitte warten, alle Transporte werden geprüft ...")
            self.root.update_idletasks()
            self.progressbar.set(0)

            alle_ids = get_alle_transport_ids(verbindungs_i)
            ergebnisse = []

            # Zähler für die Statistik
            anzahl_korrekt = 0
            anzahl_fehlerhaft = 0
            total_ids = len(alle_ids)

            for index, tid in enumerate(alle_ids):
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

                hat_fehler = False
                for m in meldungen:
                    ergebnisse.append((tid, m))
                    if m.strip().lower() != "korrekt":
                        hat_fehler = True

                # Zähler für Fehler erhöhen
                if hat_fehler:
                    anzahl_fehlerhaft += 1
                else:
                    anzahl_korrekt += 1

                # Ladebalken aktualisieren (Aktueller Schritt geteilt durch Gesamtanzahl)
                self.progressbar.set((index + 1) / total_ids)
                self.root.update_idletasks()

            ergebnisse.sort(key=lambda x: (x[1], x[0]))

            self.output.delete("1.0", tk.END)
            self.output.insert(tk.END, "Alle Transport-IDs - Prüfungen\n")
            self.output.insert(tk.END, "==================================================\n")

            for tid, m in ergebnisse:
                self.ausgabe_meldung_einfuegen(f"{tid} -> {m}\n")

            #Statistik am Ende
            self.output.insert(tk.END, "\n==================================================\n")
            self.output.insert(tk.END, f"Zusammenfassung: {total_ids} Transporte geprüft\n")
            self.output.insert(tk.END, f"Korrekt: {anzahl_korrekt}\n", "gruen")
            self.output.insert(tk.END, f"Fehlerhaft: {anzahl_fehlerhaft}\n", "rot")

            self.status.set(f"{len(alle_ids)} Transporte geprüft")

        except Exception as e:
            messagebox.showerror("Fehler", f"Ein Fehler ist aufgetreten:\n{e}")

    def on_clear(self):
        
        '''
        @brief Setzt die Benutzereingabe und die Anzeige wieder auf den Ausgangszustand zurück.
        @details
        Diese Methode ist die Reset-Funktion der Oberfläche.

        Was an dieser Stelle passiert:
        - Das Eingabefeld für die Transport-ID wird geleert.
        - Das Ausgabefeld mit den bisherigen Meldungen wird gelöscht.
        - Der Haken für den Standard-API-Key wird wieder gesetzt.
        - Das API-Feld wird wieder mit dem Standardwert belegt und gesperrt.
        - Die Statuszeile wird wieder auf *Bereit* gesetzt.

        Warum das gebraucht wird:
        - Der Anwender kann damit schnell einen neuen Prüfvorgang starten,
          ohne alte Inhalte manuell entfernen zu müssen.

        @return Kein Rückgabewert. Die GUI wird direkt zurückgesetzt.
        '''

        self.entry.delete(0, tk.END)
        self.output.delete("1.0", tk.END)
        self.use_default_api_key.set(True)
        self.on_toggle_api_key_mode()
        self.progressbar.set(0)
        self.status.set("Bereit")

if __name__ == "__main__":
    
    # CustomTkinter Design-Einstellungen
    ctk.set_appearance_mode("System")  
    ctk.set_default_color_theme("blue") 
    
    # root wird nun mit CTk() erstellt
    root = ctk.CTk()
    app = TransportGUI(root)
    root.mainloop()