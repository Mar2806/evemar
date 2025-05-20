from vpython import *
import math
import random
import tkinter  # Import tkinter for getting screen size
import os

def version_2():
    # Get the screen size using tkinter
    root = tkinter.Tk()
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    root.destroy()  # Destroy the tkinter window after getting the size

    # Calculate scene dimensions, you can adjust the factors as needed
    scene_width = int(screen_width * 0.985 + 20)
    scene_height = int(screen_height * 0.85 + 20)

    # Set up the scene
    scene = canvas(title='3D Solar System ',
                   width=scene_width, height=scene_height,
                   center=vector(0, 0, 0),
                   background=color.black,
                   ambient=vector(0, 0, 0),
                   autoscale=False,
                   title_color=color.black)

    # Keep autospin False if you want to control it yourself or rely on manual mouse rotation.
    scene.autospin = False

    # --- Generate spherical shell of stars around a center ---
    class Star:
        def __init__(self, offset):
            self.offset = offset
            self.obj = sphere(pos=offset, radius=1,
                              color=vector(random.uniform(0.7, 1), random.uniform(0.7, 1), random.uniform(0.7, 1)),
                              emissive=True, shininess=0)

    def generate_star_shell(radius, count):
        stars = []
        for _ in range(count):
            theta = random.uniform(0, 2 * math.pi)
            phi = random.uniform(0, math.pi)
            x = radius * math.sin(phi) * math.cos(theta)
            y = radius * math.sin(phi) * math.sin(theta)
            z = radius * math.cos(phi)
            offset = vector(x, y, z)
            stars.append(Star(offset))
        return stars

    star_radius = 1500
    num_stars = 2000
    stars = generate_star_shell(radius=star_radius, count=num_stars)

    # Disable default lighting
    scene.lights = []

    # Define the Sun
    sun = sphere(pos=vector(0, 0, 0), radius=2, color=vector(1, 1, 0), emissive=True)
    sun_light = local_light(pos=sun.pos, color=color.white)

    # Planet data
    #  Added texture file names to the planet data.
    planets_data = [
        {'name': 'Mercury', 'radius': 0.5, 'orbital_radius': 5, 'orbital_period': 0.88, 'phi_offset': 0,
         'texture': 'final/textures/mercury.jpg', 'real_radius_km': 2439.7, 'real_orbital_radius_mio_km': 57.91},
        {'name': 'Venus', 'radius': 0.8, 'orbital_radius': 8, 'orbital_period': 2.25, 'phi_offset': math.pi / 4,
         'texture': 'final/textures/venus.jpg', 'real_radius_km': 6051.8, 'real_orbital_radius_mio_km': 108.2},
        {'name': 'Earth', 'radius': 1, 'orbital_radius': 12, 'orbital_period': 3.0, 'phi_offset': math.pi / 2,
         'texture': 'final/textures/earth.jpg', 'real_radius_km': 6371, 'real_orbital_radius_mio_km': 149.6},
        {'name': 'Mars', 'radius': 0.6, 'orbital_radius': 16, 'orbital_period': 4.88, 'phi_offset': 3 * math.pi / 4,
         'texture': 'final/textures/mars.jpg', 'real_radius_km': 3389.5, 'real_orbital_radius_mio_km': 227.9},
        {'name': 'Jupiter', 'radius': 1.8, 'orbital_radius': 25, 'orbital_period': 12.0, 'phi_offset': math.pi,
         'texture': 'final/textures/jupyter.jpg', 'real_radius_km': 69911, 'real_orbital_radius_mio_km': 778.5},
        {'name': 'Saturn', 'radius': 1.6, 'orbital_radius': 35, 'orbital_period': 29.5, 'phi_offset': 5 * math.pi / 4,
         'texture': 'final/textures/saturn.jpg', 'real_radius_km': 58232, 'real_orbital_radius_mio_km': 1434},
        {'name': 'Uranus', 'radius': 1.2, 'orbital_radius': 48, 'orbital_period': 84.0, 'phi_offset': 3 * math.pi / 2,
         'texture': 'final/textures/uranus.jpg', 'real_radius_km': 25362, 'real_orbital_radius_mio_km': 2871},
        {'name': 'Neptune', 'radius': 1.1, 'orbital_radius': 60, 'orbital_period': 165.0, 'phi_offset': 7 * math.pi / 4,
         'texture': 'final/textures/neptune.jpg', 'real_radius_km': 24622, 'real_orbital_radius_mio_km': 4495}
    ]

    planets = []
    angles = [0] * len(planets_data)

    # Create planets
    for i, data in enumerate(planets_data):
        try:
            # Load the texture.  Make sure the file exists!
            planet = sphere(
                pos=vector(data['orbital_radius'], 0, 0),
                radius=data['radius'],
                texture=data['texture'],  # Apply the texture
                make_trail=False,
                shininess=0
            )
            planet.name = data['name']
            planets.append(planet)
            angles[i] = 0
        except Exception as e:
            print(f"Error loading texture for {data['name']}: {e}")
            # If the texture fails to load, create the planet without a texture.
            planet = sphere(pos=vector(data['orbital_radius'], 0, 0),
                            radius=data['radius'],
                            color=data['color'],  # Keep the color from the original data
                            make_trail=False,
                            shininess=0)
            planet.name = data['name']
            planets.append(planet)
            angles[i] = 0

    # Simulation parameters
    time_speed = 60
    horizontal_speed = 0.5
    trail_delay_time = 2
    orbit_angle = math.radians(60.2)
    paused = False

    # Handle keyboard input for pausing
    def handle_keydown(evt):
        nonlocal paused
        if evt.key == ' ':
            paused = not paused

    scene.bind('keydown', handle_keydown)

    # Definition of slider_callback
    def slider_callback(s):
        nonlocal time_speed
        time_speed = s.value  # Link slider value to simulation speed

    # Append slider and instructions below the canvas
    scene.append_to_caption('\n\nSimulation Speed: ')
    speed_slider = slider(min=1, max=100, value=time_speed, length=300, bind=slider_callback, vertical=False)
    scene.append_to_caption('\n\nPause/Start = Leertaste')
    scene.append_to_caption('\n\n')

    # Main simulation loop
    t = 0
    trail_started = False

    while True:
        # No need for scene_is_active check here, as VPython's rate handles it
        rate(max(1, time_speed))  # Ensure rate is at least 1 to avoid division by zero if time_speed is 0

        if not paused:
            sun.pos.x += horizontal_speed
            sun_light.pos = sun.pos
            # The camera should automatically follow the sun if 'follow' is set.
            # No need to explicitly handle mouse movements for rotation with default VPython controls.
            scene.camera.follow(sun)

            # Move stars to follow sun based on their original offset
            for star in stars:
                star.obj.pos = sun.pos + star.offset

            # Move planets
            for i, planet in enumerate(planets):
                data = planets_data[i]
                angular_velocity = 2 * math.pi / (data['orbital_period'] * 100)
                angles[i] += angular_velocity

                z_orbit = data['orbital_radius'] * math.cos(angles[i] + data['phi_offset'])
                y_orbit = data['orbital_radius'] * math.sin(angles[i] + data['phi_offset']) * math.sin(orbit_angle)
                x_orbit = data['orbital_radius'] * math.sin(angles[i] + data['phi_offset']) * math.cos(orbit_angle)

                planet.pos = sun.pos + vector(x_orbit, y_orbit, z_orbit)

            # Enable trails
            if not trail_started and t * (1 / time_speed) >= trail_delay_time:
                for planet in planets:
                    planet.make_trail = True
                trail_started = True

            t += 1
        # No else block with rate(30) needed, as the simulation loop is always running
        # but only updates if not paused.
