######################################
#
#   2D List-based Dimensional Exploration
#   Logan Kaminski
#   Version 0.1, 2024-10-26
#
#   REQUIRED PACKAGES: ursina (pip install ursina)
#
######################################

from ursina import * #get ursina library
from ursina.prefabs.first_person_controller import FirstPersonController
from ursina.shaders import basic_lighting_shader
from ursina.scripts.noclip_mode import NoclipMode
from maps import level_data #level data (see maps/level_data.py)

print('Ursinacasting - Loading levels from blockmaps')

maplevelname = level_data.level_data_4 #loads level 4 by default as it is the largest 2D list, good for gauging performance

app = Ursina() #define app
window.editor_ui.enabled = False #turn off dogshit editor ui
shooter = Audio(sound_file_name='fire.mp3', autoplay=False) #audio file
#these are placeholders/cut objects because i ran out of time V
#baseplat = Entity(model="cube", scale=10, collider='mesh', color=color.yellow, position=Vec3(0, -4, 0))
#ground = Entity(model=maplevelname, collider='mesh', scale=2, texture='brick', shader=basic_lighting_shader, texture_scale=(100,100))
#enemy = Entity(model='enemy', collider='mesh', scale=0.6, position=(-24,-2,15), shader=basic_lighting_shader, is_enemy=True)
#these are placeholders ^
shotgun = Entity(model='gun', parent=camera, scale=0.13, position=(0, -0.53, 1), color=color.brown, rotation=(-2, 0, 0), shader=basic_lighting_shader) #quake reference
player = FirstPersonController() #base ursina first person controller
player.position=(0,0,0) #set pos
player.mouse_sensitivity = Vec2(0, 0) #kill the mouse
input_handler.bind('up arrow','w') #bind arrow keys forward and backward to movement, doom-style
input_handler.bind('down arrow','s')
input_handler.unbind('w') #unbind base keys
input_handler.unbind('a')
input_handler.unbind('s')
input_handler.unbind('d')
player.cursor.color = color.red #turns the cursor red
player.jump_height = 0 #kills jumping
player_cam_speed = 1 #turn speed for the camera, left and right arrow keys

Sky() #initialize skybox

player.gravity = 0.8 #rate of which player character falls

def input(key):
    global shotgun
    global shooter
    if key == 'control': #shotgun shake control when shot
        try:
            shooter.play()
            shotgun.shake(duration=.1, magnitude=0.4, speed=.05, direction=(1,1), delay=0, attr_name='position', interrupt='finish', unscaled=False)
            camera.shake(duration=.1, magnitude=0.4, speed=.05, direction=(1,1), delay=0, attr_name='position', interrupt='finish', unscaled=False)
            if mouse.hovered_entity.is_enemy == True: #irrelevant but i might use it later
                mouse.hovered_entity.disable()
                print('shot')
            else:
                pass
        except AttributeError:
            pass

    if key == 'c': #debugging feature
        print(player.world_position)
    
    if key == 'escape': #kill world
        quit()

def gen_level(map_dat): #generate level from 2D list. this is where the fun begins
    x_incrementer = 0 #x position tracker
    z_incrementer = 0 #z position tracker
    indexer = 0 #index tracker (the actual index() function doesn't do what i need it to in this scenario because the list has only 2 datatypes)
    for row in map_dat: #row
        for item in row: #column
            if item == 0: #if the item is a floor, make it a floor
                print('floor')
                newplat = Entity(model="cube", scale=10, collider='mesh', texture='brick', color=color.brown, shader=basic_lighting_shader, position=Vec3(x_incrementer*10, -10, z_incrementer*10))
                x_incrementer += 1 #the next block is 1 over from this item in the row (loads from left to right)
                indexer += 1 #tracks where you are in the row, so this needs to be incremented
            else: #otherwise, it's a wall, make it a wall
                print('wall')
                newplat = Entity(model="cube", scale=10, collider='mesh', texture='brick', shader=basic_lighting_shader, position=Vec3(x_incrementer*10, -5, z_incrementer*10))
                x_incrementer += 1
                indexer += 1
            if indexer == len(row): #if you reach the end of the row
                print('end of row, reset')
                indexer = 0 #reset the index tracker for the next row
                x_incrementer = 0 #reset the x position
                z_incrementer += 1 #move (physically) down one row

        


gen_level(maplevelname) #generates level with level data provided on line 19

def update():
    #
    #print(player.rotation)

    if held_keys['shift']: #sprinting
        player.speed = 14
        player_cam_speed = 2
    else:
        player.speed = 7
        player_cam_speed = 1
    
    #doom/wolfenstein style turning
    if held_keys['left arrow']: #rotate left
        player.rotation_y -= player_cam_speed
    
    if held_keys['right arrow']: #rotate right
        player.rotation_y += player_cam_speed

app.run() #execute the application