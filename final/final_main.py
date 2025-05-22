from final_basic import version_1
from final_rotate_slider import version_2
import tkinter as tk

def start_version_1():
    root.destroy() #Close current window
    version_1()  #Run version 1

def start_version_2():
    root.destroy()
    version_2()  #Run version 2

root = tk.Tk() #Create main window
root.title("Simulation auswählen") #Set window title

label = tk.Label(root, text="Welche Version möchtest du starten?", font=("Arial", 14))
label.pack(pady=20) #Add widget to window

btn1 = tk.Button(root, text="Version 1 starten", width=25, height=2, command=start_version_1)
btn1.pack(pady=10)

btn2 = tk.Button(root, text="Version 2 starten", width=25, height=2, command=start_version_2)
btn2.pack(pady=10)

root.mainloop() #Start Tkinter loop