# importing main libraries
import arcpy
import os
# parameters
arcpy.env.workspace = r"E:\Uni-Muenster\SoSe_2025\Python_with_QGIS_and_ArcGIS\Week_10\arcpy_2.gdb"
arcpy.env.overwriteOutput = True
# existing bus layer
bus_stops = r"E:\Uni-Muenster\SoSe_2025\Python_with_QGIS_and_ArcGIS\Week_10\arcpy_2.gdb\stops_ms_mitte"
# #new path for the bus stops in Web Mercator but with a new name
bus_stops_3857 = r"E:\Uni-Muenster\SoSe_2025\Python_with_QGIS_and_ArcGIS\Week_10\arcpy_2.gdb\stops_ms_mitte_3857"
arcpy.management.Project(
    in_dataset=bus_stops,
    out_dataset=bus_stops_3857,
    out_coor_system=arcpy.SpatialReference(3857)  # Web Mercator
)
# this is our dynmaic point taking as an input
input_point = arcpy.GetParameterAsText(0)
# lets convert the input_point as well into Web Mercator projection
# in order to find the distance in meters
input_point_3857 = arcpy.management.Project(
    in_dataset=input_point,
    out_dataset="memory/input_point_3857",  # lets save it for temporye
    out_coor_system=arcpy.SpatialReference(3857)
)[0]
# now we can use the Near tool to find the nearest stop
arcpy.analysis.Near(
    in_features=input_point_3857,
    near_features=bus_stops_3857,
    search_radius="",
    location="LOCATION",
    method="PLANAR"
)
print('Analysis is done, point is created as well')
## time for the distance between new point and the nearest bus stops
# for that lets create a search cursor
with arcpy.da.SearchCursor(input_point_3857, ["NEAR_DIST", "NEAR_FID"]) as cursor:
    for row in cursor:
        distance = row[0]      
        bus_id = row[1]        
        break # we only have onepoint
# its time for the bus stop name ID
with arcpy.da.SearchCursor(bus_stops_3857, ["NAME"], f"OBJECTID = {bus_id}") as cursor:
    for row in cursor:
        bus_name = row[0]    
        break
# print(f"Distance between new point and nearest bus stop {bus_name} is {distance} meters")
arcpy.AddMessage(f"Distance: {distance} Meters")  
arcpy.AddMessage(f"Name of the Bus Stop: {bus_name}")  
