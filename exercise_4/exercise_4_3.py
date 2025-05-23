# Import modules
from qgis.core import QgsProject, QgsApplication # type: ignore
from qgis.core import QgsVectorLayer, QgsProject # type: ignore
from qgis.core import * # type: ignore
from qgis.core import QgsApplication # type: ignore
import os

# Supply path to qgis install location
QgsApplication.setPrefixPath(r"C:\Program Files\QGIS 3.34.8", True) 

# Path to data and QGIS-project
project_path = r"C:\Users\philippmundinger\vsproject.qgz"  
folder = r"C:\Users\philippmundinger\pycourse"

 # Create QGIS instance and "open" the project
project = QgsProject.instance()
project.read(project_path)

for file in os.listdir(folder):
    if file.endswith('.shp'):
        basename = os.path.splitext(os.path.basename(file))[0]
        # Create layer
        layer = QgsVectorLayer(os.path.join(folder,file), basename, "ogr")

# Check if layer is valid
        if not layer.isValid():
            print("Error loading the layer!")
            continue
        
        # Add layer to project
        project.addMapLayer(layer)#
        print(f"Shapefile: {basename} added to the project")
    else:
        continue  
    
    # Save 
project.write()
