import arcpy
class ToolValidator:
  # Class to add custom behavior and properties to the tool and tool parameters.

    def __init__(self):
        # Set self.params for use in other validation methods.
        self.params = arcpy.GetParameterInfo()

    def initializeParameters(self):
        # Customize parameter properties. This method gets called when the
        # tool is opened.
        return

    def updateParameters(self):
        # Modify the values and properties of parameters before internal
        # validation is performed.


        # first lets store the parameters values in a variable
        stops_parm = self.params[1]
        field_parm = self.params[2]
        value_parm = self.params[3]

        # Populate filter_value dropdown when name_field is selected
        if field_parm.value:
             stops = stops_parm.valueAsText
             field = field_parm.valueAsText

             # now we will get the unique values 
             unique_val = {row[0] for row in arcpy.da.SearchCursor(stops,[field])}
             
             # now we will set the filter_value drop down
             value_parm.filter.list = sorted(unique_val)

        return

    def updateMessages(self):
        # Modify the messages created by internal validation for each tool
        # parameter. This method is called after internal validation.
        return

    # def isLicensed(self):
    #     # Set whether the tool is licensed to execute.
    #     return True

    # def postExecute(self):
    #     # This method takes place after outputs are processed and
    #     # added to the display.
    #     return


    