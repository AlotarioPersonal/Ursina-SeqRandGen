from ursina import *
from ursina.mesh_importer import ursina_mesh_to_obj

app = Ursina()



my_mesh = Mesh() #paste ALLL of your mesh data (your entire .ursinamesh file) to this, exit your editor and reenter. no i don't have a better method yet

ursina_mesh_to_obj(mesh=my_mesh, name='my_exported_mesh', out_path=Path("models_compressed")) # Exports to the current directory

app.run()