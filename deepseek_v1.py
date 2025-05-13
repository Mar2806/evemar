from vpython import *
import math
import random
import tkinter

# Get screen size
root = tkinter.Tk()
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
root.destroy()

# Scene setup
scene_width = int(screen_width * 0.985)
scene_height = int(screen_height * 0.85)

scene = canvas(title='3D Solar System',
               width=scene_width, height=scene_height,
               center=vector(0, 0, 0),
               background=color.black,
               ambient=vector(0, 0, 0),
               autoscale=False)

scene.autospin = False

# Track interaction state
is_focused = True  # Assume focused when running locally
mouse_down = False
last_mouse_pos = None

# Star Generation
class Star:
    def __init__(self, offset):
        self.offset = offset
        self.obj = sphere(pos=offset, radius=1,
                         color=vector(random.uniform(0.7, 1), 
                                    random.uniform(0.7, 1), 
                                    random.uniform(0.7, 1)),
                         emissive=True, shininess=0)

def generate_star_shell(radius, count):
    stars = []
    for _ in range(count):
        theta = random.uniform(0, 2 * math.pi)
        phi = random.uniform(0, math.pi)
        x = radius * math.sin(phi) * math.cos(theta)
        y = radius * math.sin(phi) * math.sin(theta)
        z = radius * math.cos(phi)
        stars.append(Star(vector(x, y, z)))
    return stars

stars = generate_star_shell(radius=1500, count=2000)
scene.lights = []

# Solar System
sun = sphere(pos=vector(0, 0, 0), radius=2, color=color.yellow, emissive=True)
sun_light = local_light(pos=sun.pos, color=color.white)

planets_data = [
    {'name': 'Mercury', 'radius': 0.5, 'color': vector(0.5, 0.5, 0.5), 
     'orbital_radius': 5, 'period': 0.88, 'phi_offset': 0},
    {'name': 'Venus', 'radius': 0.8, 'color': vector(1, 0.65, 0), 
     'orbital_radius': 8, 'period': 2.25, 'phi_offset': math.pi/4},
    # ... (rest of your planet data)
]

planets = []
angles = [0] * len(planets_data)
for i, data in enumerate(planets_data):
    planet = sphere(pos=vector(data['orbital_radius'], 0, 0),
                   radius=data['radius'],
                   color=data['color'],
                   make_trail=False,
                   shininess=0,
                   name=data['name'])
    planets.append(planet)

# Interaction Handling
def handle_mouse_down(evt):
    global mouse_down, last_mouse_pos
    mouse_down = True
    last_mouse_pos = vector(evt.pos.x, evt.pos.y)
    
    picked = scene.mouse.pick
    if picked and hasattr(picked, 'name'):
        print(f"Selected: {picked.name}")

def handle_mouse_up(evt):
    global mouse_down
    mouse_down = False

def handle_mouse_move(evt):
    global last_mouse_pos
    if not mouse_down:
        return
        
    current_pos = vector(evt.pos.x, evt.pos.y)
    if last_mouse_pos:
        dx = current_pos.x - last_mouse_pos.x
        dy = current_pos.y - last_mouse_pos.y
        scene.camera.rotate(angle=dx * 0.002, axis=vector(0, 1, 0))
        scene.camera.rotate(angle=dy * 0.002, axis=vector(1, 0, 0))
    last_mouse_pos = current_pos

scene.bind('mousedown', handle_mouse_down)
scene.bind('mouseup', handle_mouse_up)
scene.bind('mousemove', handle_mouse_move)

# Animation Control
time_speed = 60
def set_speed(s):
    global time_speed
    time_speed = s.value

scene.append_to_caption('\n\nSimulation Speed: ')
slider(min=0, max=100, value=time_speed, length=300, bind=set_speed)
scene.append_to_caption('\n')

# Main Loop
orbit_angle = math.radians(60.2)
while True:
    rate(time_speed)
    
    # Update planets
    for i, planet in enumerate(planets):
        data = planets_data[i]
        angles[i] += 2 * math.pi / (data['period'] * 100)
        
        x = data['orbital_radius'] * math.sin(angles[i] + data['phi_offset']) * math.cos(orbit_angle)
        y = data['orbital_radius'] * math.sin(angles[i] + data['phi_offset']) * math.sin(orbit_angle)
        z = data['orbital_radius'] * math.cos(angles[i] + data['phi_offset'])
        
        planet.pos = sun.pos + vector(x, y, z)
    
    # Update stars
    for star in stars:
        star.obj.pos = sun.pos + star.offset
    
    sun_light.pos = sun.pos