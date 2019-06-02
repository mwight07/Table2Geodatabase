
# coding: utf-8

# In[9]:


# Script: Table_to_GDB_FC.py
# Author: Matthew Wight

# Code Description: Coding: utf-8
"""
Script to automate conversion of a CSV file to both a table and a geodatabase feature 
class with WGS84 spatial reference. Script is used to periodically load spreadsheet 
data into an ArcSDE database. When used with a web-based spreadsheet template 
(containing "DD_LON" and "DD_LAT" fields) this allows spreadsheet users to automatically 
generate updates for live maps.
"""


#-----------------------------------------------------------------------------------------  
# 1.0 - Import system modules
#----------------------------------------------------------------------------------------- 

print('Step 1.0 - Import system modules:')
print('   -- Executing...')

import arcpy
from arcpy import env
import glob
import sys
import os


print('   -- Process complete. Check for errors and move to next cell.')
print(' ')


#-----------------------------------------------------------------------------------------  
# 2.0 - Set path variables
#----------------------------------------------------------------------------------------- 

print('Step 2.0 - Set path variables: ')
print('   -- Executing...')

env.workspace = r"C:\Users\Matt\ESRI_Jupyter\Table2GDB"     # Folder path
working_dir = r"C:\Users\Matt\ESRI_Jupyter\Table2GDB"       # Folder path
out_folder_path = r"C:\Users\Matt\ESRI_Jupyter\Table2GDB"   # Out folder path

csv_name = "test1.csv"                                      # Input file name and extension
gdb_fc_name = "test4"                                       # Set .gdb feature class name
out_gdb_name = "test_fc4.gdb"                               # Set .gdb name

suffix = '.gdb'                                             # File suffix type
outLocation = os.path.join(out_folder_path, out_gdb_name)   # Create .gdb file path
gdb = outLocation                                           # Set .gdb value

prefix = ""        # leave empty if using file gdb; otherwise give SDE table prefix string


print('   -- Process complete. Check for errors and move to next cell.')
print(' ')


#-----------------------------------------------------------------------------------------  
# 3.0 - Execute CreateFileGDB in immediate mode

print('Step 3.0 - Execute CreateFileGDB...')
print('   -- Executing...')

arcpy.CreateFileGDB_management(out_folder_path, out_gdb_name)


print('   -- Process complete. Check for errors and move to next cell.')
print(' ')


#-----------------------------------------------------------------------------------------  
# 4.0 - Make list of all tables in workspace
#----------------------------------------------------------------------------------------- 

# List of tables should be similar to this: ["test1.csv", "test2.dbf"]
print('Step 4.0 - Make list of tables in workspace ...')
print('   -- Executing...')

tables = arcpy.ListTables()
print('   -- Tables: ', tables)


print('   -- Process complete. Check for errors and move to next cell.')
print(' ')


#-----------------------------------------------------------------------------------------  
# 5.0 - Execute TableToGeodatabase
#----------------------------------------------------------------------------------------- 

print('Step 5.0 - Execute TableToGeodatabase: ')
print('   -- Executing...')

try: 
    print('   -- Importing tables to gdb: ' + outLocation)
    arcpy.TableToGeodatabase_conversion(csv_name, outLocation)
except:
    print(arcpy.GetMessages())

    
print('   -- Process complete. Check for errors and move to next cell.')
print(' ')


#-----------------------------------------------------------------------------------------  
# 6.0 - Convert Table to Feature Class
#----------------------------------------------------------------------------------------- 

print('Step 6.0 - Convert Table to Feature Class...')
print('   -- Executing...')

arcpy.env.workspace = working_dir
arcpy.env.overwriteOutput = True

xy_table = csv_name
x_field = "DD_LON"
y_field = "DD_LAT"
spatial_ref = arcpy.SpatialReference()
spatial_ref.factoryCode = 4326    #WGS84
spatial_ref.create()


arcpy.MakeXYEventLayer_management(xy_table, x_field, y_field, "new", spatial_ref)

# Check for existing feature class; 'archive' if present
arcpy.env.workspace = gdb
fclist = arcpy.ListFeatureClasses()

if "{prefix}{name}".format(prefix = prefix, name = gdb_fc_name) in fclist:
    arcpy.CopyFeatures_management("{0}".format(gdb_fc_name), "{0}_old".format(gdb_fc_name))
    arcpy.Delete_management(gdb_fc_name)

#arcpy.env.workspace = working_dir
arcpy.FeatureClassToFeatureClass_conversion("new", gdb, gdb_fc_name)


print('   -- Process complete. Check for errors and move to next cell.')
print(' ')


#-----------------------------------------------------------------------------------------
print(' ')
print('All steps complete. Check for any errors or missing data in final output.')
print(' ')
#-----------------------------------------------------------------------------------------


# In[2]:


# Convert entire notebook to python script
get_ipython().system('jupyter nbconvert --to script Table2GDB_FC.ipynb')

