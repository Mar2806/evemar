from vpython import *
import math

# Set up the scene
scene = canvas(title='3D Solar System',
                width=2560, height=1440,
                center=vector(0, 0, 0),
                background=color.black,
                ambient=vector(0, 0, 0))

# Explicitly set the list of lights to be empty AFTER canvas creation
scene.lights = []

# Define the Sun (yellow and emissive)
# Sun's radius is much larger than planets, and in this simulation
# set to 10 for better visibility.  Real Sun's radius is 695,000 km.
sun = sphere(pos=vector(0, 0, 0), radius=10, color=color.yellow, emissive=True)

# Define a local light source positioned at the Sun
sun_light = local_light(pos=sun.pos, color=color.white)

# Define planets data with radii and orbital radii scaled to solar system (in AU)
# Mercury: Radius = 2,440 km = 0.0035 * Sun's radius
# Venus:   Radius = 6,051 km = 0.0087 * Sun's radius
# Earth:   Radius = 6,378 km = 0.0092 * Sun's radius
# Mars:    Radius = 3,396 km = 0.0049 * Sun's radius
# Jupiter: Radius = 71,492 km = 0.102  * Sun's radius
# Saturn:  Radius = 60,268 km = 0.086  * Sun's radius
# Uranus:  Radius = 25,559 km = 0.037  * Sun's radius
# Neptune: Radius = 24,764 km = 0.035  * Sun's radius

# Orbital periods are in years.
planets_data = [
    {'name': 'Mercury', 'radius': 0.035, 'color': color.gray(0.5), 'orbital_radius': 5, 'orbital_period': 0.88, 'phi_offset': 0},
    {'name': 'Venus',   'radius': 0.087, 'color': vector(1, 0.65, 0), 'orbital_radius': 8, 'orbital_period': 2.25, 'phi_offset': math.pi / 4},
    {'name': 'Earth',   'radius': 0.092, 'color': color.blue,      'orbital_radius': 12, 'orbital_period': 3.00, 'phi_offset': math.pi / 2},
    {'name': 'Mars',    'radius': 0.049, 'color': color.red,       'orbital_radius': 16, 'orbital_period': 4.88, 'phi_offset': 3 * math.pi / 4},
    {'name': 'Jupiter', 'radius': 1.02,  'color': vector(0, 1, 1), 'orbital_radius': 25, 'orbital_period': 12.00, 'phi_offset': math.pi},
    {'name': 'Saturn',  'radius': 0.86, 'color': vector(1, 1, 0.6), 'orbital_radius': 35, 'orbital_period': 29.45, 'phi_offset': 5 * math.pi / 4},
    {'name': 'Uranus',  'radius': 0.37,  'color': color.green,     'orbital_radius': 48, 'orbital_period': 84.00, 'phi_offset': 3 * math.pi / 2},
    {'name': 'Neptune', 'radius': 0.35,  'color': color.blue,      'orbital_radius': 60, 'orbital_period': 164.8, 'phi_offset': 7 * math.pi / 4}
]

planets = []
angles = [0] * len(planets_data)

# Create the planets (shininess set to 0 to avoid specular reflections)
for i, data in enumerate(planets_data):
    planet = sphere(pos=vector(data['orbital_radius'], 0, 0),
                    radius=data['radius'],
                    color=data['color'],
                    make_trail=False,
                    shininess=0)
    planets.append(planet)
    angles[i] = 0

# Simulation speed
time_speed = 50  # Adjust for faster or slower simulation
vertical_speed = 0.05 # Adjust for the speed of the upward motion
trail_delay_time = 2
sun_orbital_radius = 5000
sun_orbital_speed = 0.001
forward_speed = 0.5 # Define forward_speed

# Simulation loop
t = 0
trail_started = False

while True:
    rate(time_speed)

    # Update the position of the light source
    sun_light.pos = sun.pos

    # Make the Sun move "forward" and in a tilted circle
    sun_forward_motion = vector(forward_speed * t, 0, 0)
    sun_orbital_motion_unrotated = vector(0, sun_orbital_radius * math.cos(sun_orbital_speed * t), sun_orbital_radius * math.sin(sun_orbital_speed * t))
    sun.pos = sun_forward_motion + sun_orbital_motion_unrotated

    # Make the camera follow the Sun
    scene.camera.follow(sun)

    for i, planet in enumerate(planets):
        data = planets_data[i]
        angular_velocity = 2 * math.pi / (data['orbital_period'] * 100)
        angles[i] += angular_velocity

        y_orbit_unrotated = data['orbital_radius'] * math.cos(angles[i] + data['phi_offset'])
        z_orbit_unrotated = data['orbital_radius'] * math.sin(angles[i] + data['phi_offset'])
        planet_orbital_unrotated = vector(0, y_orbit_unrotated,  0)
        planet.pos = sun.pos + planet_orbital_unrotated

    # Control when the trails start
    if not trail_started:
        if t * (1 / time_speed) >= trail_delay_time:
            for planet in planets:
                planet.make_trail = True
            trail_started = True

    t += 1
