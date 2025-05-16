# main popup window 
parent_window = iface.mainWindow()

# input from the users, coordinates and the confirmation
sCoords, bOk = QInputDialog.getText(parent_window, "Geoguesser", "Enter coordinates as latitdue, longitude", text = "51.96066,7.62476")

# converting the input string into floating number
x,y = map(float,sCoords.split(","))

# converting these x y floating numbers into point
point=QgsPointXY(y,x)

# creating a tronsformation from  WGS84-coordinates to ETRS89 32N
crs_of_coordinates = QgsCoordinateReferenceSystem(4326)
crs_of_district_layer = QgsCoordinateReferenceSystem(25832)
transformer = QgsCoordinateTransform(crs_of_coordinates, crs_of_district_layer, QgsProject.instance())

# transforming point to new ETRS89 32N coordinates
point = transformer.transform(point)

# now into a geometry 
point_geometry = QgsGeometry.fromPointXY(point)

# assigning a layer to a variable to get its features
districts = QgsProject.instance().mapLayersByName("Muenster_City_Districts")[0]

# checker to check for intersection happening or not
checker = 0

# iterating through each district features 
for features in districts.getFeatures():
    # getting the geometry of the single district
    district_geometry = features.geometry()

    # if point_geometry intersects with the district geometry than we increment checker and give output.
    if point_geometry.intersects(district_geometry):
        QMessageBox.information(parent_window, "Results", f"Wow! You Win! \n Your coordinates intersects with {features['Name']} district")
        checker += 1
        
    # else we continue the loop 
    elif point_geometry.intersects(district_geometry) == False:
        continue

print(checker)
# if the checker is empty then the coordinates of points didn't intersect and new output
if checker == 0:
    QMessageBox.information(parent_window, "Results", "Better luck next time kid!")