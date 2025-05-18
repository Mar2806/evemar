import tkinter as tk
from version_1 import version_1
from version_2 import version_2
import threading

# Funktion zum Starten der Version 1
def start_version_1():
    root.destroy()  # Menü schließen
    version_1()     # Deine bestehende Funktion wird gestartet

# Funktion zum Starten der Version 2
def start_version_2():
    root.destroy()
    version_2()

# Menüfenster mit Buttons
root = tk.Tk()
root.title("Simulation auswählen")

label = tk.Label(root, text="Welche Version möchtest du starten?", font=("Arial", 14))
label.pack(pady=20)

btn1 = tk.Button(root, text="Version 1 starten", width=25, height=2, command=start_version_1)
btn1.pack(pady=10)

btn2 = tk.Button(root, text="Version 2 starten", width=25, height=2, command=start_version_2)
btn2.pack(pady=10)

root.mainloop()