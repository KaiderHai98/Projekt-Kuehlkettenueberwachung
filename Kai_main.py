import tkinter as tk
from tkinter import messagebox
from db import fetch_transport_data
from checks import check_consistency, check_cooling_breaks, check_transport_duration

def run_checks():
    transport_id = entry.get()
    rows = fetch_transport_data(transport_id)

    results = []
    for check in [check_consistency, check_cooling_breaks, check_transport_duration]:
        ok, msg = check(rows)
        results.append(("✅" if ok else "❌") + " " + msg)

    messagebox.showinfo("Ergebnisse", "\n".join(results))

# GUI
root = tk.Tk()
root.title("Kühlketten-Überwachung")
root.geometry("400x200")

label = tk.Label(root, text="Transport-ID eingeben:", font=("Arial", 12))
label.pack(pady=5)

entry = tk.Entry(root, width=40)
entry.pack(pady=5)

button = tk.Button(root, text="Prüfen", command=run_checks, bg="#4CAF50", fg="white")
button.pack(pady=10)

root.mainloop()