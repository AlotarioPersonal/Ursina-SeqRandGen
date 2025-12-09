from ursina import *
from ursina.shaders import basic_lighting_shader

ent_generic = Entity(model="wall.obj", scale=10, ignore=True, collider='mesh', thickness=5, color=color.brown)
ent_floor = Entity(model="floor.obj", scale=10, ignore=True, collider='mesh', thickness=5, color=color.brown)