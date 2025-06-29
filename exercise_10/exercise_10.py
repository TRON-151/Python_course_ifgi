# importing main libraries
import arcpy
import os

# parameters

arcpy.env.workspace = r"E:\Uni-Muenster\SoSe_2025\Python_with_QGIS_and_ArcGIS\Week_10\arcpy_2.gdb"
arcpy.env.overwriteOutput = True

# lets create a point in the workspace first
# lets give coordinates near to the Münster city but in meterss
x,y = 843277.13, 6795167.20

point = arcpy.Point(x, y)

our_point = "our_point" # name of the point feature

# we will use 3857 spatial reference for Web Mercator Projection
spatial_ref = arcpy.SpatialReference(3857) # Web Mercator
arcpy.management.CreateFeatureclass(
    arcpy.env.workspace,
    our_point,
    "POINT",
    spatial_reference=spatial_ref
)

# our point fields now:
arcpy.management.AddField(
    our_point,
    "Name",
    "TEXT"
)

# lets add this point to the workspace
with arcpy.da.InsertCursor(our_point, ["SHAPE@", "Name"]) as cursor:
    cursor.insertRow([point, "Test Point"])

# test point layer   
test_point = r"E:\Uni-Muenster\SoSe_2025\Python_with_QGIS_and_ArcGIS\Week_10\arcpy_2.gdb\our_point"
# existing bus layer
bus_stops = r"E:\Uni-Muenster\SoSe_2025\Python_with_QGIS_and_ArcGIS\Week_10\arcpy_2.gdb\stops_ms_mitte"



# But for the Near tool, we need Web Mercator projection in order to get the distance in meters
# so, we will reproject the bus stop layer as Web mercator projections

# #new path for the bus stops in Web Mercator but with a new name
bus_stops_3857 = r"E:\Uni-Muenster\SoSe_2025\Python_with_QGIS_and_ArcGIS\Week_10\arcpy_2.gdb\stops_ms_mitte_3857"
arcpy.management.Project(
    in_dataset=bus_stops,
    out_dataset=bus_stops_3857,
    out_coor_system=arcpy.SpatialReference(3857)  # Web Mercator
)

# now we can use the Near tool to find the nearest stop
arcpy.analysis.Near(
    in_features=test_point,
    near_features=bus_stops_3857,
    search_radius="",
    location="LOCATION",
    method="PLANAR"
)

print('Analysis is done, point is created as well')


## time for the distance between new point and the nearest bus stops
# for that lets create a search cursor
with arcpy.da.SearchCursor(test_point, ["NEAR_DIST", "NEAR_FID"]) as cursor:
    for row in cursor:
        distance = row[0]      
        bus_id = row[1]        
        break # we only have onepoint

# its time for the bus stop name ID
with arcpy.da.SearchCursor(bus_stops_3857, ["NAME"], f"OBJECTID = {bus_id}") as cursor:
    for row in cursor:
        bus_name = row[0]    
        break

print(f"Distance between new point and nearest bus stop {bus_name} is {distance} meters")
# print(bus_name)