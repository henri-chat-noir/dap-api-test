units_dict = {
        'E': [(0.5, 2), ('kg', 1), ('v', 2)],
        'v': [(5, 1), ('m', 1), ('s', -1)],
        'kh': [('E', 1), ('kg', 2)]
        }

import functionsJR as fJR

# MAIN CODE

target_list = fJR.base_step(units_dict['v'])
print(target_list)