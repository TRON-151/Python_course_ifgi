# first the libraries
import os
import arcpy

# next workspace
arcpy.env.workspace = r'C:\Users\ousam\Downloads\exercise_arcpy_1.gdb'

# listing all the feature classes of the workspace
fc_list = arcpy.ListFeatureClasses(feature_type='Point') # but only point feature
print(fc_list)

# path for the new output feature class active_assets
path = os.path.join(arcpy.env.workspace, 'active_assets')

# if it exists we will delete it
if arcpy.Exists(path):
    arcpy.Delete_management(path)


description = arcpy.Describe(fc_list[0])
spatial_ref = description.spatialReference
# lets create a new point feature class using the spatial reference from fc_list
arcpy.CreateFeatureclass_management(
    arcpy.env.workspace,
    'active_assets',
    'POINT',
    spatial_reference=spatial_ref
)

# fiels for the this new feature class
arcpy.AddField_management(path, 'name',   'TEXT')
arcpy.AddField_management(path, 'type',   'TEXT')
arcpy.AddField_management(path, 'status', 'TEXT')

# now ww will insert the acitve records using an InsertCursor
fields_output = ['SHAPE@', 'name', 'type', 'status']
with arcpy.da.InsertCursor(path, fields_output) as icur:
    # iterating over each point feature
    for point in fc_list:

        # using a search cursor to get the fields we need
        fields_input = ['SHAPE@', 'type', 'status']
        with arcpy.da.SearchCursor(point, fields_input) as scur:
            for shape, typ, status in scur:

                # we will check if the status is active or not
                if status and status.lower() == 'active':
                    icur.insertRow((shape, point, typ, status))

# now lets introduce some buffer zone

# buffer values for different types
buff_val = {
    'mast': 300,
    'mobile_antenna': 50,
    'building_antenna': 100
}
# path for the new output feature class buffer_zone
buffered_path = os.path.join(arcpy.env.workspace, 'buffer_zone')

# before proceeding lets delete the existing one:
if arcpy.Exists(buffered_path):
    arcpy.Delete_management(buffered_path)

# now we add a new field for buffer distance with dtype double
arcpy.AddField_management(path, 'buffere_dist', 'DOUBLE')

# 
with arcpy.da.UpdateCursor(path, ['type', 'buffere_dist']) as ucur:
    for typ, _ in ucur:
        dist = buff_val.get(typ, 0)
        ucur.updateRow((typ, dist))
        
# path for the new output feature class buffer_zone
buffered_path = os.path.join(arcpy.env.workspace, 'buffer_zone')

arcpy.Buffer_analysis(
    in_features=path,
    out_feature_class=buffered_path,
    buffer_distance_or_field='buffere_dist',
    line_side ='FULL',
    line_end_type='ROUND',
    dissolve_option='ALL'
)