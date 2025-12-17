import numpy as np
from Plant import Plant
from Map import Plantmap, Shademap, Watermap
from Environment import Environment

# define the main function
def main():
    '''
    Here we want to test the growth mechanisms of a single Plant.
    Therefore a plant with 
    - height                            = 1.0 cm
    - initial mass                      = 1.0 mg
    - initial local water table depth   = 0.5 cm
    - shade value                       = 0.0

    is created.
    We execute growth steps to check proper working of multiple growth steps.
    '''

    print("Reproduction of Growth Experiment results from Hayward and Clymo, 1983")

    # plant without neighbors, height 1.0, mass 1.0, wtd 0.5, shade 0.0, location 0.0
    testplant = Plant(init_height=1.0, init_mass = 1.0, init_local_water_table_depth=0.5, init_local_shade_value=0.0, location=(0,0))

    width_plants = 5
    height_plants = 5

    environment = Environment(width_map = width_plants, height_map = height_plants)

    # NOTE: The creation of an Environment and the Setup of Maps is working. Still in need to define the plant objects and the values for Shade and Water-table depth in detail

    print("DONE so far")
    print('\n BEGIN TESTPLANT procedure \n ################################################ \n')

    # Here I want to test all the growth mechanisms of a plant in the Plantmap of environment
    # add Environment to this plant AND 
    # add growth mechanisms to the plant
    testplant.add_Environment(environment=environment)
    print('\n Ended environment ADDING \n')

    stats_before_growth = testplant.report_stats()
    print(f'Before growth: \n {stats_before_growth} \n ')
    
    # Try to grow the testplant
    testplant.grow_step(print_params=True)

    stats_after_growth = testplant.report_stats()
    print(f'After growth: \n {stats_after_growth} \n ')
    print('\n Ended testplant GROWING for one step\n ################################################ \n')

    print("\n Begin several growth rates for a Single plant ...." )
    for i in range(77):
        # grow several times (equals average growth of one day)
        testplant.grow_step()

        # report growth status
        report = testplant.report_stats()

        # Print the current stats
        print(f"\n Stats after {i+1}. step of growth: \n {report}")

# 
if __name__ == '__main__':
    main()