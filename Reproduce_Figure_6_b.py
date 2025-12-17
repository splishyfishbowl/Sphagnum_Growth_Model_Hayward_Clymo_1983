import numpy as np
from Plant import Plant
from Map import Plantmap, Shademap, Watermap
from Environment import Environment
from Simulation import Simulation
from Statstics import Statistics
from pathlib import Path

# define the main function
def main():
    print(" #####################################################################################################################################################\n Reproduction of Growth Experiment results from Hayward and Clymo, 1983: Figure 6 \n #####################################################################################################################################################\n")

    # Created 
    # - 5 x 5 grid
    # - initial heights will be normally distributed around arbitrary zero with standard deviation of 0.5
    params = {'number_of_spots_per_row': 10,
              'number_of_rows': 5,
              'INIT_MODE': 'NORM_DIST',
              'init_mean': 0.0,
              'init_std': 0.5}
    
    # timesteps
    timesteps = 600

    
    ################# FIGURE 6b ###############################

    timesteps = 600
    
    params = {'number_of_spots_per_row': 5,
              'number_of_rows': 5,
              'INIT_MODE': 'NORM_DIST',
              'init_mean': 0.0,
              'init_std': 0.5}
    
    # Watermap of -12 cm
    twelve_cm_deep = Watermap(number_of_rows=params['number_of_rows'],
                             number_of_spots_per_row=params['number_of_spots_per_row'],
                             items=None
                             )
    
    # change the values for the depth to -12 cm
    twelve_cm_deep.set_up(constant_value=-12.0)

    # shade 0.3
    shademap_03 = Shademap(number_of_rows=params['number_of_rows'],
                           number_of_spots_per_row=params['number_of_spots_per_row'],
                           items = None)
    
    # change the external shade to 0.3 everywhere
    shademap_03.set_up(constant_value=0.3)

    # create Simulation
    figure_6_b_simulation = Simulation(timesteps=timesteps, params=params,initial_water_map=twelve_cm_deep, initial_external_shade_map=shademap_03)

    # make plants at (1,2) -1cm high
    figure_6_b_simulation.get_environment().get_plantmap().get_item_at(1,2).set_height(-1.0)

    # make plant at (3,4) 1 cm high
    figure_6_b_simulation.get_environment().get_plantmap().get_item_at(1,2).set_height(1.0)
    # run the simulation and save results
    # ADAPTIVE WATER-TABLE
    heights, masses, shade, water = figure_6_b_simulation.run(constant_watermap=twelve_cm_deep, constant_shademap=shademap_03, print_log=False, adapt_water_table_height_to_average_carpet_height=True, adapted_depth_below_average_carpet_height=12.0)
    
    # make Statistics object
    stats = Statistics(results_height=heights, results_mass=masses, results_shade=shade, results_water_table_depth=water, timesteps=timesteps, params=params)
    fig, ax = stats.plot_average_height_masses(instant_plot=False, plt_water_and_shade=True, height_plot=5.0)
    fig, ax = stats.plot_variance_height_masses(fig=fig, ax=ax, instant_plot=False)
    fig, ax = stats.plot_average_elong_and_net_prod(fig=fig, ax=ax, instant_plot=True)
    fig_path_and_name = Path('~/GitHub/Moss_growth/.venv_Model_Sphag/HaywardAndClymo1983/Plots/figure_6_b.png').expanduser()
    fig.savefig(fig_path_and_name, format='png')

    stats.plot_heatmap_height_at(timestep=600, instant_plot=True)
    stats.plot_heatmap_masses_at(timestep=600, instant_plot=True)

    print('\n ------------------------------------------------------------------------------------------- \n ------------------------------------------------------------------------------------------- \n Successfully shown that we can \n  - add Maps to an environment, \n  - set specific plants at a certain location in this environment \n - add the environment to them \n and - grow all plants at once \n ------------------------------------------------------------------------------------------- \n ------------------------------------------------------------------------------------------- ')
# 
if __name__ == '__main__':
    main()