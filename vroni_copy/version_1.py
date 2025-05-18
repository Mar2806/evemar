from vpython import *
import math

def version_1():
    scene_width = 2300
    scene_height = 1300

    # Szene erstellen
    scene = canvas(title='Simple 3D Solar System',
                   width=scene_width, height=scene_height,
                   center=vector(0, 0, 0),
                   background=color.black,
                   ambient=vector(0, 0, 0),
                   autoscale=False)

    scene.lights = []

    # Sonne
    sun = sphere(pos=vector(0, 0, 0), radius=2, color=vector(1, 1, 0), emissive=True)
    sun_light = local_light(pos=sun.pos, color=color.white)

    # Planeten-Daten
    planets_data = [
        {'name': 'Mercury', 'radius': 0.5, 'color': vector(0.5, 0.5, 0.5), 'orbital_radius': 5, 'orbital_period': 0.88},
        {'name': 'Venus', 'radius': 0.8, 'color': vector(1, 0.65, 0), 'orbital_radius': 8, 'orbital_period': 2.25},
        {'name': 'Earth', 'radius': 1, 'color': vector(0, 0, 1), 'orbital_radius': 12, 'orbital_period': 3.0},
        {'name': 'Mars', 'radius': 0.6, 'color': vector(1, 0, 0), 'orbital_radius': 16, 'orbital_period': 4.88},
        {'name': 'Jupiter', 'radius': 1.8, 'color': vector(0, 1, 1), 'orbital_radius': 25, 'orbital_period': 12.0},
        {'name': 'Saturn', 'radius': 1.6, 'color': vector(1, 1, 0.6), 'orbital_radius': 35, 'orbital_period': 29.5},
        {'name': 'Uranus', 'radius': 1.2, 'color': vector(0, 1, 0), 'orbital_radius': 48, 'orbital_period': 84.0},
        {'name': 'Neptune', 'radius': 1.1, 'color': vector(0.2, 0.2, 1), 'orbital_radius': 60, 'orbital_period': 165.0}
    ]

    # Planeten-Objekte erstellen ohne Trails
    planets = []
    angles = [0] * len(planets_data)

    for i, data in enumerate(planets_data):
        planet = sphere(pos=vector(data['orbital_radius'], 0, 0),
                        radius=data['radius'],
                        color=data['color'],
                        make_trail=False,  # Keine Trails
                        shininess=0)
        planet.name = data['name']
        planets.append(planet)

    # Steuer-Variablen lokal
    time_speed = 50
    paused = False

    # Slider-Callback mit Zugriff auf äußere Variablen
    def slider_callback(s):
        nonlocal time_speed, paused
        time_speed = s.value
        paused = time_speed < 1  # Pause, wenn Geschwindigkeit 0 ist

    # UI-Elemente
    scene.append_to_caption('\n\nSimulation Speed: ')
    speed_slider = slider(min=0, max=300, value=time_speed, length=300, bind=slider_callback)
    scene.append_to_caption('\n\n')

    # Planeten-Klick pausiert Simulation
    def planet_clicked(evt):
        nonlocal paused
        clicked = scene.mouse.pick
        if clicked and hasattr(clicked, 'name'):
            print(f"Clicked on: {clicked.name}")
            paused = True
        else:
            print("Nichts erkannt oder kein Planet.")

    scene.bind('mousedown', planet_clicked)

    # Haupt-Simulationsschleife
    while True:
        rate(max(1, time_speed))

        if paused:
            continue

        sun_light.pos = sun.pos

        for i, planet in enumerate(planets):
            data = planets_data[i]
            angular_velocity = 2 * math.pi / (data['orbital_period'] * 100)  # Geschwindigkeit pro Zeiteinheit
            angles[i] += angular_velocity
            x = data['orbital_radius'] * math.cos(angles[i])
            z = data['orbital_radius'] * math.sin(angles[i])
            planet.pos = vector(x, 0, z)
