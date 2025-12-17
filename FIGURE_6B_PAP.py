import numpy as np
from Plant import Plant
from Map import Plantmap, Shademap, Watermap
from Environment import Environment
from Simulation import Simulation
from Statstics import Statistics
from pathlib import Path
import matplotlib.pyplot as plt
import matplotlib.pyplot as plt

from matplotlib.gridspec import GridSpec

# define the main function
def main():
    length_color = (0.29, 0.0, 0.51) # dark purple
    mass_color = 'darkgreen'
    species = 'papillosum'
    print(" #####################################################################################################################################################\n Reproduction of Growth Experiment results from Hayward and Clymo, 1983: Figure 6 \n #####################################################################################################################################################\n")

    ################# FIGURE 6b ###############################
    ################################### NUMNER OF RUNS '#####
    number_of_runs = 50
    timesteps = 600
    
    params = {'number_of_spots_per_row': 5,
              'number_of_rows': 5,
              'INIT_MODE': 'NORM_DIST',
              'init_mean': 0.0,
              'init_std': 0.5}
    
    # Watermap of -12 cm
    three_cm_deep = Watermap(number_of_rows=params['number_of_rows'],
                             number_of_spots_per_row=params['number_of_spots_per_row'],
                             items=None
                             )
    
    # change the values for the depth to -12 cm
    three_cm_deep.set_up(constant_value=-3.0)

    # shade 0.3
    shademap_03 = Shademap(number_of_rows=params['number_of_rows'],
                           number_of_spots_per_row=params['number_of_spots_per_row'],
                           items = None)
    
    # change the external shade to 0.3 everywhere
    shademap_03.set_up(constant_value=0.3)

    
    #################################### create Simulation, DEFINE SPECIES ---------->------------------->-------------------------------------------------!
    simulation = Simulation(timesteps=timesteps, params=params, initial_water_map=three_cm_deep, initial_external_shade_map=shademap_03, init_species=species)
    #########################################################################################################
    # Explicitly tell to use constants outside of the bounds
    # CONSTANT OUTBOUNDS
    for row in range(params['number_of_rows']):
        for spot in range(params['number_of_spots_per_row']):
            plant = simulation.get_environment().get_plantmap().get_item_at(index_row=row, index_spot_in_row=spot)
            plant.get_growth_processes_model().set_cap_zero(False)
            plant.get_growth_processes_model().set_approximate_height_by_mass(False)
            plant.get_growth_processes_model().set_treat_values_outside_polynomial_growth_as_constants(True)
    ###### BOUNDS END #########################################################################################

    # try the plot bands stuff
    # DUMMY RUN
    runs_height, runs_masses, shades, waters = simulation.run(adapt_water_table_height_to_average_carpet_height=True, adapted_depth_below_average_carpet_height=3.0)
    stats = Statistics(results_height=runs_height, results_mass=runs_masses, results_shade=shades, results_water_table_depth=waters, timesteps=timesteps, params=params)

    fig = plt.figure(figsize=(10,7))
    gs1 = GridSpec(12, 8, left=0.1, right=0.90, wspace=1, figure=fig)
    ax1 = fig.add_subplot(gs1[:8, :8])
    ax2 = fig.add_subplot(gs1[8:11, :])
    # plot water table
    stats.plot_water_height(fig=fig, ax=ax2, plot_zero=False)
    ax2.set_ylim(auto=True)
    
    # make heatmaps
    fig2, ax = stats.plot_heatmap_height_at(timestep=timesteps, species=species)
    fig3, ax = stats.plot_heatmap_masses_at(timestep=timesteps, species=species)

    # plot bands
    _,_, species = stats.plot_means_and_bands_of_runs(fig=fig, ax=ax1, simulation=simulation, scaling=True, number_of_runs=number_of_runs, adapt_water_table_height_to_average_carpet_height=True, adapted_depth_below_average_carpet_height=3.0)
    
    ax1.set_ylim(bottom=0,top=10.0)
    ax1.tick_params(
        axis='x',          
        which='both',      
        bottom=False,      
        top=False,         
        labelbottom=False)
    ax2.sharex(ax1)
    fig.suptitle(f'Temporal Dynamics: $\\mathit{{S.\\ {species}}}$')
    fig.legend(loc='lower center', ncol= 4, bbox_to_anchor =(0.5, 0.02))

    #### RENAME!###########################################################
    # Save TIME SERIES
    fig_path_and_name = Path(f'~/GitHub/Moss_growth/.venv_Model_Sphag/HaywardAndClymo1983/Thesis_Tex_files/Plots/Replication/Figure_b_{species}_bands_water.pdf').expanduser()
    fig.savefig(str(fig_path_and_name))

    # Save HEATMAP HEIGHT
    fig_path_and_name = Path(f'~/GitHub/Moss_growth/.venv_Model_Sphag/HaywardAndClymo1983/Thesis_Tex_files/Plots/Replication/Figure_b_{species}_heatmap_height.pdf').expanduser()
    fig2.savefig(str(fig_path_and_name))

    # Save HEATMAP MASS
    fig_path_and_name = Path(f'~/GitHub/Moss_growth/.venv_Model_Sphag/HaywardAndClymo1983/Thesis_Tex_files/Plots/Replication/Figure_b_{species}_heatmap_mass.pdf').expanduser()
    fig3.savefig(str(fig_path_and_name))
    
    plt.show()




print('\n ------------------------------------------------------------------------------------------- \n ------------------------------------------------------------------------------------------- \n Successfully shown that we can \n  - add Maps to an environment, \n  - set specific plants at a certain location in this environment \n - add the environment to them \n and - grow all plants at once \n ------------------------------------------------------------------------------------------- \n ------------------------------------------------------------------------------------------- ')
# 
if __name__ == '__main__':
    main()