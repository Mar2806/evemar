
from vpython import *
import math

def version_1():
    scene_width = 2300
    scene_height = 1300

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

    # Planeten-Daten mit Einheiten (Werte ca.)
    planets_data = [
        {'name': 'Mercury', 'radius': 0.5, 'color': vector(0.5, 0.5, 0.5), 'orbital_radius': 5, 'orbital_period': 0.88, 'real_radius_km': 2439, 'real_orbital_radius_mio_km': 58},
        {'name': 'Venus',   'radius': 0.8, 'color': vector(1, 0.65, 0),    'orbital_radius': 8, 'orbital_period': 2.25, 'real_radius_km': 6051, 'real_orbital_radius_mio_km': 108},
        {'name': 'Earth',   'radius': 1.0, 'color': vector(0, 0, 1),       'orbital_radius': 12,'orbital_period': 3.0,  'real_radius_km': 6371, 'real_orbital_radius_mio_km': 150},
        {'name': 'Mars',    'radius': 0.6, 'color': vector(1, 0, 0),       'orbital_radius': 16,'orbital_period': 4.88, 'real_radius_km': 3389, 'real_orbital_radius_mio_km': 228},
        {'name': 'Jupiter', 'radius': 1.8, 'color': vector(0, 1, 1),       'orbital_radius': 25,'orbital_period': 12.0, 'real_radius_km': 69911,'real_orbital_radius_mio_km': 778},
        {'name': 'Saturn',  'radius': 1.6, 'color': vector(1, 1, 0.6),     'orbital_radius': 35,'orbital_period': 29.5, 'real_radius_km': 58232,'real_orbital_radius_mio_km': 1430},
        {'name': 'Uranus',  'radius': 1.2, 'color': vector(0, 1, 0),       'orbital_radius': 48,'orbital_period': 84.0, 'real_radius_km': 25362,'real_orbital_radius_mio_km': 2870},
        {'name': 'Neptune', 'radius': 1.1, 'color': vector(0.2, 0.2, 1),   'orbital_radius': 60,'orbital_period': 165.0,'real_radius_km': 24622,'real_orbital_radius_mio_km': 4500}
    ]

    # Orbit-Kreise anzeigen
    for data in planets_data:
        ring(pos=vector(0, 0, 0),
             axis=vector(0, 1, 0),
             radius=data['orbital_radius'],
             thickness=0.1,
             color=color.gray(0.3),
             opacity=0.5)

    # Planeten erstellen
    planets = []
    angles = [0] * len(planets_data)

    for i, data in enumerate(planets_data):
        planet = sphere(pos=vector(data['orbital_radius'], 0, 0),
                        radius=data['radius'],
                        color=data['color'],
                        make_trail=False,
                        shininess=0)
        planet.name = data['name']
        planets.append(planet)

    # Info-Label (unsichtbar starten)
    info_label = label(pos=vector(0, 0, 0),
                       text='',
                       xoffset=30, yoffset=30,
                       height=16,
                       border=6,
                       font='sans',
                       box=True,
                       opacity=0.8,
                       visible=False,
                       color=color.white,
                       background=color.gray(0.2))

    # Steuerung
    time_speed = 50
    paused = False

    def slider_callback(s):
        nonlocal time_speed, paused
        time_speed = s.value
        paused = time_speed < 1

    scene.append_to_caption('\n\nSimulation Speed: ')
    speed_slider = slider(min=0, max=300, value=time_speed, length=300, bind=slider_callback)
    scene.append_to_caption('\n\n')

    def planet_clicked(evt):
        nonlocal paused
        clicked = scene.mouse.pick
        if clicked and hasattr(clicked, 'name'):
            paused = not paused
            for i, planet in enumerate(planets):
                if planet == clicked:
                    data = planets_data[i]
                    info_label.pos = planet.pos + vector(0, planet.radius + 2, 0)
                    info_label.text = (
                        f"Name: {data['name']}\n"
                        f"Radius: {data['real_radius_km']} km\n"
                        f"Umlaufzeit: {data['orbital_period']} Jahre\n"
                        f"Abstand zur Sonne: {data['real_orbital_radius_mio_km']} Mio. km"
                    )
                    info_label.visible = True
                    break
        else:
            info_label.visible = False

    scene.bind('mousedown', planet_clicked)

    # Hauptschleife
    while True:
        rate(max(1, time_speed))
        if paused:
            continue

        sun_light.pos = sun.pos

        for i, planet in enumerate(planets):
            data = planets_data[i]
            angular_velocity = 2 * math.pi / (data['orbital_period'] * 100)
            angles[i] += angular_velocity
            x = data['orbital_radius'] * math.cos(angles[i])
            z = data['orbital_radius'] * math.sin(angles[i])
            planet.pos = vector(x, 0, z)

            if info_label.visible and planet.name in info_label.text:
                info_label.pos = planet.pos + vector(0, planet.radius + 2, 0)

# Starte die Simulation
version_1()