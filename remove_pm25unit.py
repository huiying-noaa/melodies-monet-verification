import sys
from netCDF4 import Dataset

# Open the netCDF file in write mode
fn=sys.argv[1]
print("Remove units of pm25 in "+ fn)
nc_file = Dataset(fn, 'r+')

# Remove a global attribute
#if 'global_attribute' in nc_file.ncattrs():
#    del nc_file.global_attribute

# Get a variable
variable = nc_file.variables['pm25']

# Remove a variable attribute
if 'units' in variable.ncattrs():
    del variable.units

# Close the netCDF file
nc_file.close()
