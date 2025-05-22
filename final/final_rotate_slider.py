from vpython import *
import math
import random
import tkinter  #Import tkinter for getting screen size
import os

def version_2():
    root = tkinter.Tk() #Create a Tkinter root window
    screen_width = root.winfo_screenwidth() #Get screen width
    screen_height = root.winfo_screenheight() #Get screen height
    root.destroy()  #Destroy the tkinter window after getting the size

    scene_width = int(screen_width * 0.985 + 20) #Calculate scene width
    scene_height = int(screen_height * 0.85 + 20) #Calculate scene height

    scene = canvas(title='3D Solar System ', #Set up the scene
                    width=1920*1.28, height=1080+60,
                    center=vector(0, 0, 0),
                    background=color.black,
                    ambient=vector(0, 0, 0),
                    autoscale=False,
                    title_color=color.black)

    scene.autospin = False #Disable automatic camera rotation

    class Star: #Define Star class
        def __init__(self, offset):
            self.offset = offset
            self.obj = sphere(pos=offset, radius=1,
                                color=vector(random.uniform(0.7, 1), random.uniform(0.7, 1), random.uniform(0.7, 1)),
                                emissive=True, shininess=0)

    def generate_star_shell(radius, count): #Function to generate stars in a spherical shell
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

    star_radius = 1500 #Set star shell radius
    num_stars = 2000 #Set number of stars
    stars = generate_star_shell(radius=star_radius, count=num_stars) #Generate stars

    scene.lights = [] #Disable default lighting

    sun = sphere(pos=vector(0, 0, 0), radius=2, color=vector(1, 1, 0), emissive=True) #Define the Sun
    sun_light = local_light(pos=sun.pos, color=color.white) #Create light source at sun's position

    planets_data = [ #List of planet data
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

    planets = [] #List to hold planet objects
    angles = [0] * len(planets_data) #List to hold angles of planets

    for i, data in enumerate(planets_data): #Create planets
        try: #Try to load texture
            planet = sphere(
                pos=vector(data['orbital_radius'], 0, 0),
                radius=data['radius'],
                texture=data['texture'],  #Apply the texture
                make_trail=False,
                shininess=0
            )
            planet.name = data['name']
            planets.append(planet)
            angles[i] = 0
        except Exception as e: #Handle texture loading error
            print(f"Error loading texture for {data['name']}: {e}")
            planet = sphere(pos=vector(data['orbital_radius'], 0, 0),
                             radius=data['radius'],
                             color=color.white,  #Use white if texture fails
                             make_trail=False,
                             shininess=0)
            planet.name = data['name']
            planets.append(planet)
            angles[i] = 0

    time_speed = 60 #Simulation speed
    horizontal_speed = 0.5 #Sun's horizontal movement speed
    trail_delay_time = 2 #Delay before trails appear
    orbit_angle = math.radians(60.2) #Orbital plane angle
    paused = False #Pause state

    def handle_keydown(evt): #Handle keyboard input
        nonlocal paused
        if evt.key == ' ':
            paused = not paused

    scene.bind('keydown', handle_keydown) #Bind keyboard event

    def slider_callback(s): #Slider callback function
        nonlocal time_speed
        time_speed = s.value  #Link slider value to simulation speed

    scene.append_to_caption('\n\nSimulation Speed: ') #Add text to scene caption
    speed_slider = slider(min=1, max=100, value=time_speed, length=300, bind=slider_callback, vertical=False) #Create speed slider
    scene.append_to_caption('\n\nPause/Start = Leertaste') #Add pause instruction
    scene.append_to_caption('\n\n')

    t = 0 #Initialize time counter
    trail_started = False #Flag for trails

    while True: #Main simulation loop
        rate(max(1, time_speed)) #Set simulation rate

        if not paused:
            sun.pos.x += horizontal_speed #Move sun horizontally
            sun_light.pos = sun.pos #Update sun light position
            scene.camera.follow(sun) #Camera follows the sun

            for star in stars: #Move stars to follow sun
                star.obj.pos = sun.pos + star.offset

            for i, planet in enumerate(planets): #Move planets
                data = planets_data[i]
                angular_velocity = 2 * math.pi / (data['orbital_period'] * 100) #Calculate angular velocity
                angles[i] += angular_velocity #Update planet angle

                z_orbit = data['orbital_radius'] * math.cos(angles[i] + data['phi_offset']) #Calculate Z position
                y_orbit = data['orbital_radius'] * math.sin(angles[i] + data['phi_offset']) * math.sin(orbit_angle) #Calculate Y position
                x_orbit = data['orbital_radius'] * math.sin(angles[i] + data['phi_offset']) * math.cos(orbit_angle) #Calculate X position

                planet.pos = sun.pos + vector(x_orbit, y_orbit, z_orbit) #Set planet position

            if not trail_started and t * (1 / time_speed) >= trail_delay_time: #Enable trails after delay to avoid startup clatter
                for planet in planets:
                    planet.make_trail = True
                trail_started = True

            t += 1 #Increment time counter