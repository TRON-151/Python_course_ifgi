
# createcreate instance of the QGIS application
mc = iface.mapCanvas()
da = QgsDistanceArea()

# load the layers
districts = QgsProject.instance().mapLayersByName("Muenster_City_Districts")[0]
schools = QgsProject.instance().mapLayersByName("Schools")[0]
request = QgsFeatureRequest()

# set the request to only get the features that are in the layer
nameClause = QgsFeatureRequest.OrderByClause("Name", ascending = True)
orderby = QgsFeatureRequest.OrderBy([nameClause])
request.setOrderBy(orderby)

# get the features of the layer and create a list of district names
features = districts.getFeatures(request)
district_names = [feature["Name"] for feature in features]

# create a dialog to select the district
parent = iface.mainWindow()
sDistrict, bOk = QInputDialog.getItem(parent, "District Names", "Select District: ",district_names)

# check if the user cancelled the dialog or not
if not bOk:
    QMessageBox.warning(parent, "Schools", "User cancelled")
else:
    # create a list to store the intersecting schools
    intersecting_schools = []
    
    # elect district by name
    districts.selectByExpression(f"\"Name\" = '{sDistrict}'", QgsVectorLayer.SetSelection)
    selected_features = districts.selectedFeatures()
    
    # check if the district is selected or not. iterate over the selected features
    for feature in selected_features: 
        district_geom=feature.geometry()
        centroid = district_geom.centroid()
        for sfeature in schools.getFeatures():
            school_geom=sfeature.geometry()
            # check if the school is in the district
            if district_geom.intersects(school_geom):
                xS = sfeature.geometry().get().x()
                yS = sfeature.geometry().get().y()
                xD = centroid.get().x()
                yD = centroid.get().y()
                distance=da.measureLine([QgsPointXY(xS,yS),QgsPointXY(xD,yD)])/1000
                intersecting_schools.append(f"{sfeature['Name']},{sfeature['SchoolType']}\nDistance to City Center: {distance:.2f} km")
    # sort List
    intersecting_schools.sort()
    mc.zoomToSelected()
    if intersecting_schools:
        QMessageBox.information(parent, f"schools in {sDistrict}", "\n\n".join(intersecting_schools))
    else:
        QMessageBox.information(parent, "No Schools", f"No schools found in '{sDistrict}'.")
        
    




