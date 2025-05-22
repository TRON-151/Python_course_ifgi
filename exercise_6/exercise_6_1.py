# first we will create a empty layer with three given fields
uri = "polygon?crs=EPSG:25832&field=standard_land_value:float&field=type:string&field=district:string"
new_layer = QgsVectorLayer(uri, "temp_standard_land_value_muenster", "memory")

# lets create a provider for this layer
new_layer_provider = new_layer.dataProvider() 


# now we will read the content of the csv file 
csv_layer = QgsProject.instance().mapLayersByName("standard_land_value_muenster")[0]

# lets iterate through all the features of the csv file layer
for feature in csv_layer.getFeatures():

    # here we will store the individual values as need in variables
    std_value = feature.attribute('standard_land_value')
    type = feature.attribute('type')
    dist = feature.attribute('district')
    geom = feature.attribute('geometry')

    #print(geom)
    
    # here we will create a new feature for each iteration
    new_feature = QgsFeature(new_layer.fields())
    # and add all three values in that feature
    new_feature.setAttribute("standard_land_value", std_value)
    new_feature.setAttribute("type", type)
    new_feature.setAttribute("district", dist)
    
    # converting the geo into Qgis geometry
    geom = QgsGeometry.fromWkt(geom)
    
    # now setting the geometry for the new feature for each iteration
    new_feature.setGeometry(geom)
    
    # now we will use the new_layer_provider to add the new features to the new_layer
    new_layer_provider.addFeatures([new_feature])


# now we will add this layer to the map
QgsProject().instance().addMapLayer(new_layer)

