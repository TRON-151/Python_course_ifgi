import csv

# csv erstellen
with open(r'C:\Users\Bem\Downloads\SchoolReport.csv', 'w', newline='') as csvfile:
    # in csv schreiben
    csvwriter = csv.writer(csvfile, delimiter=';')
    
    # header row
    csvwriter.writerow(['Name', 'X', 'Y'])
    
    # Layer nach namen ausgeben
    layers = QgsProject.instance().mapLayersByName("Schools")
    layer = layers[0]
    # alle features 
    features = layer.getFeatures()
    for feature in features:
        # Koordinaten abfragen
        coords = feature.geometry().asPoint()
        name = feature["Name"]
        #write to file
        csvwriter.writerow([name, coords.x(), coords.y()])
