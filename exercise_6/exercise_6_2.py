# Create a map canvas object first
mc = iface.mapCanvas()

# create a object for pool layer
pool_layer = QgsProject.instance().mapLayersByName("public_swimming_pools")[0]
# create a object for district layer 
district_layer = QgsProject.instance().mapLayersByName("Muenster_City_Districts")[0]



# Getting all fields of the pool layer
pool_fields = pool_layer.fields()

# Getting access to the pool layer data provider
pool_provider = pool_layer.dataProvider() 

# Create new new column "district"
new_col = QgsField("district", QVariant.String, len = 50)

# Use the data provider to add the fields to the layer
pool_provider.addAttributes([new_col])

# User the method updateFields() to finally show them in the layer
pool_layer.updateFields()

# getting the fields again after the updating the pool layer
pool_fields = pool_layer.fields()


# Getting access to the layers capabilities
capabilities = pool_provider.capabilitiesString()

# Checking if the capabilty is part of the pool layer or not
if "Change Attribute Values" in capabilities:
    # if the layer can be modified then 

    # we iterate through all the features of pool layer
    for pool_feature in pool_layer.getFeatures():

        # Getting the id of the current feature
        pool_feature_id = pool_feature.id()

        # If the value of the current feature in the column "Type" has the value "H", we change it to "Hallenbad"
        if pool_feature["Type"] == "H":

            # Creating a dictionary with column and value to change
            pool_attributes = {pool_fields.indexOf("Type"):"Hallenbad"}

            # Use the changeAttributeValues method from the provider to process the attribute change for the specific feature id
            pool_provider.changeAttributeValues({pool_feature_id:pool_attributes})

        # but if the current feature in column "Type" has the value "F", we change it to "Freibad"    
        elif pool_feature["Type"] == "F":
            #applying the same process here but for value "F"
            pool_attributes = {pool_fields.indexOf("Type"):"Freibad"}
            pool_provider.changeAttributeValues({pool_feature_id:pool_attributes})
        else:
            pass
        
        # here we extract the geometry of the current feature of pool layer
        pool_geo = pool_feature.geometry()

        # Then we iterate through all the features of district layer
        for district_feature in district_layer.getFeatures():

            # extracting the geometry of the current feature of district layer
            district_geo = district_feature.geometry()

            # if the geometry of the current pool layer feature intersects with the current district layer feature
            if pool_geo.intersects(district_geo):
                # then we create a dictionary with column "district" and the value with be the current district name
                new_attribute = {pool_fields.indexOf("district"): district_feature.attribute("Name")}
                # using the pool_provider again to change the specific  pool feature ID
                pool_provider.changeAttributeValues({pool_feature_id:new_attribute})
                continue
    
    print("All relevant features are modified...")

else:
    print("Feature of the swimming pool layer can't be modified")








