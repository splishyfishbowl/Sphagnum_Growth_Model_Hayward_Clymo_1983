import numpy as np
from Plant import Plant
from Map import Plantmap, Shademap, Watermap
from Environment import Environment

# define the main function
def main():
    print("Reproduction of Growth Experiment results from Hayward and Clymo, 1983")

    # plant without neighbors, height 1.0, mass 1.0, wtd 0.5, shade 0.0, location 0.0
    testplant = Plant(init_height=1.0, init_mass = 1.0, init_local_water_table_depth=0.5, init_local_shade_value=0.0, location=(0,0))

    width_plants = 5
    height_plants = 5

    # create environment object according to paper
    environment = Environment(width_map = width_plants, height_map = height_plants, init_mode_height='NORM_DIST', mean_height=0.0, std=0.5)

    # NOTE: The creation of an Environment and the Setup of Maps is working. Still in need to define the plant objects and the values for Shade and Water-table depth in detail
    print('\n BEGIN TESTPLANT procedure \n')

    # access one plant in environment, let it report
    testplant_created_in_environment = environment.get_plant_at(0,1)
    
    # Here I want to test all the growth mechanisms of a plant in the Plantmap of environment
    # add Environment to this plant AND 
    # add growth mechanisms to the plant
    # testplant.add_Environment(environment=environment)
    print('\n Ended environment ADDING \n')

    # Track the growth data of the plants
    # for a individually created and added plant
    stats_before_growth = testplant.report_stats()
    print(f'Before growth (ADDED PLANT): \n {stats_before_growth} \n ')
    # For a default plant in environment (created by running set_up of Plantmap in Environment)
    stats_before_default_plant = testplant_created_in_environment.report_stats()
    print(f'Before growth (DEFAULT PLANT): \n {stats_before_default_plant} \n ')

    # make all plants except the testplant 2 cm high -> to investigate DL correct working
    plants = environment.get_plantmap().get_items()
    
    for i in range(5):
        for j in range(5):
            plant = plants[i][j]
            if isinstance(plant, Plant):
                # initial height is equal to 2 cm
                plant.set_height(2.0)
    
    # set a single plant at the 0/0 position
    environment.get_plantmap().set_single_item_at(testplant, testplant.get_location())
    
    # Add Environment to all plants in Plantmap
    environment.add_environment_to_plants_and_tell_neighbors()
    print('\n Ended testplant EMBEDDING in environment and Adding neighbors\n')
    
    # Try to grow the testplant
    # testplant.grow_step()
    # Try to grow all plants at once
    for i in range(5):
        environment.grow_all_plants(None, None)
        print(f'testplant.get_neighbors_impact(): {testplant.get_neighbors_impact()}')
        print(f'DL, testplant: {testplant.get_height() - testplant.get_neighbors_impact()}')
        # For Added plant
        stats_after_growth = testplant.report_stats()
        print(f'testplant after {i}.th step, after growth: \n {stats_after_growth} \n ')
        # print('\n Ended testplant GROWING \n')
        # For a default plant in environment (created by running set_up of Plantmap in Environment)
        stats_after_default_plant = testplant_created_in_environment.report_stats()
        print(f'created in environment after {i}.th step,after growth (DEFAULT PLANT): \n {stats_after_default_plant} \n ')

    print('\n ------------------------------------------------------------------------------------------- \n ------------------------------------------------------------------------------------------- \n Successfully shown that we can \n  - add Maps to an environment, \n  - set specific plants at a certain location in this environment \n - add the environment to them \n and - grow all plants at once \n ------------------------------------------------------------------------------------------- \n ------------------------------------------------------------------------------------------- ')
# 
if __name__ == '__main__':
    main()