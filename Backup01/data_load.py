import os
import json

os.chdir("C:\\0_Python\dap-api-test\\")
# print(os.getcwd())

filename = 'UnitsDict04.json'    #Create string variable for filename

with open(filename, 'r') as file:      # Open connection to file, read only
    unitsListing = json.load(file)

# value = unitsList[143]

# print(value)

for entry in unitsListing:
    
    value = (entry['name'], entry['defString'])
    if entry['convCoefficient'] == 1:
        print(value)

# value = t_dict['color']['red'].value
# print(value)

units_dict = {
        'E': [(0.5, 2), ('kg', 1), ('v', 2)],
        'v': [(5, 1), ('m', 1), ('s', -1)],
        'kh': [('E', 1), ('kg', 2)]
        }

# FUNCTION DEFINITIONS
def all_SIBU(unit_list):

    SIBU_list = ('kg', 'm', 's')
    
    all_SIBU = True
    for unit, degree in unit_list:

        unit_is_number = isinstance(unit, int) or isinstance(unit, float)

        if not unit_is_number and unit not in SIBU_list:
            all_SIBU = False
            print(unit, all_SIBU)

    return all_SIBU

def base_step(unit_list):

    if all_SIBU(unit_list):
        print("this is all SIBU")
        base_step = unit_list
        print(base_step)

    else:
        print("This needs to be iterated")
    
    return base_step

# MAIN CODE

target_list = base_step(units_dict['v'])
print(target_list)