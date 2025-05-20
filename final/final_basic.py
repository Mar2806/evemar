from vpython import *
import math
import os

def version_1():

    scene_width = 2300
    scene_height = 1300

    scene = canvas(title='3D Solar System with Textured Planets',
                    width=scene_width, height=scene_height,
                    center=vector(0, 0, 0),
                    background=color.black,
                    ambient=vector(0, 0, 0),
                    autoscale=False)

    scene.lights = []

    # Sonne
    sun = sphere(pos=vector(0, 0, 0), radius=2, color=vector(1, 1, 0), emissive=True)
    sun_light = local_light(pos=sun.pos, color=color.white)

    # Planet data with image file names
    planets_data = [
        {'name': 'Mercury', 'radius': 0.5, 'orbital_radius': 5, 'orbital_period': 0.88, 'texture': 'final/textures/mercury.jpg', 'real_radius_km': 2439.7, 'real_orbital_radius_mio_km': 57.91, 'color': color.gray(0.7)},
        {'name': 'Venus', 'radius': 0.8, 'orbital_radius': 8, 'orbital_period': 2.25, 'texture': 'final/textures/venus.jpg', 'real_radius_km': 6051.8, 'real_orbital_radius_mio_km': 108.2, 'color': vector(1, 0.7, 0)},
        {'name': 'Earth', 'radius': 1.0, 'orbital_radius': 12, 'orbital_period': 3.0, 'texture': 'final/textures/earth.jpg', 'real_radius_km': 6371, 'real_orbital_radius_mio_km': 149.6, 'color': color.blue},
        {'name': 'Mars', 'radius': 0.6, 'orbital_radius': 16, 'orbital_period': 4.88, 'texture': 'final/textures/mars.jpg', 'real_radius_km': 3389.5, 'real_orbital_radius_mio_km': 227.9, 'color': color.red},
        {'name': 'Jupiter', 'radius': 1.8, 'orbital_radius': 25, 'orbital_period': 12.0, 'texture': 'final/textures/jupyter.jpg', 'real_radius_km': 69911, 'real_orbital_radius_mio_km': 778.5, 'color': vector(1, 0.8, 0.6)},
        {'name': 'Saturn', 'radius': 1.6, 'orbital_radius': 35, 'orbital_period': 29.5, 'texture': 'final/textures/saturn.jpg', 'real_radius_km': 58232, 'real_orbital_radius_mio_km': 1434, 'color': color.yellow},
        {'name': 'Uranus', 'radius': 1.2, 'orbital_radius': 48, 'orbital_period': 84.0, 'texture': 'final/textures/uranus.jpg', 'real_radius_km': 25362, 'real_orbital_radius_mio_km': 2871, 'color': color.cyan},
        {'name': 'Neptune', 'radius': 1.1, 'orbital_radius': 60, 'orbital_period': 165.0, 'texture': 'final/textures/neptune.jpg', 'real_radius_km': 24622, 'real_orbital_radius_mio_km': 4495, 'color': color.blue},
    ]

    # Orbit-Kreise
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
        try:
            # Load the texture.  Make sure the file exists!
            planet = sphere(
                pos=vector(data['orbital_radius'], 0, 0),  # Initial position along x-axis
                radius=data['radius'],  # Planet size
                texture=data['texture'],  # Apply texture instead of solid color
                make_trail=False  # Leave a trail to show the orbit path
            )
            planet.name = data['name']
            planets.append(planet)
            angles[i] = 0  # Initialize its orbital angle to 0
        except Exception as e:
            print(f"Error loading texture for {data['name']}: {e}")
            # If the texture fails to load, create the planet without a texture.
            planet = sphere(pos=vector(data['orbital_radius'], 0, 0),
                            radius=data['radius'],
                            color=data['color'],  # Keep the color, was missing in the previous version
                            make_trail=False,
                            shininess=0)
            planet.name = data['name']
            planets.append(planet)
            angles[i] = 0

    # Info-Label
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

    selected_planet_index = None

    time_speed = 50
    paused = False

    def slider_callback(s):
        nonlocal time_speed
        time_speed = s.value

    def handle_keydown(evt):
        nonlocal paused
        if evt.key == ' ':
            paused = not paused

    scene.append_to_caption('\n\nSimulation Speed: ')
    speed_slider = slider(min=0, max=100, value=time_speed, length=300, bind=slider_callback)
    scene.append_to_caption('\n\nPause/Start = Leertaste\n\n')

    scene.bind('keydown', handle_keydown)

    def planet_clicked(evt):
        nonlocal selected_planet_index
        clicked = scene.mouse.pick
        if clicked and hasattr(clicked, 'name'):
            for i, planet in enumerate(planets):
                if planet == clicked:
                    selected_planet_index = i
                    data = planets_data[i]
                    info_label.text = (
                        f"Name: {data['name']}\n"
                        f"Radius: {data['real_radius_km']} km\n"
                        f"Umlaufzeit: {data['orbital_period']} Jahre\n"
                        f"Abstand zur Sonne: {data['real_orbital_radius_mio_km']} Mio. km"
                    )
                    info_label.visible = True
                    return
        # Wenn außerhalb geklickt wird, Info ausblenden
        selected_planet_index = None
        info_label.visible = False

    scene.bind('mousedown', planet_clicked)

    while True:
        rate(max(10, time_speed))

        if not paused:
            sun_light.pos = sun.pos

            for i, planet in enumerate(planets):
                data = planets_data[i]
                angular_velocity = 2 * math.pi / (data['orbital_period'] * 100)
                angles[i] += angular_velocity
                x = data['orbital_radius'] * math.cos(angles[i])
                z = data['orbital_radius'] * math.sin(angles[i])
                planet.pos = vector(x, 0, z)

        # Info-Label aktualisieren, wenn ein Planet ausgewählt ist
        if selected_planet_index is not None:
            selected_planet = planets[selected_planet_index]
            info_label.pos = selected_planet.pos + vector(0, selected_planet.radius + 2, 0)
