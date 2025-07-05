# importing main libraries
import arcpy
import os
import time


# first we get the parameters from the user the we start the script
new_point = arcpy.GetParameterAsText(0) 
fc_to_evaluate_against = arcpy.GetParameterAsText(1)
name_field = arcpy.GetParameterAsText(2)  
value_field = arcpy.GetParameterAsText(3) 

# lets setup the progressor 
arcpy.SetProgressor(type='step',message='Progress in my Script',min_range=0, max_range=4,step_value=1)
time.sleep(0.5)


######## FIRST #########

arcpy.SetProgressorLabel("Reprojecting your point...")
arcpy.SetProgressorPosition(1)
time.sleep(2) 

# now will first need to change the new point into Web Mercator projection
# so that we get the distnace in meters

new_point_3857 = arcpy.management.Project(
    in_dataset=new_point,       # we will give the dynamic new point
    out_dataset="memory/new_point_3857",    # and save it in memory
    out_coor_system=arcpy.SpatialReference(3857) # last the Web Mercator projection
)[0]

######## SECOND #########

arcpy.SetProgressorLabel("Filtering bus stops...")
arcpy.SetProgressorPosition(2)
time.sleep(2)

# lets specidfy the layer or the exact stop we want to evalute against

# stops_layer = "memory/filtered_stops"
sql = f"{name_field} = '{value_field}'"
arcpy.management.MakeFeatureLayer(
    in_features=fc_to_evaluate_against,
    out_layer="stops_layer",
    where_clause=sql
)

####### THIRD ########

arcpy.SetProgressorLabel("Calculating distance...")
arcpy.SetProgressorPosition(3)
time.sleep(2)

# now we will run the Near tool as we did in the 
# 10th exercise

arcpy.analysis.Near(
    in_features=new_point_3857,
    near_features="stops_layer",
    search_radius="",
    location="LOCATION",
    method="PLANAR"
)

# let get the distance from the new point to the nearest feature
with arcpy.da.SearchCursor(new_point_3857, ["NEAR_DIST"]) as cursor:
    for row in cursor:
        distance = row[0]
        break


####### FOURTH ########

arcpy.SetProgressorLabel("Your analysis is done...")
arcpy.SetProgressorPosition(4)
time.sleep(2)

arcpy.AddMessage(f"Distance: {distance:} Meters")
arcpy.AddMessage(f"Your Selected Stop: {value_field}")

# Clean up
arcpy.Delete_management("memory/input_point_3857")
# arcpy.Delete_management(stops_layer)