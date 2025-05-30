"""
***************************************************************************
*                                                                         *
*   This program is free software; you can redistribute it and/or modify  *
*   it under the terms of the GNU General Public License as published by  *
*   the Free Software Foundation; either version 2 of the License, or     *
*   (at your option) any later version.                                   *
*                                                                         *
***************************************************************************
"""

from qgis.PyQt.QtCore import QCoreApplication
from qgis.core import (QgsProcessing,
                       QgsFeatureSink,
                       QgsProcessingException,
                       QgsProcessingAlgorithm,
                       QgsProject,
                       QgsVectorLayer,
                       QgsDistanceArea,
                       QgsFeatureRequest,
                       QgsProcessingParameterFeatureSource,
                       QgsProcessingParameterFeatureSink,
                       QgsProcessingParameterFileDestination,
                       QgsProcessingParameterEnum)
from qgis import processing
import os
import time
from qgis.utils import iface 
from PyQt5.QtWidgets import QMessageBox 



class create_city_district_profile(QgsProcessingAlgorithm):
    """
    This is an example algorithm that takes a vector layer and
    creates a new identical one.

    It is meant to be used as an example of how to create your own
    algorithms and explain methods and variables used to do it. An
    algorithm like this will be available in all elements, and there
    is not need for additional work.

    All Processing algorithms should extend the QgsProcessingAlgorithm
    class.
    """

    # Constants used to refer to parameters and outputs. They will be
    # used when calling the algorithm from another algorithm, or when
    # calling from the QGIS console.


    # lets make some variable for user input 
    district_in = 'District'
    Pool_or_School = 'Pools or Schools'
    Storage_path = 'Storage path for output'

    def tr(self, string):
        """
        Returns a translatable string with the self.tr() function.
        """
        return QCoreApplication.translate('Processing', string)

    def createInstance(self):
        return create_city_district_profile()

    def name(self):
        """
        Returns the algorithm name, used for identifying the algorithm. This
        string should be fixed for the algorithm, and must not be localised.
        The name should be unique within each provider. Names should contain
        lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return 'create_city_district_profile'

    def displayName(self):
        """
        Returns the translated algorithm name, which should be used for any
        user-visible display of the algorithm name.
        """
        return self.tr('Create_city_district_profile')

    def group(self):
        """
        Returns the name of the group this algorithm belongs to. This string
        should be localised.
        """
        return self.tr('group 3')

    def groupId(self):
        """
        Returns the unique ID of the group this algorithm belongs to. This
        string should be fixed for the algorithm, and must not be localised.
        The group id should be unique within each provider. Group id should
        contain lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return 'group 3'

    def shortHelpString(self):
        """
        Returns a localised short helper string for the algorithm. This string
        should provide a basic description about what the algorithm does and the
        parameters and outputs associated with it..
        """
        return self.tr("This algorithm will take your choice of district, option of pool or school and calculates some different varieties of information, then output it in the form of pdf report")


    

    def initAlgorithm(self, config=None):
        """
        Here we define the inputs and output of the algorithm, along
        with some other properties.
        """

        # We add the input vector features source. It can have any kind of
        # geometry.
        # the first parameter Name of the district
        self.addParameter(
            QgsProcessingParameterFeatureSource(
                self.district_in, 
                self.tr('Choose District'),
                self.sort_district(),
                defaultValue= "No District selected yet",
                optional= False
            )
        )
        # this parameter is for the option of pools or schools
        self.addParameter(
            QgsProcessingParameterFeatureSink(
                self.Pool_or_School,
                self.tr('Which information do you want to include in PDF?'),
                ["Public_Swimming_Pools","Schools"],
                defaultValue= "Not selected yet",
                optional=False
            )
        )
        # this parameter is to get the path but with filter of pdf only
        self.addParameter(
            QgsProcessingParameterFeatureSink(
                self.Storage_path,
                self.tr('Storage path for the output PDF?'),
                fileFilter = "PDF files (.PDF)"
            )
        )

    ############ custom methods here ###########

    # lets create a method to sort the district layer features in alphabetic order for input
    def sort_district(self):
        # this is district layer 
        district_layer = QgsProject.instance().mapLayersByName("Muenster_City_Districts")[0]
        request = QgsFeatureRequest()

        # now lets order it by Name of the district
        name = QgsFeatureRequest.OrderByClause("Name", ascending = True)
        order = QgsFeatureRequest.OrderBy([name])
        # now lets set this order for features
        request.setOrderBy(order)
        # now we will get the features in a alphabatic order by "Name" attribute in a list
        district_list = []
        for feature in district_layer.getFeatures(request):
            district_list.append(feature.attribute('Name'))
        
        # and we return the district_list
        return(district_list)
    
    # this method is to select the district among the others 
    def choose_district(self, district_name):
        dist = QgsProject.instance().mapLayersByName("Muenster_City_District")[0]
        show = f"\"Name\" = '{district_name}'"
        dist.selectedByExpression(show, QgsVectorLayer.SetSelection)
        
        choosen_district = dist.selectedFeatures()[0]

        return choosen_district
    
    # this method is the area of above district 
    def area_dist(self, district):
        
        dist = self.choose_district(district)
        # lets get the ellipsoid and crs of that this dist
        distance = QgsDistanceArea()
        distance.setEllipsoid("ETRS89")
        distance.setSourceCrs(QgsProject.instance().crs(), QgsProject.instance().transformContext())

        # taking geometry
        geometry = dist.geometry()
        area = distance.measureArea(geometry)

        # and return the area
        return(area)
    
    # this methods counts the no. of house hold which are in the selected district
    def count_households(self, district):

        dist = self.choose_district(district)
        household_layer = QgsProject.instance().mapLayersByName("House_Numbers")[0]

        count = 0
        #lets count the households which intersects with the selected district
        dist_geometry = dist.geometry()
        for feature in household_layer.getFeatures():
            # if the point of house exists inside the selected district then we count
            if dist_geometry.contains(feature.geometry()):
                count += 1
        
        return count
    
    # this methods is like the previous one but it counts the no. of parcels in the selected district
    def count_parcels(self, district):
        dist = self.choose_district(district)
        parcel_layer = QgsProject.instance().mapLayersByName("Muenster_Parcels")[0]

        count = 0
        #lets count the parcel which intersects with the selected district
        dist_geometry = dist.geometry()
        for feature in parcel_layer.getFeatures():
            # if the parcel instersects with the selected district then we count
            if dist_geometry.intersects(feature.geometry()):
                count += 1
        
        return count
    
    # now we count the no. of schools or the pools in the selected district
    def count_pool_or_school(self, district, choice):
        dist = self.choose_district(district)

        if choice == "pools":
            # then we take swimming pool layer
            pools_layer = QgsProject.instance().mapLayersByName("public_swimming_pools")[0]

            # we do the same thing again to count the pools in the selected district:
            count = 0
            #lets count the pools which intersects with the selected district
            dist_geometry = dist.geometry()
            for feature in pools_layer.getFeatures():
                # if the point of pools intersects with the selected district then we count
                if dist_geometry.intersects(feature.geometry()):
                    count += 1
            return count
        
        # else the choice will be schools so we count the schools then
        else:
            schools_layer = QgsProject.instance().mapLayersByName("Schools")[0]
            # we do the same thing again to count the schools in the selected district:
            count = 0
            #lets count the parcel which intersects with the selected district
            dist_geometry = dist.geometry()
            for feature in schools_layer.getFeatures():
                # if the point of parcel intersects with the selected district then we count
                if dist_geometry.intersects(feature.geometry()):
                    count += 1
            return count

    # this method to create the map:
    def map(self, district):

        #select the district and zoom to the feature
        districts = QgsProject.instance().mapLayersByName("Muenster_City_Districts")[0]
        district = self.choose_district(district)
        bbox = districts.boundingBoxOfSelected()
        iface.mapCanvas().setExtent(bbox)
        iface.mapCanvas().refresh()

        #set processing to sleep for 10 seconds so the zoom has enough time
        time.sleep(10)

        # Create output path for the image in project directory
        path = os.path.join(QgsProject.instance().homePath(), "image.png")
        iface.mapCanvas().saveAsImage(path)

        
        return path
    
    # last method to create the pdf doc
    def create_pdf(self, pdf_output, district_name, parent, area, household_number, parcels, schools_or_pools, schools_or_pools_number, picture_path):
        from reportlab.pdfgen import canvas
        from reportlab.lib.pagesizes import letter
        from reportlab.pdfgen import canvas
        from reportlab.lib.styles import getSampleStyleSheet
        from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Image
        from reportlab.lib.units import inch

        
        #create texts and image objects to insert in the pdf later
        doc = SimpleDocTemplate(pdf_output, pagesize=letter)

        content = []
        styles = getSampleStyleSheet()
        #texts
        Title = Paragraph(f"<b>District Report for {district_name}</b>", styles["Title"])
        parent_text = Paragraph(f"Parent District: {parent}", styles["Normal"])
        area_text = Paragraph(f"Size: {area} square kilometers", styles["Normal"])
        household_text = Paragraph(f"Number of Housholds: {household_number}", styles["Normal"])
        parcels_text =Paragraph(f"Number of Parcels {parcels}", styles["Normal"])
        schools_or_pools_text = Paragraph(f"Number of {schools_or_pools}: {schools_or_pools_number}", styles["Normal"])
        
        #images
        map = Image(picture_path, 4*inch, 4*inch)
        diagramm = Image(self.plot_type_distribution(self.count_feature_types(schools_or_pools, district_name)), 4*inch, 3*inch)
        


        #append the content to the story list the order of append is important for the order in the pdf 
        content.append(Title)
        content.append(Spacer(1, 12))
        content.append(parent_text)
        content.append(area_text)
        content.append(household_text)
        content.append(parcels_text)
        content.append(schools_or_pools_text)
        content.append(Spacer(1, 12))
        content.append(map)

        doc.build(content)
        
        
        return pdf_output

    ################################################

    # this is the main algorithm 
    def processAlgorithm(self, parameters, context, feedback):
        """
        Here is where the processing itself takes place.
        """

        #first lets the option for the different districts
        districts = self.parameterAsInt(parameters, self.district_in, context)
        district = self.sort_district()[districts]

        #then the choice between pools or schools
        option = self.parameterAsEnum(parameters, self.Pool_or_School, context)
        # now storage path
        path = self.parameterAsFileOutput(parameters, self.Storage_path, context)

        if option == 0:
            choice = 'pools'
        else:
            choice = 'schools'    


        # variables for the output in the pdf file
        size = self.area_dist(district) # area of the dist
        p_dist = self.choose_district(district)["P_District"] # parent of that dist
        household = self.count_households(district)
        parcels = self.count_parcels(district)
        pool_or_school_numbers = self.count_pool_or_school(district, choice)
        map = self.map(district)

        # last we create a pdf
        pdf_path = self.create_pdf(path, district, p_dist, size, household, parcels, choice, pool_or_school_numbers, map)
        return {self.Storage_path: pdf_path}
