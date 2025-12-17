import numpy as np
from Plant import Plant
from Map import Plantmap, Shademap, Watermap
from Environment import Environment

# define the main function
def main():
    print("test")

    # plant without neighbors, height 1.0, mass 1.0, wtd 0.5, shade 0.0, location 0.0
    testplant = Plant(init_height=1.0, init_mass = 1.0, init_local_water_table_depth=0.5, init_local_shade_value=0.0, location=(0,0))

    width_plants = 5
    height_plants = 5

    environment = Environment(width_map = width_plants, height_map = height_plants)

    # NOTE: The creation of an Environment and the Setup of Maps is working. Still in need to define the plant objects and the values for Shade and Water-table depth in detail

    print("DONE so far")
    print('\n BEGIN TESTPLANT procedure \n')

    # Here I want to test all the growth mechanisms of a plant in the Plantmap of environment
    # add Environment to this plant AND 
    # add growth mechanisms to the plant
    testplant.add_Environment(environment=environment)
    print('\n Ended environment ADDING \n')

    stats_before_growth = testplant.report_stats()
    print(f'Before growth: \n {stats_before_growth} \n ')
    
    # set a single plant at the 0/0 position
    environment.get_plantmap().set_single_item_at(testplant, testplant.get_location())
    print('\n Ended testplant EMBEDDING in environment\n')
    
    # Try to grow the testplant
    environment.get_plantmap().get_items()[0][0].grow_step()

    stats_after_growth = testplant.report_stats()
    print(f'After growth: \n {stats_after_growth} \n ')
    print('\n Ended testplant GROWING \n')
# 
if __name__ == '__main__':
    main()