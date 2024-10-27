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
from ursina.shaders import basic_lighting_shader, lit_with_shadows_shader
from ursina.scripts.noclip_mode import NoclipMode
from ursina import EditorCamera
from maps import level_data #level data (see maps/level_data.py)

print('Ursinacasting - Loading levels from blockmaps')

maplevelname = level_data.map1 #loads level 4 by default as it is the largest 2D list, good for gauging performance

app = Ursina(size=Vec2(800,600), borderless=False, title="Omicron") #define app
window.editor_ui.enabled = False #turn off dogshit editor ui
shooter = Audio(sound_file_name='fire.mp3', autoplay=False) #audio file
step = Audio(sound_file_name='stepstone.wav', autoplay=False)
can_shoot = True
shotgun = Entity(model='gun', parent=camera, scale=0.13, scale_x=0.15, position=(0, -0.53, 1), color=color.brown, shader=basic_lighting_shader, rotation=(-2, 0, 0)) #quake reference
player = FirstPersonController() #base ursina first person controller
blockmap_scale = 5 #size of the blocks. dont change unless you know what you're doing
player.position=(blockmap_scale,-blockmap_scale,blockmap_scale) #set pos
player.mouse_sensitivity = Vec2(0, 0) #kill the mouse
sittight = Text(text="Sit tight, exiting...")
sittight.hide()
#mouse.locked = False
input_handler.bind('up arrow','w') #bind arrow keys forward and backward to movement, doom-style
input_handler.bind('down arrow','s')
input_handler.unbind('w') #unbind base keys
input_handler.unbind('a')
input_handler.unbind('s')
input_handler.unbind('d')
player.cursor.color = color.red #turns the cursor red
player.jump_height = 0 #kills jumping
player_cam_speed = 2 #turn speed for the camera, left and right arrow keys
player.speed = 10
camera.fov = 90

Sky() #initialize skybox

player.gravity = 0.8 #rate of which player character falls

def input(key):
    global shotgun
    global shooter
    if key == 'control' and can_shoot == True: #shotgun shake control when shot
        try:
            shooter.play()
            shotgun.shake(duration=.1, magnitude=1.4, speed=.05, direction=(-45,0), delay=0, attr_name='rotation', interrupt='finish', unscaled=False, )
            camera.shake(duration=.1, magnitude=0.4, speed=.05, direction=(-1,1), delay=0, attr_name='position', interrupt='finish', unscaled=False)
            if mouse.hovered_entity.is_enemy == True: #checks for tag "is_enemy" on any hovered entities
                mouse.hovered_entity.disable()
                print('shot')
            else:
                pass
        except AttributeError:
            pass
    else:
        pass

    if key == 'c': #debugging feature
        print(player.world_position)
    
    if key == 'escape': #kill world
        sittight.show()
        quit()

def gen_level(map_dat): #generate level from 2D list. this is where the fun begins
    x_incrementer = 0 #x position tracker
    z_incrementer = 0 #z position tracker
    indexer = 0 #index tracker (the actual index() function doesn't do what i need it to in this scenario because the list has only 2 datatypes)
    for row in map_dat: #row
        for item in row: #column
            if item == 0: #if the item is a floor, make it a floor/ceiling
                newplat = Entity(model="cube", scale=blockmap_scale, collider='cube', texture='brick', shader=basic_lighting_shader, color=color.brown, position=Vec3(x_incrementer*blockmap_scale, -10, z_incrementer*blockmap_scale))
                newceil = Entity(model="cube", scale=blockmap_scale, collider='cube', texture='brick', shader=basic_lighting_shader, color=color.gray, position=Vec3(x_incrementer*blockmap_scale, -10+blockmap_scale*2, z_incrementer*blockmap_scale))
                x_incrementer += 1 #the next block is 1 over from this item in the row (loads from left to right)
                indexer += 1 #tracks where you are in the row, so this needs to be incremented
            elif item == 1: #otherwise, it's a wall, make it a wall
                newplat = Entity(model="cube", scale=blockmap_scale, collider='cube', texture='brick', shader=basic_lighting_shader, position=Vec3(x_incrementer*blockmap_scale, -5, z_incrementer*blockmap_scale))
                x_incrementer += 1
                indexer += 1
            elif item == 2: #or a floor/ceiling with an enemy in it
                newplat = Entity(model="cube", scale=blockmap_scale, collider='cube', texture='brick', shader=basic_lighting_shader, color=color.brown, position=Vec3(x_incrementer*blockmap_scale, -10, z_incrementer*blockmap_scale))
                newenemy = Entity(model="sphere", collider='cube', texture='noise', shader=basic_lighting_shader, is_enemy=True, position=Vec3(x_incrementer*blockmap_scale, -5.5, z_incrementer*blockmap_scale))
                newceil = Entity(model="cube", scale=blockmap_scale, collider='cube', texture='brick', shader=basic_lighting_shader, color=color.gray, position=Vec3(x_incrementer*blockmap_scale, -10+blockmap_scale*2, z_incrementer*blockmap_scale))
                x_incrementer += 1
                indexer += 1
            elif item == 3: #or a grass plate
                newplat = Entity(model="cube", scale=blockmap_scale, collider='cube', texture='grass', shader=basic_lighting_shader, position=Vec3(x_incrementer*blockmap_scale, -10, z_incrementer*blockmap_scale))
                x_incrementer += 1
                indexer += 1
            elif item == 4: #or a grass plate with an enemy on it
                newplat = Entity(model="cube", scale=blockmap_scale, collider='cube', texture='grass', shader=basic_lighting_shader, position=Vec3(x_incrementer*blockmap_scale, -10, z_incrementer*blockmap_scale))
                newenemy = Entity(model="sphere", collider='cube', texture='noise', shader=basic_lighting_shader, is_enemy=True, position=Vec3(x_incrementer*blockmap_scale, -5.5, z_incrementer*blockmap_scale))
            else: #if it's NONE OF THOSE, then just dont fill the slot with anything and increment
                x_incrementer += 1
                indexer += 1

            if indexer == len(row): #if you reach the end of the row
                indexer = 0 #reset the index tracker for the next row
                x_incrementer = 0 #reset the x position
                z_incrementer += 1 #move (physically) down one row

print("Generating Level, Sit Tight...")
gen_level(maplevelname) #generates level with level data provided on line 19

def update():
    global can_shoot
    if shooter.playing==True:
        can_shoot = False
    else:
        can_shoot = True

    #if held_keys['up arrow']:
    #    if step.playing==True:
    #        pass
    #    else:
    #        step.play()
    
    #doom/wolfenstein style turning
    if held_keys['left arrow']: #rotate left
        player.rotation_y -= player_cam_speed
    
    if held_keys['right arrow']: #rotate right
        player.rotation_y += player_cam_speed


#sun = DirectionalLight(rotation=Vec3(-45,45,-45), shadows=True)
#sus = AmbientLight(color = color.rgba(0, 0, 0, 0))
#sus.parent = scene
app.run() #execute the application