from vpython import *
import math
import random

# Set up the scene
scene = canvas(title='3D Solar System with Interactive Starfield',
                width=2560, height=1440,
                center=vector(0, 0, 0),
                background=color.black,
                ambient=vector(0, 0, 0),
                autoscale=False)  # Disable autoscaling for stars

# Disable automatic rotation
scene.autospin = False

# Create a large number of stars for the background
num_stars = 2000
stars = []
for _ in range(num_stars):
    # Random position within a large cube
    x = random.uniform(-1000, 1000)
    y = random.uniform(-1000, 1000)
    z = random.uniform(-1000, 1000)
    # Random color (mostly white with slight variation)
    c = vector(random.uniform(0.7, 1), random.uniform(0.7, 1), random.uniform(0.7, 1))
    star = sphere(pos=vector(x, y, z), radius=1, color=c, emissive=True, shininess=0)  # Make stars emissive and not shiny
    stars.append(star)

# Explicitly set the list of lights to be empty AFTER canvas creation
scene.lights = []

# Define the Sun (yellow and emissive)
sun = sphere(pos=vector(0, 0, 0), radius=2, color=vector(1, 1, 0), emissive=True)

# Define a local light source positioned at the Sun
sun_light = local_light(pos=sun.pos, color=color.white)

# Define planets with their orbital radii, colors, and initial angles
planets_data = [
    {'name': 'Mercury', 'radius': 0.5, 'color': vector(0.5, 0.5, 0.5), 'orbital_radius': 5, 'orbital_period': 0.88, 'phi_offset': 0},
    {'name': 'Venus', 'radius': 0.8, 'color': vector(1, 0.65, 0), 'orbital_radius': 8, 'orbital_period': 2.25, 'phi_offset': math.pi / 4},
    {'name': 'Earth', 'radius': 1, 'color': vector(0, 0, 1), 'orbital_radius': 12, 'orbital_period': 3.0, 'phi_offset': math.pi / 2},
    {'name': 'Mars', 'radius': 0.6, 'color': vector(1, 0, 0), 'orbital_radius': 16, 'orbital_period': 4.88, 'phi_offset': 3 * math.pi / 4},
    {'name': 'Jupiter', 'radius': 1.8, 'color': vector(0, 1, 1), 'orbital_radius': 25, 'orbital_period': 12.0, 'phi_offset': math.pi},
    {'name': 'Saturn', 'radius': 1.6, 'color': vector(1, 1, 0.6), 'orbital_radius': 35, 'orbital_period': 29.5, 'phi_offset': 5 * math.pi / 4},
    {'name': 'Uranus', 'radius': 1.2, 'color': vector(0, 1, 0), 'orbital_radius': 48, 'orbital_period': 84.0, 'phi_offset': 3 * math.pi / 2},
    {'name': 'Neptune', 'radius': 1.1, 'color': vector(0.2, 0.2, 1), 'orbital_radius': 60, 'orbital_period': 165.0, 'phi_offset': 7 * math.pi / 4}
]

planets = []
angles = [0] * len(planets_data)

# Create the planets (shininess set to 0 to avoid specular reflections)
for i, data in enumerate(planets_data):
    planet = sphere(pos=vector(data['orbital_radius'], 0, 0),
                    radius=data['radius'],
                    color=data['color'],
                    make_trail=False,  # Initially don't create trails
                    shininess=0)
    planets.append(planet)
    angles[i] = 0  # Initial angle

# Simulation speed
time_speed = 50  # Adjust for faster or slower simulation
horizontal_speed = 0.5  # Adjust for the speed of the horizontal motion of the Sun
trail_delay_time = 2  # Time in seconds before trails start
orbit_angle = math.radians(60.2)  # Angle of the orbital plane relative to the sun's motion

# Store the previous mouse position
prev_mouse_pos = None

# Function to handle mouse movement and rotate the scene
def handle_mouse_move(evt):
    global prev_mouse_pos
    if prev_mouse_pos is not None:
        # Calculate the change in mouse position
        dx = evt.pos.x - prev_mouse_pos.x
        dy = evt.pos.y - prev_mouse_pos.y

        # Rotate the scene based on mouse movement
        scene.rotate(angle=dx * 0.002, axis=vector(0, 1, 0))  # Rotate around y-axis
        scene.rotate(angle=dy * 0.002, axis=vector(1, 0, 0))  # Rotate around x-axis

    prev_mouse_pos = evt.pos

# Bind the mousemove event to the handle_mouse_move function
scene.bind('mousemove', handle_mouse_move)

# Simulation loop
t = 0
trail_started = False

while True:
    rate(time_speed)  # Limit the frame rate

    # Update the position of the light source to always be at the Sun's position
    sun_light.pos = sun.pos

    # Move the Sun horizontally
    sun.pos.x += horizontal_speed

    # Make the camera follow the Sun
    scene.camera.follow(sun)

    for i, planet in enumerate(planets):
        data = planets_data[i]
        # Update the angle based on the orbital period and an offset
        angular_velocity = 2 * math.pi / (data['orbital_period'] * 100)
        angles[i] += angular_velocity

        # Calculate the new x, y, and z coordinates for the angled orbit.
        z_orbit = data['orbital_radius'] * math.cos(angles[i] + data['phi_offset'])
        y_orbit = data['orbital_radius'] * math.sin(angles[i] + data['phi_offset']) * math.sin(orbit_angle)
        x_orbit = data['orbital_radius'] * math.sin(angles[i] + data['phi_offset']) * math.cos(orbit_angle)

        # Set the planet's position relative to the moving Sun
        planet.pos = sun.pos + vector(x_orbit, y_orbit, z_orbit)

    # Control when the trails start
    if not trail_started:
        if t * (1 / time_speed) >= trail_delay_time:
            for planet in planets:
                planet.make_trail = True
            trail_started = True

    t += 1
