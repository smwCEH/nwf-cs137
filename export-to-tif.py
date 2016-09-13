import os
import sys
import platform
import datetime
import time
import random
import json
import collections


import arcpy


# Capture start_time
start_time = time.time()


def hms_string(sec_elapsed):
    """Function to display elapsed time

    Keyword arguments:
    sec_elapsed -- elapsed time in seconds
    """
    h = int(sec_elapsed / (60 * 60))
    m = int((sec_elapsed % (60 * 60)) / 60)
    s = sec_elapsed % 60.
    return "{0}:{1:>02}:{2:>05.2f}".format(h, m, s)


# Print Python version, version info, and platform architecture
print('\n\nsys.version:\t\t\t\t\t{0}'.format(sys.version))
print('sys.versioninfo:\t\t\t\t{0}'.format(sys.version_info))
print('platform.architecture():\t\t{0}'.format(platform.architecture()))


# Print script filename, start date and time
script = os.path.basename(__file__)
print('\n\nStarted {0} at {1} on {2}...'.format(script,
                                                datetime.datetime.now().strftime('%H:%M:%S'),
                                                datetime.datetime.now().strftime('%Y-%m-%d')))


# Define NODATA value
NODATA = -9999.0000


# Define DEFAULT value as None
DEFAULT = None


# Set arcpy overwrite output to True
arcpy.env.overwriteOutput = True
# print('\n\narcpy Environment variables:')
# environments = arcpy.ListEnvironments()
# for environment in environments:
#     print('\t{0:<30}:\t{1}'.format(environment, arcpy.env[environment]))


# Define CORPADMIN ArcSDE connection file
arcsde_corpadmin = r'C:\Users\SMW\AppData\Roaming\ESRI\Desktop10.1\ArcCatalog\Connection to LADB CEHCORP CORPADMIN.sde'
print('\n\narcsde_corpadmin:\t\t{0}'.format(arcsde_corpadmin))


# Define CORPADMIN ArcSDE user
arcsde_corpadmin_user = r'CORPADMIN'
print('arcsde_corpadmin_user:\t\t{0}'.format(arcsde_corpadmin_user))


# Define NWF raster catalog
raster_catalog = r'NWF_Cs137_Total'
raster_catalog = arcsde_corpadmin + '\\' + arcsde_corpadmin_user + '.' + raster_catalog
print('\n\nraster_catalog:\t\t{0}'.format(raster_catalog))


print('\n\narcpy.Exists({0}:\t\t{1}'.format(raster_catalog,
                                            arcpy.Exists(raster_catalog)))


# Define out folder
out_folder = r'F:\Radioecology\NWFCs-137\eidc-data-deposit\c3e530bf-af20-43fc-8b4b-92682233ff08'
print('\n\nout_folder:\t\t{0}'.format(out_folder))


# arcpy.da.SearchCursor
print('\n')
field_names = ['OBJECTID', 'NAME', 'QUARTERDATE']
where_clause=''
for row in sorted(arcpy.da.SearchCursor(in_table=raster_catalog,
                                        field_names=field_names)):
    print('\tOBJECTID:\t{0}\t\tNAME:\t{1}'.format(row[0], row[1]))
    #
    in_raster = raster_catalog + '/Raster.OBJECTID={0}'.format(row[0])
    print('\t\tin_raster:\t\t{0}'.format(in_raster))
    out_rasterdataset = os.path.join(out_folder, row[1] + '.tif')
    print('\t\tout_rasterdata:\t\t{0}'.format(out_rasterdataset))
    #
    if arcpy.Exists(out_rasterdataset):
        arcpy.Delete_management(out_rasterdataset)
    #
    arcpy.CopyRaster_management(in_raster=in_raster,
                                out_rasterdataset=out_rasterdataset,
                                config_keyword='',
                                background_value='',
                                nodata_value=NODATA,
                                onebit_to_eightbit='NONE',
                                colormap_to_RGB='NONE',
                                pixel_type='32_BIT_FLOAT',
                                scale_pixel_value='NONE',
                                RGB_to_Colormap='NONE',
                                format='TIFF',
                                transform='NONE')
del row


# Capture end_time
end_time = time.time()


# Report elapsed_time (= end_time - start_time)
print('\n\nIt took {0} to execute this.'.format(hms_string(end_time - start_time)))


# Print script filename, finish date and time
print('\n\nFinished {0} at {1} on {2}.\n'.format(script,
                                                 datetime.datetime.now().strftime('%H:%M:%S'),
                                                 datetime.datetime.now().strftime('%Y-%m-%d')))
