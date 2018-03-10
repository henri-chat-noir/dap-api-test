units_dict = {
    'kh': [('E', 3), ('kg', 2), ('v', 4)],
    'E': [(0.5, 2), ('kg', 1), ('v', 2)],
    'v': [(5, 1), ('m', 1), ('s', -1)]

    }

# FUNCTION DEFINITIONS
    
def is_SIBU(unit):
    # Function simply test a single unit letter to see if in SIBU list, ignoring integers or floats
    
    SIBU_list = ('kg', 'm', 's')
    
    is_SIBU = True
    unit_is_number = isinstance(unit, int) or isinstance(unit, float)

    if not unit_is_number and unit not in SIBU_list:
        is_SIBU = False
        # print(unit, is_SIBU)

    return is_SIBU

def all_SIBU(unit_list):
    # This function tests all arguments in a list to see if unit letters are SIBU

    all_SIBU = True
    for unit, degree in unit_list:

        if not is_SIBU(unit):
            all_SIBU = False

    return all_SIBU

def base_step(arg_list, units_dict):
    # The purpose of this function is to swap-in a single argument (with a non-SIBU unit) with replacement arguments
    # where the degrees in the replacement are affected by the degree of the argument being replaced

    for arg in arg_list:

        unit = arg[0]
        degree = arg[1]
        
        if is_SIBU(unit):
            print("done with this argument")
            
            # base_step = unit_list
            # print(base_step)
        
        else:
            
            print("This argument needs to be base-stepped, since it has this unit:", unit )
            print("Current argument list: ", arg_list)
            
            # Start by clearing the offending argument out of argument list
            arg_list.remove(arg)
            print("This is arg list after argument removed: ", arg_list)

            # This is key bit.  Replacement argument list is returned by looking into dictionary for letter = unit
            rep_arg_list = units_dict[unit]
            print("The is replacement arg list from dictionary, i.e. prior to degree adjustment: ", rep_arg_list)
            
            # This for loop builds a set of tuples consistent with rep_arg_list, but where degrees multiplied by degree
            # from the argument that is being replaced (and already cleared from arg_list
            new_args = []
            for rep_arg in rep_arg_list:
                rep_unit = rep_arg[0]
                rep_degree = degree * rep_arg[1]   
                rep_tuple = (rep_unit, rep_degree)
                new_args.append(rep_tuple)

            # On this side of else, i.e. when non SIBU, arg list simple returned with new_args added
            # (noting argument cleared earlier in function
            arg_list = arg_list + new_args
            print("This is revised arguments list:", arg_list)
           
        base_step = arg_list 

    return base_step

def simplify(arg_list):

    unit_list = []
    
    for unit, degree in arg_list:

        if unit not in unit_list:
            unit_list.append(unit)  
    
    simplify = []
    for unique_unit in unit_list:
        
        comb_degree = 0
        for unit, degree in arg_list:

            if unit == unique_unit:
                comb_degree = comb_degree + degree
            
        simplify.append( (unique_unit, comb_degree) )

    return simplify


# MAIN CODE

target_list = base_step(units_dict['kh'], units_dict)
print("Just before while: ", target_list)


while not all_SIBU(target_list):
    
    target_list = base_step(target_list, units_dict)
   
simplified_list = simplify(target_list)   
  
print("This was target list for simplification: ", target_list)
print("Here is the simplified list:", simplified_list)