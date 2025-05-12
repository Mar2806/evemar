from vpython import *
import math

# Set up the scene
scene = canvas(title='Tilted Solar System Spiral',
                width=2560, height=1440,
                center=vector(0, 0, 0),
                background=color.black,
                ambient=vector(0, 0, 0))

# Explicitly set the list of lights to be empty AFTER canvas creation
scene.lights = []

# Define the Sun (yellow and emissive)
sun = sphere(pos=vector(0, 0, 0), radius=2, color=vector(1, 1, 0), emissive=True)

# Define a local light source positioned at the Sun
sun_light = local_light(pos=sun.pos, color=color.white)

# Define the tilt angle of the ecliptic plane (60 degrees in radians)
ecliptic_tilt_degrees = 60
ecliptic_tilt_radians = math.radians(ecliptic_tilt_degrees)

# Define planets with their orbital radii, colors, and initial angles
planets_data = [
    {'name': 'Mercury', 'radius': 0.5, 'color': vector(0.5, 0.5, 0.5), 'orbital_radius': 5, 'orbital_period': 0.88, 'phi_offset': 0},      # Gray
    {'name': 'Venus', 'radius': 0.8, 'color': vector(1, 0.65, 0), 'orbital_radius': 8, 'orbital_period': 2.25, 'phi_offset': math.pi / 4},          # Orange
    {'name': 'Earth', 'radius': 1, 'color': vector(0, 0, 1), 'orbital_radius': 12, 'orbital_period': 3.0, 'phi_offset': math.pi / 2},              # Blue
    {'name': 'Mars', 'radius': 0.6, 'color': vector(1, 0, 0), 'orbital_radius': 16, 'orbital_period': 4.88, 'phi_offset': 3 * math.pi / 4},              # Red
    {'name': 'Jupiter', 'radius': 1.8, 'color': vector(0, 1, 1), 'orbital_radius': 25, 'orbital_period': 12.0, 'phi_offset': math.pi},          # Cyan
    {'name': 'Saturn', 'radius': 1.6, 'color': vector(1, 1, 0.6), 'orbital_radius': 35, 'orbital_period': 29.5, 'phi_offset': 5 * math.pi / 4},        # Pale Yellow
    {'name': 'Uranus', 'radius': 1.2, 'color': vector(0, 1, 0), 'orbital_radius': 48, 'orbital_period': 84.0, 'phi_offset': 3 * math.pi / 2},          # Green
    {'name': 'Neptune', 'radius': 1.1, 'color': vector(0.2, 0.2, 1), 'orbital_radius': 60, 'orbital_period': 165.0, 'phi_offset': 7 * math.pi / 4}      # Dark Blue
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
forward_speed = 0.1  # Speed of the Sun's motion "forward" (along x-axis in this case)
trail_delay_time = 2  # Time in seconds before trails start
target_orbit_time = 120
sun_orbital_speed = 0.001
sun_orbital_radius_y = 5000

# Define the rotation axis for the ecliptic plane (tilted around the z-axis)
# rotation_axis = vector(0, 0, 1)  # Now calculated dynamically
rotation_axis = vector(0,0,1)

# Function to rotate a vector around an axis
def rotate_vector(v, axis, angle):
    vprime = v * math.cos(angle) + cross(axis, v) * math.sin(angle) + axis * dot(axis, v) * (1 - math.cos(angle))
    return vprime

# Function to calculate the direction vector of the Sun's motion
def get_sun_direction(sun_pos, previous_sun_pos):
    direction = sun_pos - previous_sun_pos
    if direction.mag < 1e-6:  # Handle the case where the Sun hasn't moved much
        return vector(1, 0, 0)  # Default direction (e.g., along x-axis)
    return direction.norm()

# Simulation loop
t = 0
trail_started = False
previous_sun_pos = vector(0, 0, 0)  # Store the Sun's previous position

while True:
    rate(time_speed)  # Limit the frame rate

    # Update the position of the light source to always be at the Sun's position
    sun_light.pos = sun.pos

    # Make the Sun move "forward" (along x) and in a tilted circle
    sun_forward_motion = vector(forward_speed * t, 0, 0)
    sun_orbital_motion_unrotated = vector(0, sun_orbital_radius_y * math.cos(sun_orbital_speed * t), sun_orbital_radius_y * math.sin(sun_orbital_speed * t))
    sun_orbital_motion_rotated = rotate_vector(sun_orbital_motion_unrotated, rotation_axis, ecliptic_tilt_radians)
    sun.pos = sun_forward_motion + sun_orbital_motion_rotated

    # Calculate the Sun's direction of motion
    sun_direction = get_sun_direction(sun.pos, previous_sun_pos)
    previous_sun_pos = sun.pos  # Update previous position for next iteration

    # Calculate the rotation axis to align the orbital plane with the Sun's motion
    rotation_axis = cross(vector(0, 1, 0), sun_direction).norm() #rotation axis perpendicular to both y axis and direction of motion.
    if rotation_axis.mag < 1e-6:
        rotation_axis = vector(0,0,1)

    # Make the camera follow the Sun
    scene.camera.follow(sun)

    for i, planet in enumerate(planets):
        data = planets_data[i]
        # Update the angle based on the orbital period and an offset for the "DNA" look
        angular_velocity = 2 * math.pi / (data['orbital_period'] * 100)  # Scale time for visualization
        angles[i] += angular_velocity

        # Calculate the initial orbital position in the (un-tilted) y-z plane
        y_orbit_unrotated = data['orbital_radius'] * math.cos(angles[i] + data['phi_offset'])
        z_orbit_unrotated = data['orbital_radius'] * math.sin(angles[i] + data['phi_offset'])
        planet_orbital_unrotated = vector(0, y_orbit_unrotated, z_orbit_unrotated)

        # Rotate the orbital position by the ecliptic tilt angle, now relative to sun's motion
        planet_orbital_rotated = rotate_vector(planet_orbital_unrotated, rotation_axis, ecliptic_tilt_radians)

        # Set the planet's position relative to the moving Sun
        planet.pos = sun.pos + planet_orbital_rotated

    # Control when the trails start
    if not trail_started:
        if t * (1 / time_speed) >= trail_delay_time:
            for planet in planets:
                planet.make_trail = True
            trail_started = True

    t += 1
