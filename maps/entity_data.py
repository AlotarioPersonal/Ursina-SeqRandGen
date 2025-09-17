from ursina import *
from ursina.shaders import basic_lighting_shader


floor_ent = Entity(model="cube", scale=10, ignore=True, collider='mesh', texture='brick', color=color.brown, shader=basic_lighting_shader)

