from vpython import *
import math

# Set up the scene
scene = canvas(title='Sun and Planets Motion Through Space',
                width=2560, height=1440,
                center=vector(0, 0, 0),
                background=color.black,
                ambient=vector(0, 0, 0))

# Explicitly set the list of lights to be empty AFTER canvas creation
scene.lights = []

# Constants
AU = 149.6e6  # km, Astronomical Unit
YEAR = 365.25 * 24 * 3600  # seconds in a year
DAY = 24 * 3600 # seconds in a day

# Sun parameters
sun_radius = 696340  # km
sun_color = color.yellow
sun_velocity = vector(20, 0, 0)  # km/s, simplified for visualization (actual is ~20km/s)
sun = sphere(pos=vector(0, 0, 0), radius=sun_radius/100000, color=sun_color, emissive=True) #scaled down

# Local light source at the Sun
sun_light = local_light(pos=sun.pos, color=color.white)

# Ecliptic tilt (for visualization, using a fixed tilt)
ecliptic_tilt_degrees = 23.5
ecliptic_tilt_radians = math.radians(ecliptic_tilt_degrees)
rotation_axis = vector(0, 0, 1)

# Function to rotate a vector
def rotate_vector(v, axis, angle):
    vprime = v * math.cos(angle) + cross(axis, v) * math.sin(angle) + axis * dot(axis, v) * (1 - math.cos(angle))
    return vprime

# Planet data with more realistic parameters
planet_data = [
    {'name': 'Earth', 'radius': 6371, 'color': color.blue, 'orbital_radius': AU, 'orbital_period': YEAR,
     'initial_angle': 0, 'velocity': vector(0, 29.78, 0)},  # km/s
    {'name': 'Jupiter', 'radius': 69911, 'color': color.cyan, 'orbital_radius': 778.3e6,
     'orbital_period': 11.86 * YEAR, 'initial_angle': math.pi / 2, 'velocity': vector(0, 13.07, 0)},
]

# Create planets
planets = []
for data in planet_data:
    planet = sphere(pos=vector(data['orbital_radius'] / 100000, 0, 0),  # Scale down for visualization
                    radius=data['radius'] / 100000,  # Scale down
                    color=data['color'],
                    make_trail=True,
                    trail_type='line',
                    interval=100,
                    retain=400)
    planet.data = data  # Store the planet's data
    planets.append(planet)

# Time parameters
time_scale = 10000  # Speed up time for visualization
dt = 10000       # Time step

# Initial velocities (important for making the orbits work)
for planet in planets:
    planet.velocity = planet.data['velocity']

# Main animation loop
t = 0
while True:
    rate(100)  # Limit frame rate

    # Sun moves along a line (simplified)
    sun.pos += sun_velocity * dt / 100000  # Scale for display

    # Update planet positions and velocities
    for planet in planets:
        # Orbital motion (simplified as circular)
        angle = planet.data['initial_angle'] + (t * dt / planet.data['orbital_period']) * 2 * math.pi
        planet_orbital_unrotated = vector(planet.data['orbital_radius'] * cos(angle) / 100000, planet.data['orbital_radius'] * sin(angle) / 100000, 0)
        planet.pos = sun.pos + rotate_vector(planet_orbital_unrotated, rotation_axis, ecliptic_tilt_radians)

    t += 1
