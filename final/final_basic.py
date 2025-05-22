from vpython import *
import math
import tkinter  #Import tkinter for getting screen size
import os
from datetime import datetime, timedelta

def version_1():
    root = tkinter.Tk() #Create a Tkinter root window
    screen_width = root.winfo_screenwidth() #Get screen width (NOT USED IN FINAL VERSION)
    screen_height = root.winfo_screenheight() #Get screen height (NOT USED IN FINAL VERSION)
    scene = canvas(title='3D Solar System (Date-Based with Click Info)', #Create a 3D scene
                    width=1920*1.25, height=1080-50, #Set canvas size, should work for most 16:9 screens
                    center=vector(0, 0, 0),
                    background=color.black,
                    ambient=vector(0, 0, 0),
                    autoscale=False)
    scene.lights = [] #Clear default lights
    root.destroy()  #Destroy the tkinter window after getting the size

    #sun
    sun = sphere(pos=vector(0, 0, 0), radius=2, color=vector(1, 1, 0), emissive=True) #Create a sun sphere
    sun_light = local_light(pos=sun.pos, color=color.white) #Create light source sun position

    planets_data = [ # List of planets with properties
        {'name': 'Mercury', 'radius': 0.5, 'orbital_radius': 5,  'orbital_period': 0.240846, 'texture': 'evemar/final/textures/mercury.jpg', 'angle_at_start': math.radians(120), 'real_radius_km': 2439.7, 'real_orbital_radius_mio_km': 57.91},
        {'name': 'Venus',   'radius': 0.8, 'orbital_radius': 8,  'orbital_period': 0.615,     'texture': 'evemar/final/textures/venus.jpg',   'angle_at_start': math.radians(250), 'real_radius_km': 6051.8, 'real_orbital_radius_mio_km': 108.2},
        {'name': 'Earth',   'radius': 1.0, 'orbital_radius': 12, 'orbital_period': 1.0,       'texture': 'evemar/final/textures/earth.jpg',   'angle_at_start': math.radians(0),   'real_radius_km': 6371,   'real_orbital_radius_mio_km': 149.6},
        {'name': 'Mars',    'radius': 0.6, 'orbital_radius': 16, 'orbital_period': 1.8808,    'texture': 'evemar/final/textures/mars.jpg',    'angle_at_start': math.radians(45),  'real_radius_km': 3389.5, 'real_orbital_radius_mio_km': 227.9},
        {'name': 'Jupiter', 'radius': 1.8, 'orbital_radius': 25, 'orbital_period': 11.862,    'texture': 'evemar/final/textures/jupyter.jpg', 'angle_at_start': math.radians(90),  'real_radius_km': 69911,  'real_orbital_radius_mio_km': 778.5},
        {'name': 'Saturn',  'radius': 1.6, 'orbital_radius': 35, 'orbital_period': 29.4571,   'texture': 'evemar/final/textures/saturn.jpg',  'angle_at_start': math.radians(180), 'real_radius_km': 58232,  'real_orbital_radius_mio_km': 1434},
        {'name': 'Uranus',  'radius': 1.2, 'orbital_radius': 48, 'orbital_period': 84.0205,   'texture': 'evemar/final/textures/uranus.jpg',  'angle_at_start': math.radians(270), 'real_radius_km': 25362,  'real_orbital_radius_mio_km': 2871},
        {'name': 'Neptune', 'radius': 1.1, 'orbital_radius': 60, 'orbital_period': 164.8,     'texture': 'evemar/final/textures/neptune.jpg', 'angle_at_start': math.radians(315), 'real_radius_km': 24622,  'real_orbital_radius_mio_km': 4495},
    ]

    #Create rings for each planet
    for data in planets_data: 
        ring(pos=vector(0, 0, 0),
             axis=vector(0, 1, 0),
             radius=data['orbital_radius'], #Radius of ring
             thickness=0.1, 
             color=color.gray(0.3),
             opacity=0.5) 

    planets = [] #List to hold planet objects
    angles = [] #List to hold angles of planets
    
    #Create planets
    for data in planets_data:
        angle = data['angle_at_start']
        try: #Try to load texture for planet
            planet = sphere(pos=vector(data['orbital_radius'] * math.cos(angle),
                                       0,
                                       data['orbital_radius'] * math.sin(angle)),
                            radius=data['radius'], #take data from planets_data
                            texture=data['texture'],
                            make_trail=False)
        except: #If texture not found, create simple sphere
            planet = sphere(pos=vector(data['orbital_radius'] * math.cos(angle),
                                       0,
                                       data['orbital_radius'] * math.sin(angle)),
                            radius=data['radius'],
                            color=color.white,
                            make_trail=False)
        planet.name = data['name']
        planets.append(planet) #Add planet to list
        angles.append(angle)

    #Info label for clicked planet
    info_label = label(pos=vector(0,0,0),
                       text='',
                       xoffset=30, yoffset=30,
                       height=16,
                       border=6,
                       font='sans',
                       box=True,
                       opacity=0.8,
                       visible=False,
                       color=color.white,
                       background=color.gray(0.2))

    selected_planet_index = None

    #Date simulation
    start_date = datetime(2025, 5, 20)
    current_date = start_date

    #UI controls
    time_speed = 50  #Days (frames) per second
    paused = False

    #Slider function (when slider is moved)
    def slider_callback(s): 
        nonlocal time_speed
        time_speed = s.value

    #Pause/Start function (when space is pressed)
    def handle_keydown(evt):
        nonlocal paused
        if evt.key == ' ':
            paused = not paused

    #Planet click function (when planet is clicked)
    def planet_clicked(evt):
        nonlocal selected_planet_index
        clicked = scene.mouse.pick
        if clicked and hasattr(clicked, 'name'):
            for i, planet in enumerate(planets):
                if planet == clicked:
                    selected_planet_index = i
                    data = planets_data[i]
                    info_label.text = (
                        f"Name: {data['name']}\n"
                        f"Radius: {data['real_radius_km']} km\n"
                        f"Umlaufzeit: {data['orbital_period']} Jahre\n"
                        f"Abstand zur Sonne: {data['real_orbital_radius_mio_km']} Mio. km"
                    )
                    info_label.visible = True 
                    return
        selected_planet_index = None
        info_label.visible = False

    #Bind events and UI
    scene.bind('keydown', handle_keydown)
    scene.bind('mousedown', planet_clicked)

    #UI elements (text and slider)
    date_text = wtext(text=f'Date: {current_date.strftime("%Y-%m-%d")}')
    scene.append_to_caption('\n\nSimulation Speed (days/sec): ')
    speed_slider = slider(min=0, max=500, value=time_speed, length=300, bind=slider_callback)
    scene.append_to_caption('\n\n[Leertaste] Pause/Start\n\n')

    while True:
        rate(60)

        if not paused:
            #Advance time
            days_passed = time_speed / 60  #days per frame
            current_date += timedelta(days=days_passed) #update current date

            #Update planet positions
            for i, planet in enumerate(planets):
                period_days = planets_data[i]['orbital_period'] * 365.25
                angular_velocity = 2 * math.pi / period_days
                angles[i] += angular_velocity * days_passed

                x = planets_data[i]['orbital_radius'] * math.cos(angles[i])
                z = planets_data[i]['orbital_radius'] * math.sin(angles[i])
                planet.pos = vector(x, 0, z)

            #Update date display
            date_text.text = f'Date: {current_date.strftime("%Y-%m-%d")}'

        #Update info label position if visible
        if selected_planet_index is not None:
            selected_planet = planets[selected_planet_index]
            info_label.pos = selected_planet.pos + vector(0, selected_planet.radius + 2, 0)
