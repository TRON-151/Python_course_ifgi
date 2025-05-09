import csv
from qgis.core import QgsProject # type: ignore

# create csv
with open(r'C:\Users\Bem\Downloads\SchoolReport.csv', 'w', newline='') as csvfile:
    # write csv
    csvwriter = csv.writer(csvfile, delimiter=';')
    
    # header row
    csvwriter.writerow(['Name', 'X', 'Y'])
    
    # output each layer by name 
    layers = QgsProject.instance().mapLayersByName("Schools")
    layer = layers[0]
    
    # get Layer by name and the first Layer in the returned List
    features = layer.getFeatures()
    for feature in features:
        # request coordinates
        coords = feature.geometry().asPoint()
        name = feature["Name"]
        # write to file
        csvwriter.writerow([name, coords.x(), coords.y()])