import processing

# Specify the input parameters for the viewshed analysis
input_layer = '/Users/adrianwidlak/Downloads/multiprocessing/zlaczone_krk.tif'
observer_points = '/Users/adrianwidlak/Downloads/multiprocessing/observer_points.shp'
output_file = '/Users/adrianwidlak/Downloads/multiprocessing/zlaczone_krk.tif/combined_viewshed.tif'

# Load the observer points as a QgsVectorLayer
observer_layer = QgsVectorLayer(observer_points, 'Observer Points', 'ogr')

# Initialize the combined viewshed raster
combined_viewshed = None

# Iterate over each observer point
for feature in observer_layer.getFeatures():
    # Get the observer point geometry
    observer_geometry = feature.geometry()

    # Run the viewshed algorithm for the current observer point
    parameters = {'INPUT': input_layer,
                  'OBSERVER': observer_geometry,
                  'VISIBILITY': 1,
                  'TARGET_DISTANCE': 0,
                  'OUTPUT': 'TEMPORARY_OUTPUT'}
    result = processing.run("gdal:viewshed", parameters)

    # Retrieve the viewshed output raster
    viewshed_raster = result['OUTPUT']

    # Combine the viewshed with the previous outputs using addition
    if combined_viewshed is None:
        combined_viewshed = QgsRasterLayer(viewshed_raster)
    else:
        combined_viewshed.startEditing()
        combined_viewshed.dataProvider().addRasterLayer(viewshed_raster, 'TEMP_LAYER')
        combined_viewshed.mergeEditBuffer()
        combined_viewshed.commitChanges()

# Save the final combined viewshed raster to a file
combined_viewshed.dataProvider().clone().writeToFile(output_file)

# Refresh the QGIS layer registry to update the layer list
QgsProject.instance().layerTreeRoot().refresh()