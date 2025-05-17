from vpython import *
from version_1 import version_1
from version_2 import version_2

# Hauptfunktion zum Umschalten der Simulationen
def main():
    scene = canvas(title='Solar System Simulation')
    
    # Standardmäßig Version 1 laden
    version1.version_1()

    # Button erstellen, um zur Version 2 zu wechseln
    def switch_to_version_2():
        scene.clear()  # Alle bisherigen Objekte löschen
        version2.version_2()

    button(text="Wechsel zu Version 2", bind=switch_to_version_2, pos=scene.title_anchor)

# Main starten
main()