from vpython import *
import math

# Set up the scene
scene = canvas(title='Simple 3D Solar System',
               width=800, height=600,
               center=vector(0, 0, 0),
               background=color.black,
               ambient=vector(0, 0, 0))

# Explicitly set the list of lights to be empty AFTER canvas creation
scene.lights = []

# Define the Sun (yellow and emissive)
sun = sphere(pos=vector(0, 0, 0), radius=2, color=vector(1, 1, 0), emissive=True)

# Define a local light source positioned at the Sun
sun_light = local_light(pos=sun.pos, color=color.white)

# Define planets with their orbital radii, colors, and initial angles
planets_data = [
    {'name': 'Mercury', 'radius': 0.5, 'color': vector(0.5, 0.5, 0.5), 'orbital_radius': 5, 'orbital_period': 0.88},      # Gray
    {'name': 'Venus', 'radius': 0.8, 'color': vector(1, 0.65, 0), 'orbital_radius': 8, 'orbital_period': 2.25},          # Orange
    {'name': 'Earth', 'radius': 1, 'color': vector(0, 0, 1), 'orbital_radius': 12, 'orbital_period': 3.0},              # Blue
    {'name': 'Mars', 'radius': 0.6, 'color': vector(1, 0, 0), 'orbital_radius': 16, 'orbital_period': 4.88},              # Red
    {'name': 'Jupiter', 'radius': 1.8, 'color': vector(0, 1, 1), 'orbital_radius': 25, 'orbital_period': 12.0},          # Cyan
    {'name': 'Saturn', 'radius': 1.6, 'color': vector(1, 1, 0.6), 'orbital_radius': 35, 'orbital_period': 29.5},        # Pale Yellow
    {'name': 'Uranus', 'radius': 1.2, 'color': vector(0, 1, 0), 'orbital_radius': 48, 'orbital_period': 84.0},          # Green
    {'name': 'Neptune', 'radius': 1.1, 'color': vector(0.2, 0.2, 1), 'orbital_radius': 60, 'orbital_period': 165.0}      # Dark Blue
]

planets = []
angles = [0] * len(planets_data)

# Create the planets (shininess set to 0 to avoid specular reflections)
for i, data in enumerate(planets_data):
    planet = sphere(pos=vector(data['orbital_radius'], 0, 0),
                    radius=data['radius'],
                    color=data['color'],
                    make_trail=True,
                    shininess=0)
    planets.append(planet)
    angles[i] = 0  # Initial angle

# Simulation speed
time_speed = 50  # Adjust for faster or slower simulation

# Simulation loop
while True:
    rate(time_speed)  # Limit the frame rate

    # Update the position of the light source to always be at the Sun's position
    sun_light.pos = sun.pos

    for i, planet in enumerate(planets):
        data = planets_data[i]
        # Update the angle based on the orbital period
        angular_velocity = 2 * math.pi / (data['orbital_period'] * 100)  # Scale time for visualization
        angles[i] += angular_velocity

        # Calculate the new x and z coordinates for a circular orbit in the x-z plane
        x = data['orbital_radius'] * math.cos(angles[i])
        z = data['orbital_radius'] * math.sin(angles[i])
        planet.pos = vector(x, 0, z)