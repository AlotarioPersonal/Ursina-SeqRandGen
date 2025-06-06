######################################
#
#   2D List-based Dimensional Exploration
#   L. Kaminski
#   Version 0.2, 2024-11-10
#
#   REQUIRED PACKAGES:
#   -ursina/dependencies
#   -threading
#
######################################

from ursina import * #get ursina library
from maps import level_data #level data (see maps/level_data.py)
from ursina.prefabs.first_person_controller import FirstPersonController
from ursina.shaders import basic_lighting_shader
import threading

maplevelname = level_data.level_data_rand

t_ev = threading.Event()
app = Ursina() #define app
Entity.geom=False
from maps.entity_data import floor_ent
from maps.entity_data import wall
floor_ent.geom=True
wall.geom=True


window.editor_ui.disable()

player = FirstPersonController() #base ursina first person controller
player.position=(0,0,0) #set pos
player.mouse_sensitivity = Vec2(0, 0) #kill the mouse

camera.clip_plane_far=75
input_handler.bind('up arrow','w') #bind arrow keys forward and backward to movement, doom-style
input_handler.bind('down arrow','s')
input_handler.unbind('w')
input_handler.unbind('a')
input_handler.unbind('s')
input_handler.unbind('d')
player.cursor.color = color.dark_gray #turns the cursor red hur dur fuck face
player.jump_height = 0 #kills jumping
player_cam_speed = 2 #turn speed for the camera, left and right arrow keys
skybox = Sky() #initialize skybox
skybox.texture="skybox.png"
scene.fog_density=0.07
scene.fog_color=color.black
camera.fov = 110
player.eternal=True
skybox.eternal=True
floor_ent.eternal=True
wall.eternal=True
floor_ent.position=Vec3(9999999,9999999,99999999)
wall.position=Vec3(9999999,9999999,99999999)

last_indexed_ent = 0

player.gravity = 0.98 #rate of which player character falls
player.speed = 13


#define entity types


def resetScene():
    player.position=Vec3(0,0,0)
    scene.clear()
    player.position=Vec3(0,0,0)


def input(key):
    global player_cam_speed
    if key == 'c': #debugging feature
        print(player.world_position)
    
    if key == 'r': #debugging feature
        resetScene()
        gen_level(maplevelname)
    
    if key == 'escape': #kill world
        quit()
        app.run()



def gen_level(map_dat): #generate level from 2D list. this is where the fun begins
    global floor_ent
    global wall
    global last_indexed_ent
    x_incrementer = 0 #x position tracker
    z_incrementer = 0 #z position tracker
    indexer = 0 #index tracker (the actual index() function doesn't do what i need it to in this scenario because the list has only 2 datatypes)
    for row in map_dat: #row for indexer
        for item in row: #column for indexer
            if item == 0: #if the item is a floor, make it a floor
                floor_dup = duplicate(floor_ent, position=Vec3(x_incrementer*10, -10, z_incrementer*10))
                floor_dup.eternal=False
                x_incrementer += 1 #the next block is 1 over from this item in the row (loads from left to right)
                indexer += 1 #tracks where you are in the row, so this needs to be incremented
                last_indexed_ent=0
                #floor_ent.combine()
            elif item == 1: #otherwise, it's a wall, make it a wall
                wall_dup = duplicate(wall, position=Vec3(x_incrementer*10, -5, z_incrementer*10))
                wall_dup.eternal=False
                x_incrementer += 1
                indexer += 1
                last_indexed_ent=1
                #wall.combine()
            elif item == 2: #random generation function
                random_tile = random.randrange(0,100)
                
                if random_tile<=25:
                    wall_dup = duplicate(wall, position=Vec3(x_incrementer*10, -5, z_incrementer*10))
                    wall_dup.eternal=False
                    #wall.combine()
                elif random_tile>=25:
                    floor_dup = duplicate(floor_ent, position=Vec3(x_incrementer*10, -10, z_incrementer*10))
                    floor_dup.eternal=False
                    #floor_ent.combine()
                    
                
                x_incrementer += 1
                indexer += 1
                last_indexed_ent=random_tile
            
            
            if indexer == len(row): #if you reach the end of the row
                indexer = 0 #reset the index tracker for the next row
                x_incrementer = 0 #reset the x position
                z_incrementer += 1 #move (physically) down one row
            print("generating...")

        

#t1=threading.Thread(target=gen_level(maplevelname))
#t1.start()
gen_level(maplevelname)
#gen_level(maplevelname) #generates level with level data provided on line 18

def update():
    #
    #print(player.speed)
    
    #doom/wolfenstein style turning
    if held_keys['left arrow']: #rotate left
        player.rotation_y -= player_cam_speed
    
    if held_keys['right arrow']: #rotate right
        player.rotation_y += player_cam_speed

app.run() #execute the application