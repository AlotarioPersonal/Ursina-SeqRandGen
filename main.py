'''

   2D List-based Dimensional Exploration

   Version 0.5, 2025-11-23

   Exploration mock-raycast engine written in Python using URSINA.
   Written in five days, expanded upon over the course of around a year.
   

   REQUIRED PACKAGES:
   -ursina/dependencies
   -threading
   -tkinter
   -random
   
   V 0.5 PATCH:
   -ursina 8.0 optimizations automagically applied, but still need collider optimization work
   -tkinter simple dialog window, we're officially out of terminal requirement
   -height randomization for the buildings

'''

import os

if os.name=="nt":
    os.system('cls')
else:
    os.system('clear')



from ursina import * #get ursina library
from maps import level_data #level data (see maps/level_data.py)
from ursina.prefabs.first_person_controller import FirstPersonController
from tkinter import simpledialog
import threading
import random
maplevelname = level_data.level_data_rand_custom
max_height = 0

if maplevelname == level_data.level_data_rand_custom:
    global confirmation
    confirmation = simpledialog.askstring("Input", "Would you like to save the model for this generation? [y/n]")
    x_len = simpledialog.askinteger("Input", "Enter the x-length of your generated world: ")
    y_len = simpledialog.askinteger("Input", "Enter the y-length of your generated world: ")
    max_height = simpledialog.askinteger("Input", "Enter the max building height of your generated world (Max 50): ")
    for i in range(x_len):
        level_data.level_data_rand_custom.append([2] * y_len)

t_ev = threading.Event()
app = Ursina() #define app
Entity.geom=False
from maps.entity_data import floor_ent
floor_ent.geom=True






skybox = Sky() #initialize skybox
skybox.texture="skybox.png"
total = Entity(model=None, collider=None)

camera.fov = 110
skybox.eternal=True
floor_ent.eternal=True
total.eternal=True
floor_ent.position=Vec3(9999999,9999999,99999999)

last_indexed_ent = 0

cycles = 0


def resetScene():
    global total
    
    scene.clear()
    for a in scene.collidables:
        if a.geom!=True:
            if a==FirstPersonController:
                pass
            else:
                a.disable()
    total = Entity(model=None, collider=None)
    player.position=Vec3(0,0,0)

def input(key):
    global player_cam_speed
    if key == 'c': #debugging feature
        print(player.world_position)
        
    
    if key == 'escape': #kill world
        quit()
        app.run()



def gen_level(map_dat): #generate level from 2D list. this is where the fun begins
    global floor_ent
    global last_indexed_ent
    global cycles
    set_chance_height = 0
    x_incrementer = 0 #x position tracker
    z_incrementer = 0 #z position tracker
    indexer = 0 #index tracker (the actual index() function doesn't do what i need it to in this scenario because the list has only 2 datatypes)
    for row in map_dat: #row for indexer
        for item in row: #column for indexer
            if item == 0: #if the item is a floor, make it a floor
                floor_dup = duplicate(floor_ent, position=Vec3(x_incrementer*10, -10, z_incrementer*10), parent=total)
                floor_dup.eternal=False
                x_incrementer += 1 #the next block is 1 over from this item in the row (loads from left to right)
                indexer += 1 #tracks where you are in the row, so this needs to be incremented
                last_indexed_ent=0
                cycles += 1
            elif item == 1: #otherwise, it's a wall, make it a wall
                wall_dup = duplicate(floor_ent, position=Vec3(x_incrementer*10, -5, z_incrementer*10), parent=total)
                wall_dup.eternal=False
                x_incrementer += 1
                indexer += 1
                last_indexed_ent=1
                cycles += 1
                wall_dup.color=color.white
            elif item == 2: #random generation function
                random_tile = random.randrange(0,100)
                set_chance_wall = 25
                
                if random_tile<=set_chance_wall:
                    wall_dup = duplicate(floor_ent, position=Vec3(x_incrementer*10, -5, z_incrementer*10), parent=total)
                    wall_dup.eternal=False
                    wall_dup.color=color.white
                    set_chance_height = random.randint(1,max_height)
                    if set_chance_height >= 7:
                        wall_dup.scale_y+=set_chance_height
                    cycles += 1
                    set_chance_height=0
                elif random_tile>=set_chance_wall:
                    floor_dup = duplicate(floor_ent, position=Vec3(x_incrementer*10, -10, z_incrementer*10), parent=total)
                    floor_dup.eternal=False
                    cycles += 1
                    
                
                x_incrementer += 1
                indexer += 1
                last_indexed_ent=random_tile
            
            
            if indexer == len(row): #if you reach the end of the row
                indexer = 0 #reset the index tracker for the next row
                x_incrementer = 0 #reset the x position
                z_incrementer += 1 #move (physically) down one row
                cycles += 1
            print("Generating level... " + str(cycles) + " cycles have passed")
    total.combine()

        

t1=threading.Thread(target=gen_level(maplevelname))
t1.start()



def update():
    pass


player = FirstPersonController() #base ursina first person controller
player.position=(0,max_height+5,0) #set pos
player.mouse_sensitivity = Vec2(0, 50) #kill the mouse
player.cursor.color = color.red #turns the cursor gray hur dur fuck face
player.jump_height = 5 #kills jumping
player.eternal=True
player.gravity = 0.087 #rate of which player character falls
player.speed = 13

total.collider='mesh'
Entity.color="red"


scene.clear()

total.texture='resource_structure'
from maps.entity_data import floor_ent

for z in total.children: #debug
    print(str(z) + " TOTAL-CHILD")

for y in scene.entities: #debug
    print(str(y.collider) + " SCENE ENTITY")

if maplevelname==level_data.level_data_rand_custom:
    if confirmation=='y':
        varname = random.randint(1, 9999999)
        fullname = str("dungeon_" + str(varname))
        total.model.save(name=fullname, folder= Path("models_compressed"))



scene.fog_density=0.07
scene.fog_color=color.black


app.run() #execute the application
