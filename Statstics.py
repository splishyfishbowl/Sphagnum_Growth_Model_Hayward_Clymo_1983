'''
DESCRIPTION
This shall be a class that makes us able to perform various statistical operations on the data produced by a Simualation run.
Therefore, this class accesses the Environments shade- water- and plantmap. 
Here, the values are stored and will be extracted (sounds complicated, it is not, as the Maps are basically two-dimensional numpy.arrays).
Extraction more or less means, that we are
- just reading the values in shade- and watermap.items
- accessing the plant objects in plantmap.items() and get their data (height and mass)

DETAILS
Indirectly, of course, the Environment just refers to its Plant- Water- and Shademap object.
What do I mean by that?

At the end, every plant controls its own growth by calling Plant.get_growth_values() and Plant.grow_step().
These methods then call the Growth_Processes_Model to calculate the growth given certain conditions (such as Water-table-depth, external_shade and the neighbors height_values and, of course, all parameters).
These parameters and environmental variables are of course dependent on the type of growth mechanics built into the Growth_Processes_Model.
So one plant is passive in the sense, that other class objects are calling the Plants internal functions while the Plant object itself is not calling anything in a Plant.main function or something similar.
This is done by the Environment object, where all individuals of plants are really "put together". 
This means:
    - Introducing spatial dimensions (a twodimensional grid) to be able to "locate" a plant 
    - Let the plants know which neighbors they have
    - Initializing plants (give them a height, environmental conditions)

And to be able to address all the plants and all the spots with their certain conditions, Map are created.
They map Water, Shade or Plants to the locations introduced by the Environments.
Basically they are twodimensional numpy arrays with some advanced features.

I like to think about the Plants objects as seeds, not really plants.
They are planted into the environment, which has some variables to it (Water, Shade, location).
These are saved using the Maps and the Environment just brings this all together and lets them work together.
At the end, the Maps contain all the relevant data we need for statistical analysis.
    
'''

from Environment import Environment
from Map import Plantmap, Watermap, Shademap
from Plant import Plant
from Growth_Processes_Model import Growth_Processes_Model

import numpy as np
import matplotlib.pyplot as plt
# from colorspacious import cspace_converter
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib import colormaps
import pandas as pd
import os
from pathlib import Path


# What do we need?
# # (Reproduce) Figure 6

# - *S. capillifolium*
    
# - 600 days
# - (a)
#     - no external shade 
#     - 3 cm water table depth 
# - (b)
#     - external shade 0.3
#     - 12 cm water table below
#         - variable, scaling factor 
#         - A(2) average length (cm), 0.40
#         - A(3) average mass (mg), 0.25
#         - A(4) variance in length/ surface roughness (cm²), 20.0
#         - A(5) variance in mass (mg²), 1.0
#         - A(6) average rate of elongation (cm day⁻1), 40.0
#         - A(7) average rate of production (mg day⁻1), 40.0
#         - A(8) average etiolation (cm mg⁻1), 10.0
#         Plants of initial height +1 cm or -1 cm below or above the surface
#         - A(10) exposure effect with $k= -1.39$
#         - A(17) shade
#         Additional information
#         - in (b) A(5) after 600 days has a value of 35 mg² (so really high)

class Statistics:
    # TODO:
    #    - Seperate, what shall be inside Statistics, what inside Simulation run
    #    - Make Statistics pass only the resuls of a SImulation run (three-dimensional numpy.array)
    #    - Make some methods returning statistics
    #    - 


    def __init__(self, results_height: np.ndarray, results_mass: np.ndarray, results_water_table_depth: np.ndarray, results_shade: np.ndarray, timesteps: int, params: dict, species='capillifolium', weights_for_different_variables = {'weight_height': 0.4,
                                                                                                                                                                                                               'weight_mass': 0.25,
                                                                                                                                                                                                               'weight_var_height': 20.0,
                                                                                                                                                                                                               'weight_var_mass': 1.0,
                                                                                                                                                                                                               'weight_avg_elong': 40.0,
                                                                                                                                                                                                               'weight_avg_net_prod': 40.0}):
        '''
        Initiates the environment class attribute we need, to access the Data (in form of maps) there
        '''
        # weights for plotting
        self._weights_for_different_variables = weights_for_different_variables

        if not (results_height.shape == (timesteps+1, params['number_of_rows'], params['number_of_spots_per_row'])
                and results_mass.shape == (timesteps+1, params['number_of_rows'], params['number_of_spots_per_row'])
                and results_water_table_depth.shape == (timesteps+1, params['number_of_rows'], params['number_of_spots_per_row'])
                and results_shade.shape == (timesteps+1, params['number_of_rows'], params['number_of_spots_per_row'])
                ):
            print(f'Statistics.__init__(): Results do not have the correct shape: \nWe need shape {(timesteps+1, params['number_of_rows'], params['number_of_spots_per_row'])}.\nBut Statistics got:\nresults_mass.shape: {results_mass.shape}\n esults_height.shape: {results_height.shape}\nresults_water_table_depth.shape: {results_water_table_depth.shape}\nresults_shade.shape: {results_shade.shape}')

        # If we have correct shapes for the results
        else:
            self._results_height = results_height
            self._results_mass = results_mass
            self._results_water_table_depth = results_water_table_depth
            self._results_shade = results_shade
            self._timesteps = timesteps
            self._params = None
            self._species = species

            # Check parameter dictionary
            if (
                isinstance(params['number_of_spots_per_row'], int) and
                isinstance(params['number_of_rows'], int) and
                isinstance(params['INIT_MODE'], str) and
                isinstance(params['init_mean'], float) and
                isinstance(params['init_std'], float) and
                params['number_of_spots_per_row'] > 0 and
                params['number_of_rows'] > 0 and
                params['init_std'] >= 0
                ):
                # initiate params
                print('Statistics.__init__(): Successfully initiated params')
                self._params = params
                
            else:
                print(f'Statistics.__init__(): ERROR in initiating params')

    ##### CHECKER #################################

    ##### GETTER ##################################
    def get_species(self):
        return self._species

    def get_results_height(self):
        return self._results_height
    
    def get_results_mass(self):
        return self._results_mass
    
    def get_results_water_table_depth(self):
        return self._results_water_table_depth
    
    def get_results_external_shade(self):
        return self._results_shade
    
    def get_timesteps(self):
        return self._timesteps
    
    def get_params(self):
        return self._params

    def get_weights_for_different_variables(self):
        return self._weights_for_different_variables
    
    #### SETTER ###################################
    def set_species(self, species):
        self._species = species

    def set_results_height(self, results_height: np.ndarray):
        # Check shape
        if (results_height.shape == self._results_height.shape):
            self._results_height = results_height
        else:
            print(f'Simulation.set_results_height(): Incompatible shape of new array: \nshape {self._results_height.shape} is needed, but got {results_height.shape}')
    
    def set_results_mass(self, results_mass: np.ndarray):
        # Check shape
        if (results_mass.shape == self._results_mass.shape):
            # Update
            self._results_mass = results_mass
        else:
            print(f'Simulation.set_results_mass(): Incompatible shape of new array: \nshape {self._results_mass.shape} is needed, but got {results_mass.shape}')
    
    def set_results_water_table_depth(self, results_water_table_depth: np.ndarray):
        # Check shape
        if (results_water_table_depth.shape == self._results_water_table_depth):
            self._results_water_table_depth = results_water_table_depth
        else:
            print(f'Simulation.set_results_water_table_depth(): Incompatible shape of new array: \nshape {self._results_water_table_depth.shape} is needed, but got {results_water_table_depth.shape}')
    
    def set_results_shade(self, results_shade: np.ndarray):
        # Check shape
        if (results_shade.shape == self._results_shade.shape):
            self._results_shade = results_shade
        else:
            print(f'Simulation.set_results_shade(): Incompatible shape of new array: \nshape {self._results_shade.shape} is needed, but got {results_shade.shape}')
    
    def set_timesteps(self, timesteps: int):
        self._timesteps = timesteps

    def set_params(self, params: dict):
        # Check for correct entries

    ######### METHODS #######################################################

    
        '''
        RETURN VALUE
        average_height, average_mass

        Returns the 
        - average length and 
        - average mass 
        of the plants in Plantmap attribute of environment object at a certain point in time.

        '''
        # get the values from the plantmap
        heights, masses = self.load_plants_height_and_masses_values()

        # flatten, make the average
        flattened_heights = np.flatten(heights)
        flattened_masses = np.reshape(masses)

        average_height = np.average(flattened_heights)
        average_mass = np.average(flattened_masses)

        # return average values
        return average_height, average_mass

#########         #########################################
######### METHODS #########################################
#########         #########################################


######### STATISTICS ######################################
    def get_elongs_and_net_prods_at(self, timestep: int):
        '''
        ## RETURN
        elongation: *float* or *Integer* array, avg_net_prod: *float* or *Integer* array
        Returns the elongation and net productivity (as mass gain) for all plants a specific timestep.
        Returns get_elongs_and_net_prods_at(timestep=1) for the 0.th timestep.
        It is calculated by getting the height/mass of the current timestep for all plants and subtracts the height/mass of all plants at the previous timestep.
        ## PARMETER
        timestep: *Integer*  
        The timestep, where we want to get the elongation and productivity of the twodimensional grid.
        '''
        # Check, if timesteps is referencable
        if (1 <= timestep < self.get_timesteps() + 1):

            # calculate average of elongation by gettting the difference of average height now and in the last step
            height_prev_step = self.get_results_height()[timestep-1]
            height_current_step = self.get_results_height()[timestep]
            elongation = height_current_step - height_prev_step

            # calculate average of net productivity by gettting the difference of average mass now and in the last step
            mass_prev_step = self.get_results_mass()[timestep-1]
            mass_this_step = self.get_results_mass()[timestep]
            net_prod = mass_this_step - mass_prev_step

            # return
            return elongation, net_prod
        
        elif timestep==0:
            # return the same value as, as the plant could not grow here
            return self.get_elongs_and_net_prods_at(timestep=1)
        else:
            print(f'Statistics.get_elongs_and_net_prods_at(): Something went wrong. timestep: {timestep}, allowed: {self.get_timesteps()}')

    def get_average_height_mass_wtd_shade_at_timestep(self, timestep: int):
        '''
        ## RETURN
        Returns all the averages of the twodimensional grid   
        (  
        - height 
        - mass of the plants
        - water_table_depth 
        - external shade at each spot  
        ) for a specific timestep.
        ## PARMETER
        timestep: *Integer*  
        The timestep, where we want to get all the average values of the twodimensional grid
        '''
        # Check, if timesteps is referencable
        if (0 <= timestep < self.get_timesteps() + 1):

            # calculate averages
            avg_height = np.average(self.get_results_height()[timestep])
            avg_mass = np.average(self.get_results_mass()[timestep])
            avg_water_table_height = np.average(self.get_results_water_table_depth()[timestep])
            avg_shade = np.average(self.get_results_external_shade()[timestep])

            # return
            return avg_height, avg_mass, avg_water_table_height, avg_shade

        else:
            # print out, that we cannot access given timestep data
            print(f'Statistics.get_average_height_mass_wtd_shade_at_timestep():\ntimestep value {timestep} is out of bounds.\nTimestep possible between 0 and {self.get_timesteps + 1}.\n Returned -1 for everything.')
            
            return -1.0, -1.0, -1.0, -1.0
        
    def get_average_for_all_timesteps(self):

        '''
        ##RETURN
        Returns the average (for all timesteps, across the whole grid) of a variable  
        (  
        - height 
        - mass of the plants
        - water_table_depth 
        - external shade at each spot  
        ) for a specific timestep.
          
        So we return _four_ single values.
        '''

        # return all the values accessed by numpy slicing
        height_timmean = np.average(self.get_results_height())
        mass_timmean = np.average(self.get_results_mass())
        water_timmean = np.average(self.get_results_water_table_depth())
        ext_shade_timmean = np.average(self.get_results_external_shade())

        # return values
        return height_timmean, mass_timmean, water_timmean, ext_shade_timmean
    
    def get_time_series_of_averages(self):
        '''
        ## RETURN
        averages_height *np.ndarray*, averages_masses *np.ndarray*, averages_water_table_heights *np.ndarray*, averages_exterbal_shade *np.ndarray*  
        This function return a time series of averages for all the relevant variables   
        (  
        - height 
        - mass of the plants
        - water_table_depth 
        - external shade at each spot  
        ) 
        This means, that we calculate the average across the grid at each timestep and return a series with length *timesteps* for all four variables.
    
        '''
        # Make empty container for each variable
        averages_height = np.zeros(self.get_timesteps() + 1)
        averages_masses = np.zeros(self.get_timesteps() + 1)
        averages_water_table_heights = np.zeros(self.get_timesteps() + 1)
        averages_external_shade = np.zeros(self.get_timesteps() + 1)

        # iterate over all 
        for t in range(self.get_timesteps()+1):

            # get all the averages for the specific timestep
            averages_height[t], averages_masses[t], averages_water_table_heights[t], averages_external_shade[t] = self.get_average_height_mass_wtd_shade_at_timestep(t)

        # return time_series
        return averages_height, averages_masses, averages_water_table_heights, averages_external_shade
    
    def get_variance_height_mass_wtd_shade_at_timestep(self, timestep: int):
        '''
        ## RETURN
        Returns all the varinaces of the twodimensional grid   
        (  
        - height 
        - mass of the plants
        - water_table_depth 
        - external shade at each spot  
        ) for a specific timestep.
        ## PARMETER
        timestep: *Integer*  
        The timestep, where we want to get all the variance values of the twodimensional grid
        '''
        # Check, if timesteps is referencable
        if (0 <= timestep < self.get_timesteps() + 1):

            # calculate averages
            var_height = np.var(self.get_results_height()[timestep])
            var_mass = np.var(self.get_results_mass()[timestep])
            var_water_table_height = np.var(self.get_results_water_table_depth()[timestep])
            var_shade = np.var(self.get_results_external_shade()[timestep])

            # return
            return var_height, var_mass, var_water_table_height, var_shade

        else:
            # print out, that we cannot access given timestep data
            print(f'Statistics.get_variance_height_mass_wtd_shade_at_timestep():\ntimestep value {timestep} is out of bounds.\nTimestep possible between 0 and {self.get_timesteps + 1}.\n Returned 0.0 for everything.')
            
            return 0.0, 0.0, 0.0, 0.0

    def get_time_series_of_variances(self):
        '''
        ## RETURN
        variances_height *np.ndarray*, variances_masses *np.ndarray*, variances_water_table_heights *np.ndarray*, variances_exterbal_shade *np.ndarray*  
        This function returns a time series of averages for all the relevant variables   
        (  
        - height 
        - mass of the plants
        - water_table_depth 
        - external shade at each spot  
        ) 
        This means, that we calculate the variance across the grid at each timestep and return a series with length *timesteps* for all four variables.
    
        '''
        # Make empty container for each variable
        variances_height = np.zeros(self.get_timesteps() + 1)
        variances_masses = np.zeros(self.get_timesteps() + 1)
        variances_water_table_heights = np.zeros(self.get_timesteps() + 1)
        variances_external_shade = np.zeros(self.get_timesteps() + 1)

        # iterate over all 
        for t in range(self.get_timesteps()+1):

            # get all the averages for the specific timestep
            variances_height[t], variances_masses[t], variances_water_table_heights[t], variances_external_shade[t] = self.get_variance_height_mass_wtd_shade_at_timestep(t)

        # return time_series
        return variances_height, variances_masses, variances_water_table_heights, variances_external_shade
    
    def get_average_elongation_net_productivity(self, timestep: int):
        '''
        ## RETURN
        avg_elongation: *float* or *Integer*, avg_net_prod: *float* or *Integer*
        Returns the average elongation and net productivity (as mass gain) for a specific timestep.
        Returns get_average_elongation_net_productivity(timestep=1) for the 0.th timestep.
        It is calculated by getting the average height/mass of the current timestep for all plants and subtracts the average height/mass of all plants at the previous timestep.
        ## PARMETER
        timestep: *Integer*  
        The timestep, where we want to get the average elongation and productivity of the twodimensional grid.
        '''
        # Check, if timesteps is referencable
        if (1 <= timestep < self.get_timesteps() + 1):

            # calculate average of elongation by gettting the difference of average height now and in the last step
            avg_height_prev_step = np.average(self.get_results_height()[timestep-1])
            avg_height_current_step = np.average(self.get_results_height()[timestep])
            avg_elongation = avg_height_current_step - avg_height_prev_step

            # calculate average of net productivity by gettting the difference of average mass now and in the last step
            avg_mass_prev_step = np.average(self.get_results_mass()[timestep-1])
            avg_mass_this_step = np.average(self.get_results_mass()[timestep])
            avg_net_prod = avg_mass_this_step - avg_mass_prev_step

            # return
            return avg_elongation, avg_net_prod
        
        elif timestep==0:
            # return the same value as, as the plant could not grow here
            return self.get_average_elongation_net_productivity(timestep=1)

    def get_var_elong_net_prod_at_timestep(self, timestep: int):
        '''
        ## RETURN
        var_elong, var_net_prod at the timestep timestep

        if timestep is out of bounds, 0.0, 0.0
        '''
        
        # Check, if timesteps is referencable
        if (0 <= timestep < self.get_timesteps() + 1):

            # calculate averages
            var_elong, var_net_prod = np.var(self.get_elongs_and_net_prods_at(timestep=timestep)[0]), np.var(self.get_elongs_and_net_prods_at(timestep=timestep)[1])
            
            # return
            return var_elong, var_net_prod

        else:
            # print out, that we cannot access given timestep data
            print(f'Statistics.get_var_elong_net_prod_at_timestep():\ntimestep value {timestep} is out of bounds.\nTimestep possible between 0 and {self.get_timesteps + 1}.\n Returned 0.0 for everything.')
            
            return 0.0, 0.0

    def get_time_series_of_average_elongation_and_mass(self):
        '''
        ## Returns  
        avg_elong: *np.ndarray*, avg_net_prod: *np.ndarray*
        Time series of average elongation and net productivity.
        Calculated by taking the difference of the average height/mass of the plants at a certain timestep and the average height/mass at the previous timestep.
        For the 0.th timestep 0.0, 0.0 is saved.
        '''
        # Make empty container for each variable
        avg_elong = np.zeros(self.get_timesteps() + 1)
        avg_net_prod = np.zeros(self.get_timesteps() + 1)
        

        # iterate over all 
        for t in range(self.get_timesteps()+1):

            # get all the averages for the specific timestep
            avg_elong[t], avg_net_prod[t] = self.get_average_elongation_net_productivity(t)

        # return time_series
        return avg_elong, avg_net_prod

    def get_time_series_variance_elong_net_prod(self):
        '''
        ## Returns:
        Timeseries of the variances of elong and net_prod
        '''
        # Make empty container for each variable
        var_elong = np.zeros(self.get_timesteps() + 1)
        var_net_prod = np.zeros(self.get_timesteps() + 1)

        # iterate over all 
        for t in range(self.get_timesteps()+1):

            # get all the averages for the specific timestep
            var_elong[t], var_net_prod[t] = self.get_var_elong_net_prod_at_timestep(t)

        # return time_series
        return var_elong, var_net_prod

########### Make BANDS #######################################

    def get_means_and_bands_from_simulation(self, simulation, constant_watermap = None, water_table_series = None, number_of_runs=1.0, adapt_water_table_height_to_average_carpet_height = False, adapted_depth_below_average_carpet_height=0.0):
            '''
            ## RETURN  
            all are numpyarrays of length timesteps + 1

            avg_avg_height, std_avg_height, avg_avg_masses, std_avg_masses, avg_avg_elong, std_avg_elong, avg_avg_net_prod , std_avg_net_prod
            
            '''

            # check for Simulation object
            from Simulation import Simulation
            
            # If the passed simulation object is indeed a Simulation
            if isinstance(simulation, Simulation):

                # initialize timesteps and params from there
                params = simulation.get_params()
                timesteps = simulation.get_timesteps()

                
                # make container for the results: complete timeseries
                runs_height = np.zeros(((number_of_runs, timesteps + 1, params['number_of_rows'], params['number_of_spots_per_row'])))
                runs_masses = np.zeros((number_of_runs, timesteps + 1, params['number_of_rows'], params['number_of_spots_per_row']))
                runs_shades = np.zeros(((number_of_runs, timesteps + 1, params['number_of_rows'], params['number_of_spots_per_row'])))
                runs_waters = np.zeros(((number_of_runs, timesteps + 1, params['number_of_rows'], params['number_of_spots_per_row'])))
                runs_elongations = np.zeros(((number_of_runs, timesteps + 1, params['number_of_rows'], params['number_of_spots_per_row'])))
                runs_prod = np.zeros(((number_of_runs, timesteps + 1, params['number_of_rows'], params['number_of_spots_per_row'])))
                
                # timeseries of average values
                avg_elongs = np.zeros(((number_of_runs, timesteps + 1)))
                avg_net_prods = np.zeros(((number_of_runs, timesteps + 1)))
                avg_heights = np.zeros((number_of_runs, timesteps + 1))
                avg_masses = np.zeros((number_of_runs, timesteps + 1))
                avg_shades = np.zeros((number_of_runs, timesteps + 1))
                avg_waters = np.zeros((number_of_runs, timesteps + 1))
                
                # variances: especially needed for the band width plotting
                var_heights = np.zeros((number_of_runs, timesteps + 1))
                var_masses = np.zeros((number_of_runs, timesteps + 1))
                var_elong = np.zeros((number_of_runs, timesteps + 1))
                var_net_prod = np.zeros((number_of_runs, timesteps + 1))
                var_waters = np.zeros((number_of_runs, timesteps + 1))
                var_shades = np.zeros((number_of_runs, timesteps + 1))

                # averages of averages
                avg_avg_height = np.zeros((timesteps + 1))
                avg_avg_mass = np.zeros((timesteps + 1))
                avg_avg_elong = np.zeros((timesteps + 1))
                avg_avg_net_prod = np.zeros((timesteps + 1))
                avg_var_mass = np.zeros((timesteps + 1))
                avg_var_height = np.zeros((timesteps + 1))

                # variances of the averages (variance between runs)
                std_avg_height = np.zeros((timesteps + 1))
                std_avg_masses = np.zeros((timesteps + 1))
                std_avg_elong = np.zeros((timesteps + 1))
                std_avg_net_prod = np.zeros((timesteps + 1))
                std_var_mass = np.zeros((timesteps + 1))
                std_var_height = np.zeros((timesteps + 1))

                # loop for simulating
                for r in range(number_of_runs):
                    
                    # make the initial conditions of heights normally distributed
                    simulation.set_init_mode_height(self.get_params()['INIT_MODE'])

                    # run the simulation
                    # RAW DATA
                    runs_height[r,:,:,:], runs_masses[r,:,:,:], runs_shades[r,:,:,:], runs_waters[r,:,:,:] = simulation.run(watermap_series=water_table_series, constant_watermap=constant_watermap, adapt_water_table_height_to_average_carpet_height=adapt_water_table_height_to_average_carpet_height, adapted_depth_below_average_carpet_height=adapted_depth_below_average_carpet_height)

                    # make statistics object
                    stats = Statistics(results_height=runs_height[r,:,:,:], results_mass=runs_masses[r,:,:,:], results_shade=runs_shades[r,:,:,:], results_water_table_depth=runs_waters[r,:,:,:], timesteps=timesteps, params=params)
                    
                    # AVERAGES PER TIMESTEP
                    # save averages at each timestep -> get timeseries
                    avg_heights[r], avg_masses[r], avg_shades[r], avg_waters[r] = stats.get_time_series_of_averages()

                    # save averages at each timestep for elong and net_prod-> get timeseries 
                    avg_elongs[r], avg_net_prods[r] = stats.get_time_series_of_average_elongation_and_mass()

                    # VARIANCES PER TIMESTEP
                    # save variances timeseries
                    var_heights[r], var_masses[r], var_shades[r], var_waters[r] = stats.get_time_series_of_variances()

                    # save variances at each timestep for elongation rate and net prod
                    var_elong[r], var_net_prod[r] = stats.get_time_series_variance_elong_net_prod()
                
                # Make POINTWISE averages of averages
                # Therefore we have to iterate over all TIMESTEPS
                # calculte the standard deviation at each timestep for the average height across all runs
                for ts in range(timesteps + 1):
                    # print(f'get_means_and_bands_from_simulation(): timestep {ts}')
                    
                    # get the std of all average lengths and masses at this timestep (for the several runs) (right side)
                    # save standard deviations across the runs (left side)
                    # variances of the averages (variance between runs)
                    std_avg_height[ts] = np.std(avg_heights[:, ts])
                    std_avg_masses[ts] = np.std(avg_masses[:, ts]) 
                    std_avg_elong[ts]  = np.std(avg_elongs[:, ts])
                    std_avg_net_prod[ts] = np.std(avg_net_prods[:, ts])
                    
                    std_var_mass[ts] = np.std(var_masses[:, ts])
                    std_var_height[ts] = np.std(var_heights[:, ts])

                    # save the average of the average height values we have at each timestep (created by different runs)
                    avg_avg_height[ts] = np.average(avg_heights[:, ts])
                    avg_avg_mass[ts] = np.average(avg_masses[:, ts]) 
                    avg_avg_elong[ts]  = np.average(avg_elongs[:, ts])
                    avg_avg_net_prod[ts] = np.average(avg_net_prods[:, ts])

                    avg_var_height[ts] = np.average(var_heights[:, ts])
                    avg_var_mass[ts] = np.average(var_masses[:, ts])
                    
                
                # RETURN (mean band, std band)
                return avg_avg_height, std_avg_height, avg_avg_mass, std_avg_masses, avg_avg_elong, std_avg_elong, avg_avg_net_prod , std_avg_net_prod, avg_var_height, std_var_height, avg_var_mass, std_var_mass
            
            # if there was passed an object that is not a simulation obejct
            elif not(isinstance(simulation, Simulation)):
                print(f'Statistics.get_means_and_bands(): Wrong type of simulation. Expected None or Simualtion but got {type(simulation)}.\n')
            
# ######### PREPARATION PLOTTING ##############################

    def extend_data_to_heat_map_data(self, mass_height_data:np.ndarray):
        number_rows = len(mass_height_data[:,0])
        number_of_spots = len(mass_height_data[0,:])
        
        # double the "pixels" plus one for half offset of the rows 
        data_for_image = np.zeros((number_rows * 2, number_of_spots * 2 + 1))

        # fill the data_for_image array with the values of the data
        # This will make one spot in the original data four spots large
        # 
        # [v1][v2] -> [v1][v1][v2][v2][wh]
        #  [v3][v4]   [wh][v3][v3][v4][v4]
        # 

        # spaceholder for white values
        white = -1.0

        # make all entries white in the new array
        data_for_image[:,:] = white

        for row in range(number_rows):
            for spot in range(number_of_spots):
                # fill four fields, with offset for uneven rows
                data_for_image[2*row : 2*row + 2 , 
                               (row % 2) + spot*2: (row % 2) + spot*2 +2] = mass_height_data[row, spot]
        
        # return data made for the heatmap with offset
        return data_for_image
            
######### PLOTTING ##########################################

    def plot_average_height_masses(self, averages_height=None, averages_mass=None, fig=None, ax=None, width_plot=10, height_plot=6, instant_plot=False, show_legend=True, plt_water_and_shade = False):
        
        # Calculate the series of averages if not passed
        if averages_height==None or averages_mass==None:
            averages_height, averages_mass, averages_water , averages_ext_shade = self.get_time_series_of_averages()
        
        # timestep interval
        timesteps = np.arange(len(averages_height))
        
        weights_for_different_variables = self.get_weights_for_different_variables()
        
        # plot
        if fig==None or ax==None:
            fig, ax = plt.subplots(figsize=(width_plot,height_plot))
        ax.plot(timesteps, averages_height * weights_for_different_variables['weight_height'], label= f'Average Height of plants (factor {weights_for_different_variables['weight_height']}) [cm]')
        # ax.plot(timesteps, averages_height, label='Average Height of plants [cm]')

        ax.plot(timesteps, averages_mass * weights_for_different_variables['weight_mass'], label=f'Average mass of plants (factor {weights_for_different_variables['weight_mass']})[mg]')
        # ax.plot(timesteps, averages_mass, label='Average mass of plants [mg]')


        if plt_water_and_shade:
            ax.plot(timesteps, averages_water * 0.5, label='Average Height of water (factor 0.5)')
            ax.plot(timesteps, averages_ext_shade, label='Average External shade')
        ax.set_xlabel('Timesteps [days]')
        ax.set_ylabel('Numerical units')

        ax.set_ylim((0.0,10.0))
        
        # show legend if wanted
        if show_legend:
            plt.legend()

        # Plot if desired
        if instant_plot:
            plt.show()
        
        # return figure and axis object
        return fig, ax

    def plot_variance_height_masses(self, variances_height=None, variances_mass=None, fig=None, ax=None, width_plot=10, height_plot=6, instant_plot=False, show_legend=True):
        
        
        # Calculate the series of averages if not passed
        if variances_height==None or variances_mass==None:
            variances_height, variances_mass, variances_water , variances_ext_shade = self.get_time_series_of_variances()
        
        # timestep interval
        timesteps = np.arange(len(variances_height))
        
        # get the weights for the different scales in plotting
        weights_for_different_variables = self.get_weights_for_different_variables()

        # new plot if there are no fig and ax objects
        if fig==None or ax==None:
            fig, ax = plt.subplots(figsize=(width_plot,height_plot))

        ax.plot(timesteps, variances_height * weights_for_different_variables['weight_var_height'], label=f'Variances Height of plants (factor {weights_for_different_variables['weight_var_height']})[cm²]')
        # ax.plot(timesteps, averages_height, label='Average Height of plants [cm]')
        ax.plot(timesteps, variances_mass * weights_for_different_variables['weight_var_mass'], label=f'Variances mass of plants (factor {weights_for_different_variables['weight_var_mass']})[mg²]')
        # ax.plot(timesteps, averages_mass, label='Average mass of plants [mg]')

        ax.set_xlabel('Timesteps [days]')
        ax.set_ylabel('Numerical units')

        ax.set_ylim((0.0,10.0))
        
        # show legend if wanted
        if show_legend:
            plt.legend()

        # Plot if desired
        if instant_plot:
            plt.show()
        
        # return figure and axis object
        return fig, ax
        
    def plot_average_elong_and_net_prod(self, average_elong_series=None, average_net_prod_series=None, fig=None, ax=None, width_plot=10, height_plot=6, instant_plot=False, show_legend=True):
        
        # Calculate the series of averages if not passed
        if average_elong_series==None or average_net_prod_series==None:
            average_elong_series, average_net_prod_series = self.get_time_series_of_average_elongation_and_mass()
        
        # timestep interval
        timesteps = np.arange(len(average_elong_series))
        
        # get the weights for the different scales in plotting
        weights_for_different_variables = self.get_weights_for_different_variables()

        # new plot if there are no fig and ax objects
        if fig==None or ax==None:
            fig, ax = plt.subplots(figsize=(width_plot,height_plot))

        # plot average elongation and net productivity
        ax.plot(timesteps, average_elong_series * weights_for_different_variables['weight_avg_elong'], label=f'Average elongation (factor {weights_for_different_variables['weight_avg_elong']})[cm/d]')
        ax.plot(timesteps, average_net_prod_series * weights_for_different_variables['weight_avg_net_prod'], label=f'Average net productivity (factor {weights_for_different_variables['weight_avg_net_prod']})[mg/d]')

        ax.set_xlabel('Timesteps [days]')
        ax.set_ylabel('Numerical units')

        ax.set_ylim((-10.0,10.0))
        
        # show legend if wanted
        if show_legend:
            plt.legend()

        # Plot if desired
        if instant_plot:
            plt.show()
        
        # return figure and axis object
        return fig, ax
        
    def plot_heatmap_height_at(self, species, timestep: int, fig=None, ax=None, instant_plot = False):
        # update species
        self.set_species(species)

        # Check, if timesteps is referencable
        if (0 <= timestep < self.get_timesteps() + 1):
            # Make Heatmap

            # Get data at specific timestep
            height_data = self.get_results_height()[timestep]
            
            # if no fig, ax object was passed, create new
            if fig == None or ax == None:
                fig, ax = plt.subplots()

            # make data from the height data for the heatmap to display the offset
            image_height_data = self.extend_data_to_heat_map_data(height_data)
            
            # make image
            im = ax.imshow(image_height_data, cmap = colormaps.get_cmap('Greens'))
            
            # get number of spots and rows
            num_rows, num_spots = height_data.shape

            # X ticks at center of each 2×2 block (base row)
            x_tick_positions = 2*np.arange(num_spots) + 0.5
            x_tick_labels    = np.arange(num_spots)

            # Y ticks at centers
            y_tick_positions = 2*np.arange(num_rows) + 0.5
            y_tick_labels    = np.arange(num_rows)

            # Show all ticks and label them with the respective list entries
            ax.set_xticks(x_tick_positions, labels=x_tick_labels, # spots
                        rotation=45, ha="right", rotation_mode="anchor")
            ax.set_yticks(y_tick_positions, labels=y_tick_labels) # rows

            # Loop over data dimensions and create text annotations.
            for i in range(len(height_data[:,0])): # rows
                for j in range(len(height_data[0])): # spots
                    text = ax.text((i % 2) + j * 2 + 0.5, i * 2 + 0.5, np.round(height_data[i, j], decimals=2),
                                ha="center", va="center", color="w")

            # ax.set_title(f"Height of $\\mathit{{S.\\ {self.get_species()}}}$ after {timestep} timesteps")
            ax.set_ylabel('Rows')
            ax.set_xlabel('Spots in row')
            # fig.tight_layout()
            if instant_plot:
                plt.show()

            return fig, ax
        else:
            print(f'Heatmap failed. Timestep {timestep} is out of bounds: Has to be between 0 and {self.get_timesteps()}.')
 
    def plot_heatmap_masses_at(self, species, timestep: int, fig=None, ax=None, instant_plot = False):
       
        # update species
        self.set_species(species)

        # Check, if timesteps is referencable
        if (0 <= timestep < self.get_timesteps() + 1):
            # Make Heatmap

            # Get data at specific timestep
            mass_data = self.get_results_mass()[timestep]
            
            # if no fig, ax object was passed, create new
            if fig == None or ax == None:
                fig, ax = plt.subplots()
            
            # make data from the height data for the heatmap to display the offset
            image_mass_data = self.extend_data_to_heat_map_data(mass_data)

            im = ax.imshow(image_mass_data, cmap=colormaps.get_cmap('Greens'))

            # get number of spots and rows
            num_rows, num_spots = mass_data.shape

            # X ticks at center of each 2×2 block (base row)
            x_tick_positions = 2*np.arange(num_spots) + 0.5
            x_tick_labels    = np.arange(num_spots)

            # Y ticks at centers
            y_tick_positions = 2*np.arange(num_rows) + 0.5
            y_tick_labels    = np.arange(num_rows)

            # Show all ticks and label them with the respective list entries
            ax.set_xticks(x_tick_positions, labels=x_tick_labels, # spots
                        rotation=45, ha="right", rotation_mode="anchor")
            ax.set_yticks(y_tick_positions, labels=y_tick_labels) # rows


            # Loop over data dimensions and create text annotations.
            for i in range(len(mass_data[:,0])): # rows
                for j in range(len(mass_data[0])): # spots
                    text = ax.text((i % 2) + j*2 + 0.5, i*2 + 0.5, np.round(mass_data[i, j], decimals=2),
                                ha="center", va="center", color="w")

            # ax.set_title(f"Mass of $\\mathit{{S.\\ {self.get_species()}}}$ at timestep {timestep}")
            ax.set_ylabel('Rows')
            ax.set_xlabel('Spots in row')
            fig.tight_layout()
            if instant_plot:
                plt.show()
            return fig, ax
        else:
            print(f'Heatmap failed. Timestep {timestep} is out of bounds: Has to be between 0 and {self.get_timesteps()}.')

    def plot_water_height(self, fig=None, ax=None, width_plot=10, height_plot=3, instant_plot=False, show_legend=True, mark_where_constant=False, plot_zero = True):
        
        # plot
        if fig==None or ax==None:
            fig, ax = plt.subplots(figsize=(width_plot,height_plot))

        # load the averages
        averages_height, averages_mass, averages_water , averages_ext_shade = self.get_time_series_of_averages()

        # timestep interval
        timesteps = np.arange(len(averages_height))
        
        # plot average water table
        ax.plot(timesteps[1:], averages_water[1:], label='Avg. height water table [cm]', c='darkblue')

        # plot the boundaries at which the polynomial function take constants
        if mark_where_constant:
            ax.plot(timesteps,  np.zeros(len(averages_height)), label='upper bound water table', c='Grey', alpha=0.7)
            ax.plot(timesteps, np.zeros(len(averages_height)) - 15, label='lower bound water table', c='Grey', alpha = 0.7)

        # plot zero if desired
        if plot_zero:
            ax.plot(timesteps, np.zeros(len(timesteps)), label='Height of reference', linestyle ='--', c='#6B8FBF')

        # make x label and y label
        ax.set_xlabel('Timesteps')
        ax.set_ylabel('Height [cm]')

        # return values
        return fig, ax

    def plot_means_and_bands_of_runs(self, simulation, plt_height = True, plt_mass = True, plt_elong = True, plt_net_prod = True, plt_var_height=True, plt_var_mass = True, scaling = False, constant_watermap = None, water_table_series = None, number_of_runs=1.0, adapt_water_table_height_to_average_carpet_height = False, adapted_depth_below_average_carpet_height=0.0, timesteps: int=None, fig=None, ax=None, length_color=(0.29, 0.0, 0.51), mass_color = "#3D632F", elongation_color = "#A671A2", net_prod_color = "#7FBE82"):
    
        '''
        Plots the averages of several runs for each timestep together with an 2 std band
        '''
        # update species for plots
        self.set_species(simulation.get_species())

        # get timesteps from class if none was passed
        if timesteps == None:
            timesteps = self.get_timesteps()

        # load data
        avg_avg_height, std_avg_height, avg_avg_masses, std_avg_masses, avg_avg_elong, std_avg_elong, avg_avg_net_prod , std_avg_net_prod, avg_var_height, std_var_height, avg_var_mass, std_var_mass = self.get_means_and_bands_from_simulation(simulation=simulation, water_table_series=water_table_series, adapt_water_table_height_to_average_carpet_height=adapt_water_table_height_to_average_carpet_height, adapted_depth_below_average_carpet_height=adapted_depth_below_average_carpet_height, number_of_runs=number_of_runs, constant_watermap=constant_watermap)
        
        print(f'Avg height: {avg_avg_height[359]}, Avg_mass: {avg_avg_masses[359]}')
        print(f'avg_avg_height.shape: {avg_avg_height.shape}')
        # plot
        if fig==None or ax==None:
            fig, ax = plt.subplots()

        # scale, if wanted, like in FIGURE 6
        sh = 1.0
        sm = 1.0
        se = 1.0
        snp = 1.0
        svh = 1.0
        svm = 1.0

        # scales if wanted
        if scaling:
            sh = self.get_weights_for_different_variables()['weight_height']
            sm = self.get_weights_for_different_variables()['weight_mass']
            se = self.get_weights_for_different_variables()['weight_avg_elong']
            snp = self.get_weights_for_different_variables()['weight_avg_net_prod']
            svh = self.get_weights_for_different_variables()['weight_var_height']
            svm = self.get_weights_for_different_variables()['weight_var_mass']
        
        # Length
        if plt_height:
            ax.fill_between(np.arange(0,timesteps + 1), (avg_avg_height + 2 * std_avg_height) * sh, (avg_avg_height - 2 * std_avg_height) * sh, alpha=.15, linewidth=0, color=length_color)
            ax.plot(np.arange(0,timesteps + 1), avg_avg_height * sh, linewidth=2, label='Height [cm]', c=length_color)
            
        # Mass
        if plt_mass:
            ax.fill_between(np.arange(0,timesteps + 1), (avg_avg_masses + 2 * std_avg_masses) * sm, (avg_avg_masses - 2 * std_avg_masses) * sm, alpha=.15, linewidth=0, color=mass_color)
            ax.plot(np.arange(0,timesteps + 1), avg_avg_masses * sm, linewidth=2, label='Mass [mg]', c=mass_color)
            
        # Elongation
        if plt_elong:
            ax.fill_between(np.arange(0,timesteps + 1), (avg_avg_elong + 2 * std_avg_elong) * se, (avg_avg_elong - 2 * std_avg_elong) * se, alpha=.15, linewidth=0, color=elongation_color)
            ax.plot(np.arange(0,timesteps + 1), avg_avg_elong * se, linewidth=2, label='Height growth rate [cm / d]', c=elongation_color)
            
        # Net prod
        if plt_net_prod:
            ax.fill_between(np.arange(0,timesteps + 1), (avg_avg_net_prod + 2 * std_avg_net_prod) * snp, (avg_avg_net_prod - 2 * std_avg_net_prod) * snp, alpha=.15, linewidth=0, color=net_prod_color)
            ax.plot(np.arange(0,timesteps + 1), avg_avg_net_prod * snp, linewidth=2, label='Mass growth rate [mg / d]', c=net_prod_color)

        # Var height
        if plt_var_height:
            ax.fill_between(np.arange(0,timesteps + 1), (avg_var_height + 2 * std_var_height) * svh, (avg_var_height - 2 * std_var_height) * svh, alpha=.15, linewidth=0, color=elongation_color)
            ax.plot(np.arange(0,timesteps + 1), avg_var_height * svh, linewidth=2, label='Variance height cm$^2$', c=elongation_color, linestyle='--')
        
        # Var mass
        if plt_var_mass:
            ax.fill_between(np.arange(0,timesteps + 1), (avg_var_mass + 2 * std_var_mass) * svm, (avg_var_mass - 2 * std_var_mass) * svm, alpha=.15, linewidth=0, color=net_prod_color)
            ax.plot(np.arange(0,timesteps + 1), avg_var_mass * svm, linewidth=2, label='Variance mass mg$^2$', c=net_prod_color, linestyle='--')
         
        # ax.set_xlabel('Timesteps')
        ax.set_ylabel('Numerical Units')
        

        return fig, ax, self.get_species()