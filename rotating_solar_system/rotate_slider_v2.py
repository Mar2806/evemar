from vpython import *
import math
import random
import tkinter

# Get the screen size using tkinter
root = tkinter.Tk()
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
root.destroy()

# Calculate scene dimensions
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
scene.autospin = False

# --- Generate spherical shell of stars ---
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

# Create planets
for i, data in enumerate(planets_data):
    planet = sphere(pos=vector(data['orbital_radius'], 0, 0),
                    radius=data['radius'],
                    color=data['color'],
                    make_trail=False,
                    shininess=0,
                    name=data['name'])
    planets.append(planet)
    angles[i] = 0

# Simulation parameters
time_speed = 60
horizontal_speed = 0.5
trail_delay_time = 2
orbit_angle = math.radians(60.2)

prev_mouse_pos = None
is_dragging = False # Track if the mouse is being dragged

def handle_mouse_move(evt):
    global prev_mouse_pos, is_dragging
    if evt.buttons == 1: # Left button is pressed
        is_dragging = True
        if prev_mouse_pos is not None:
            dx = evt.pos.x - prev_mouse_pos.x
            dy = evt.pos.y - prev_mouse_pos.y
            scene.camera.rotate(angle=dx * 0.002, axis=vector(0, 1, 0))
            scene.camera.rotate(angle=dy * 0.002, axis=vector(1, 0, 0))
    prev_mouse_pos = evt.pos

def handle_mouse_down(evt):
    global prev_mouse_pos, is_dragging
    prev_mouse_pos = evt.pos
    is_dragging = False # Reset drag flag on a new mouse down

def handle_mouse_up(evt):
    global is_dragging
    if not is_dragging: # If it's a click and not a drag
        clicked_object = scene.mouse.pick
        if clicked_object:
            if hasattr(clicked_object, 'name'):
                print(f"Clicked on: {clicked_object.name}")
            else:
                print("Clicked on an unknown object.")
    is_dragging = False # Reset drag flag on mouse up

scene.bind('mousemove', handle_mouse_move)
scene.bind('mousedown', handle_mouse_down)
scene.bind('mouseup', handle_mouse_up)

# Add a horizontal slider
def slider_callback(s):
    global time_speed
    time_speed = s.value

scene.append_to_caption('\n\nSimulation Speed: ')
speed_slider = slider(min=0, max=100, value=time_speed, length=300, bind=slider_callback, vertical=False)
scene.append_to_caption('\n\n')

# Main simulation loop
t = 0
trail_started = False

while True:
    rate(time_speed)

    sun.pos.x += horizontal_speed
    sun_light.pos = sun.pos
    scene.camera.follow(sun)

    # Move stars
    for star in stars:
        star.obj.pos = sun.pos + star.offset

    # Move planets
    if time_speed > 0:
        for i, planet in enumerate(planets):
            data = planets_data[i]
            angular_velocity = 2 * math.pi / (data['orbital_period'] * 100)
            angles[i] += angular_velocity

            z_orbit = data['orbital_radius'] * math.cos(angles[i] + data['phi_offset'])
            y_orbit = data['orbital_radius'] * math.sin(angles[i] + data['phi_offset']) * math.sin(orbit_angle)
            x_orbit = data['orbital_radius'] * math.sin(angles[i] + data['phi_offset']) * math.cos(orbit_angle)

            planet.pos = sun.pos + vector(x_orbit, y_orbit, z_orbit)

    # Enable trails
    if not trail_started and t * (1 / max(1, time_speed)) >= trail_delay_time and time_speed > 0:
        for planet in planets:
            planet.make_trail = True
        trail_started = True

    sleep(0.001)
    t += 1