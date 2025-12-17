import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from Statstics import Statistics
from Map import Watermap, Shademap, Plantmap
from Simulation import Simulation
from CSV_handler import CSV_handler



def main():

    np.random.seed(10)
    path_to_mwm14 = '~/GitHub/Moss_growth/.venv_Model_Sphag/HaywardAndClymo1983/MWM14_data_whole_range.csv'
    # trying to load csv
    csvhandler = CSV_handler()

    # trying to load a csv table
    df, wtd_array_in_cm = csvhandler.get_daily_dataframe_and_array_from_mm_csv(path_to_csv=path_to_mwm14)

    # Created 
    # - 5 x 5 grid
    # - initial heights will be normally distributed around arbitrary zero with standard deviation of 0.5
    params = {'number_of_spots_per_row': 5,
              'number_of_rows': 5,
              'INIT_MODE': 'NORM_DIST',
              'init_mean': 0.0,
              'init_std': 0.5}
    
    # timesteps
    timesteps = len(wtd_array_in_cm)

    series_of_watermaps_with_heights_from_wtd_array = []

    # Make watermap series #######################################################################
    for i in range(len(wtd_array_in_cm)):

        # make new watermap object
        wm_i = Watermap(number_of_rows=params['number_of_rows'],
                             number_of_spots_per_row=params['number_of_spots_per_row'],
                             items=None
                             )
        # fill it with the values from the water-tables from csv table
        wm_i.set_up(constant_value=wtd_array_in_cm[i])

        # append this watermap to the list
        series_of_watermaps_with_heights_from_wtd_array.append(wm_i)
    
    initial_wm = Watermap(number_of_rows=params['number_of_rows'],
                             number_of_spots_per_row=params['number_of_spots_per_row'],
                             items=None
                             )
    
    # change the values for the depth to initial values
    initial_wm.set_up(constant_value=wtd_array_in_cm[0])
    #############################################################################################

    # set up Simulation
    
    simulation = Simulation(timesteps=timesteps, params=params, init_species='capillifolium')

    # MAKE SIMULATION CAP ZERO AND APPR HEIGHT BY MASS ###########################################################################
    # Explicitly tell to use cap zero and approximate height by mass
    # set growth models to cap zero and approximate height by mass for all plants
    for row in range(params['number_of_rows']):
        for spot in range(params['number_of_spots_per_row']):
            plant = simulation.get_environment().get_plantmap().get_item_at(index_row=row, index_spot_in_row=spot)
            plant.get_growth_processes_model().set_cap_zero(True)
            plant.get_growth_processes_model().set_approximate_height_by_mass(True)
            plant.get_growth_processes_model().set_treat_values_outside_polynomial_growth_as_constants(False)
    ###############################################################################################################################
    
    heights, masses, shades, waters = simulation.run(print_log=False, adapt_water_table_height_to_average_carpet_height=True, adapted_depth_below_average_carpet_height=3.0)
    stats = Statistics(results_height=heights, results_mass=masses, results_shade=shades, results_water_table_depth=waters, timesteps=timesteps, params=params)
    fig, ax = stats.plot_average_height_masses(instant_plot=False, plt_water_and_shade=False, height_plot=5.0)
    fig, ax = stats.plot_variance_height_masses(fig=fig, ax=ax, instant_plot=False)
    fig, ax = stats.plot_average_elong_and_net_prod(fig=fig, ax=ax, instant_plot=True)
    

    # Sensitivity analysis
    k_ar = np.linspace(-1.39, 1.0, 1)


    # make results container for sensitivity analysis
    heights_under_k = np.zeros((len(k_ar), timesteps + 1, params['number_of_rows'], params['number_of_spots_per_row']))
    variances_height_under_k = np.zeros((len(k_ar), timesteps + 1))
    

    for i,k in enumerate(k_ar):
        heights, masses, shades, waters = simulation.run(print_log=False, watermap_series=series_of_watermaps_with_heights_from_wtd_array, k_elong=k, k_prod=k)
        print(f'masses: {masses}')
        print(f'heights: {heights}')
        stats = Statistics(results_height=heights, results_mass=masses, results_shade=shades, results_water_table_depth=waters, timesteps=timesteps, params=params)
        fig, ax = stats.plot_average_height_masses(instant_plot=False, plt_water_and_shade=True, height_plot=5.0)
        # fig, ax = stats.plot_variance_height_masses(fig=fig, ax=ax, instant_plot=False)
        variances_height_under_k[i], vm_under_k, _, _ = stats.get_time_series_of_variances()
        heights_under_k[i] = heights
    
    # get the average height at the last timestep
    plt.plot(k_ar, [np.average(heights_under_k[j,-1,:,:]) for j in range(len(k_ar))])
    fig, ax = stats.plot_water_height() 
    plt.show()

if __name__ == '__main__':
    main()