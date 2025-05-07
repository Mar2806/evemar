from vpython import *
import math

# Set up the scene
scene = canvas(title='Simple 3D Solar System',
               width=800, height=600,
               center=vector(0, 0, 0),
               background=color.black)

# Define the Sun
sun = sphere(pos=vector(0, 0, 0), radius=2, color=color.yellow, emissive=True)

# Define planets with their orbital radii, colors, and initial angles
planets_data = [
    {'name': 'Mercury', 'radius': 0.5, 'color': color.gray, 'orbital_radius': 5, 'orbital_period': 0.88},
    {'name': 'Venus', 'radius': 0.8, 'color': color.orange, 'orbital_radius': 8, 'orbital_period': 2.25},
    {'name': 'Earth', 'radius': 1, 'color': color.blue, 'orbital_radius': 12, 'orbital_period': 3.0},
    {'name': 'Mars', 'radius': 0.6, 'color': color.red, 'orbital_radius': 16, 'orbital_period': 4.88},
    {'name': 'Jupiter', 'radius': 1.8, 'color': color.cyan, 'orbital_radius': 25, 'orbital_period': 12.0},
    {'name': 'Saturn', 'radius': 1.6, 'color': color.yellow, 'orbital_radius': 35, 'orbital_period': 29.5},
    {'name': 'Uranus', 'radius': 1.2, 'color': color.green, 'orbital_radius': 48, 'orbital_period': 84.0},
    {'name': 'Neptune', 'radius': 1.1, 'color': color.blue, 'orbital_radius': 60, 'orbital_period': 165.0}
]

planets = []
angles = [0] * len(planets_data)

# Create the planets
for i, data in enumerate(planets_data):
    planet = sphere(pos=vector(data['orbital_radius'], 0, 0),
                    radius=data['radius'],
                    color=data['color'],
                    make_trail=True)  # Add trails to see the orbits
    planets.append(planet)
    angles[i] = 0  # Initial angle

# Simulation speed
time_speed = 50  # Adjust for faster or slower simulation

# Simulation loop
while True:
    rate(time_speed)  # Limit the frame rate

    for i, planet in enumerate(planets):
        data = planets_data[i]
        # Update the angle based on the orbital period
        angular_velocity = 2 * math.pi / (data['orbital_period'] * 100)  # Scale time for visualization
        angles[i] += angular_velocity

        # Calculate the new x and z coordinates for a circular orbit in the x-z plane
        x = data['orbital_radius'] * math.cos(angles[i])
        z = data['orbital_radius'] * math.sin(angles[i])
        planet.pos = vector(x, 0, z)