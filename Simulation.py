from Environment import Environment
from Map import Plantmap, Watermap, Shademap
from Plant import Plant
from Growth_Processes_Model import Growth_Processes_Model
import time

import numpy as np

class Simulation:
    # TODO:
    #    - Seperate, what shall be inside Statistics, what inside Simulation run
    #    - Make Simulation pass only everything, that is needed to make Environment, Map and Plant objects and params and timesteps
    #    - Make some method that runs everything for the duration of timesteps
    #    - 
    def __init__(self, timesteps, params, initial_water_map:Watermap=None, initial_external_shade_map:Shademap=None, environment:Environment=None, init_species = 'capillifolium', init_mode_heights : str = ''):
        '''
        ## DESCRIPTION
        Sets up a simulation with a certain Environment object. If no species is given, capillifolium will be passed to the Plantmap object initially.

        ## PARAMS
        - timesteps, Integer: the number of timesteps we want to simulate
        - params, dictionary: should contain
                - params['width'], positive Integer:  number of spots in one row we want to create in our Environment object
                - params['height'], positive Integer: number of rows we want to create in our Environment object
                - params['INIT_MODE'], String: string that determines the initial distribution of plant heights, e.g. 'NORM_DIST' or 'UNIFORM'
                - params['init_mean'], float: determines the mean of the distribution chosen by params['INIT_MODE']
                - params['init_std'], nonegative float: determines the standard deviation of the distribution chosen by params['INIT_MODE'], if applicable
        - species, String: Default capillifolium, but can be 'papillosum', too. Defines, which species lawn we want to create
        - init_modes_height, str: determines the initial distribution of the heights in the newly created Plantmap in run() if there has not been given a initial plantmap. See Plantmap._set_up() for more
        '''
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
            print('Simulation.__init__(): Successfully initiated params')
            self._init_species = init_species

            self._init_mode_heights = init_mode_heights
        
            # boolean to check, whether an Environment object is referenced
            self._environment_attribute_referenced = False

            # save the number of timesteps
            self._timesteps = timesteps

            # save params
            self._params = params

            # save Initial watermap
            self._initial_watermap = initial_water_map

            # save initial shademap
            self._initial_external_shademap = initial_external_shade_map

            # make a container for the results
            number_of_spots_per_row = params['number_of_spots_per_row']
            number_of_rows = params['number_of_rows']

            # make the threedimensional np.array
            self._results_heights = np.zeros((timesteps+1, number_of_rows, number_of_spots_per_row))
            self._results_masses = np.zeros((timesteps+1, number_of_rows, number_of_spots_per_row))
            self._results_water = np.zeros((timesteps+1, number_of_rows, number_of_spots_per_row))
            self._results_shade = np.zeros((timesteps+1, number_of_rows, number_of_spots_per_row))

            # make an Environment object if by deafult there is none passed
            if environment==None:
                # Default case
                self._environment = Environment(species=init_species, number_of_rows = number_of_rows, spots_per_row = number_of_spots_per_row, init_mode_height=params['INIT_MODE'], mean_height=params['init_mean'], std=params['init_std'])
            else:
                # CHECK row and column number of the passed environment object 
                if not(environment.get_number_of_rows()==self._params['number_of_rows'] and environment.get_number_of_plants_in_one_row()==self._params['number_of_spots_per_row']):
                    # If not the right dimensions
                    self._environment = Environment(number_of_rows = number_of_rows, spots_per_row = number_of_spots_per_row, init_mode_height=params['INIT_MODE'], mean_height=params['init_mean'], std=params['init_std'], species=init_species)
                    print(f'Simulation.__init__(): FAILURE: Passed Custom Environment object is not having the right dimension.\nDimesnions (rows, spots): {(environment.get_number_of_rows(), environment.get_number_of_plants_in_one_row())}\nNeeded (rows, spots): {(self._params['number_of_rows'], params['number_of_spots_per_row'])} \nAnother new Environment was created.')

                # if we had the right dimensions
                elif (environment.get_number_of_rows()==self._params['number_of_rows'] and environment.get_number_of_plants_in_one_row()==self._params['number_of_spots_per_row']):
                    # take the passed environment object
                    self._environment = environment
                
            # # Add Environment to all plants in Plantmap
            self._environment.add_environment_to_plants_and_tell_neighbors()

            # Update, that we have an environment object
            self._environment_attribute_referenced = True

            # if initial map for water was passed, set it in environment
            if not initial_water_map == None:
                # FIXME: Delete this line
                print(f'Simulation.__init__(): Initial watermap: {initial_water_map.get_items()}')

                self._environment.set_watermap(watermap=initial_water_map)

            # if initial map for water was passed, set it in environment
            if not initial_external_shade_map == None:
                self._environment.set_shademap(shademap=initial_external_shade_map)

            # Print Status
            print(f'Simulation.__init__():\nSuccessfully initiated simulation with parameters:\n{params}')

            # return environment object?
            # return self._environment

        else:
            print(f'Simulation.__init__(): Something was wrong about the parameter dictionary: \n{params}.')
           
    ##### CHECKER #################################

    def check_for_environment(self):
        '''
        A method to check, whether a Environment object has been referenced to the Statistics object.
        Returns True, if Statistics already has an environment object referenced.
        Returns False, if it does not.
        Usually we could just use the get_is_environement_attribute_referenced() method.
        But I wanted to implement a dedicated method to be able to modify the process of checking the environment object eventually.
        '''
        # check the _environment
        if isinstance(self._environment, Environment):

            # return True for a adequate Environment object
            return True
        
        # if there is no Environment object referenced
        else:
            print(f'Simulation.check_for_environment(): No Environment class attribute. \nDo Simulation.set_environment().')
            return False

    ##### GETTER ##################################
    def get_init_mode_heights(self):
        '''
        self._init_modes_height, str: determines the initial distribution of the heights in the newly created Plantmap in run() if there has not been given a initial plantmap for this run (this how normal distribution for plants heights are created). See Plantmap._set_up() for more
        '''
        return self._init_mode_heights

    def get_species(self):
        return self._init_species

    def get_params(self):

        # return private object params
        return self._params

    def get_is_environement_attribute_referenced(self):
        '''
        Returns the boolean that reflects whether we have already referenced an environment object or not
        '''
        return self._environment_attribute_referenced

    def get_environment(self):
        '''
        Returns the Environment attribute and checks, whether there is one
        '''
        # in the case of a proper environment attribute
        if self.check_for_environment():

            # return the Environment object
            return self._environment
        
        # if we have another improper attribute
        else:
            print(f'Statistics.get_environment(): Returned None as there is no Statistics._environment() object fulfilling Statistics.check_for_environment().\nAn environment object has to be passed to the Statistics object.')
            return None

    def get_initial_watermap(self):
        return self._initial_watermap
    
    def get_initial_external_shademap(self):
        return self._initial_external_shademap
  
    def get_timesteps(self):
        return self._timesteps
    #### SETTER ###################################
    def set_init_mode_height(self, init_mode_heights:str):
        '''
        ## Return
        init_modes_height, str: determines the initial distribution of the heights in the newly created Plantmap in run() if there has not been given a initial plantmap. See Plantmap._set_up() for more
        '''
        self._init_mode_heights = init_mode_heights

    def set_species(self, species: str):
        if species in ['capillifolium', 'papillosum']:
            self._init_species = species
        
        else:
            print(f'Simulation.set_species(): {species} is not recognized as a valid species name. We need \'capillifolium\' or \'papillosum\'')

    def set_params(self, params):
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
            print('Simulation.set_params(): Successfully set params')
        
        # set params
        self._params = params

    def set_environment(self, environment):
        '''
        Sets the environment after a check for
        - object type of environment
        - if there already is an environment object

        PARAMS
        - environment, Environment object:  The new environment object to be referenced
        '''
        # check for already existing environment attribute
        if self.check_for_environment():

            # if there is already a proper environment object
            print(f'Simulation.set_environment(): \nNo environment attribute was updated. There already exists one')

        elif(not isinstance(environment, Environment)):

            # if we do not get a Environment object
            print(f'Simulation.set_environment(): \nNo environment attribute was updated. \nExpected Environment object as an argument, but received a {type(environment)} object')
        
        else:

            # if everything is okay update environment attribute
            self._environment = environment

    def set_environment_referenced(self, value: bool):
        '''
        Sets the boolean that reflects whether we have already referenced an environment object or not.
        '''
        # TODO: Think about whether this should be only possible, if we have not yet referenced a Environment object
        self._environment_attribute_referenced = value

    def set_initial_watermap(self, initial_watermap):
        self._initial_watermap = initial_watermap

    def set_initial_external_shademap(self, initial_external_shademap):
        self._initial_external_shademap = initial_external_shademap
    ######### METHODS #######################################################

    def load_water_values(self):
        '''
        Returns the watermaps values for water table heights saved in environement if existing
        '''
        if self.check_for_environment():
            # access water map values
            water_values = self.get_environment().get_watermap().get_items()

            # return
            return water_values
        
        # if there is no proper Environment object
        else:
            print(f'Simulation.load_water_values(): No water values could be loaded.')
    
    def load_shade_values(self):
        '''
        Returns the shademaps values for external shade saved in environment if existing
        '''
        if self.check_for_environment():

            # access water map values
            shade_values = self.get_environment().get_shademap().get_items()

            # return
            return shade_values
        
        # no proper environment attribute
        else:
            print(f'Simulation.load_shade_values(): No shade values could be loaded.')
    
    def load_plants_height_and_masses_values(self):
        '''
        Returns the heights and masses of the plants saved in environment.plantmap() if existing
        '''
        if self.check_for_environment():

            # access plant height and masses values
            plant_heights, plant_masses = self.get_environment().get_plantmap().get_heights_and_mass()

            # return heights and masses
            return plant_heights, plant_masses
        
        # no proper environment attribute
        else:
            print(f'Simulation.load_shade_values(): No plant heights and masses could be loaded.')

    def run(self, initial_plantmap:Plantmap | None = None, constant_watermap:Watermap=None, constant_shademap:Shademap=None, watermap_series=None, shademap_series=None, print_log = False, adapt_water_table_height_to_average_carpet_height=False, adapted_depth_below_average_carpet_height:float | int = 0.0, k_prod = -1.39, k_elong = -1.39):
        '''
        ## RETURN  
        Returns four 3D numpy arrays with results for all timesteps for each height, mass, external shade and water-table depth
        Runs a simulation for the number of timesteps given in self._timesteps.
        It measures the runtime, 
        creates multiple 3D np.arrays to save all the twodimensional results of water, shade and growth (height and mass) according to the shape of environment (which is again defined by the Simulation object),
        runs environment.grow_all_plants(optional_watermap, optional_shademap) and saves the results here for each timestep.
        Prints a short summary of the results.

        ## PARAMETER
        constant_watermap: *Watermap*  
        If None, a constant watermap with water table of height 0.0 will be used for all timesteps.  
        If a watermap with constant values shall be used for all timesteps, this map will be used.  
        If, additionally, a watermap _series_ (`watermap_series`) is given, then `constant_watermap` can function as the initial condition.  
        To achieve this case the `len(watermap_series)` should be equal to `Environment.get_timesteps()` and not `Environment.get_timesteps() + 1`).

        constant_shademap: *Shademap*  
        If None, a constant shademap with external shade of 0.0 will be used for all timesteps.  
        If a shademap, representing the external shade at each spot, with constant values shall be used for all timesteps, this map will be used.  
        If, additionally, a shademap _series_ (`shademap_series`) is given, then `constant_shademap` can function as the initial condition.   
        To achieve this case the `len(shademap_series)` should be equal to `Environment.get_timesteps()` and not `Environment.get_timesteps() + 1`).

        watermap_series: *Series of watermaps*
        Length of `Environment.get_timesteps()` or `Environment.get_timesteps() + 1` needed.   
        In the first case, if constant_watermap is given, the constant_watermap will be used as the initial condition.
        If passed, the entries of this series will be used for each timestep as the watermap (representing the water-table height above an arbitrary zero).  

        shademap_series: *Series of shademaps*
        Length of `Environment.get_timesteps()` or `Environment.get_timesteps() + 1` needed.   
        In the first case, if constant_shademap is given, the constant_shademap will be used as the initial condition.
        If passed, the entries of this series will be used for each timestep as the shademap (representing the external shade caused by vascular plants).  

        adapt_water_table_height_to_average_carpet_height: *bool*, Default: False.  
        If True, the water-table height is set to the average moss carpet height minus `adapted_depth_below_average_carpet_height`.
        So if `adapted_depth_below_average_carpet_height = 3.0`the water-table will always be three cm below the average moss carpet height.
        Basically, we more or less assure certain water availability.

        adapted_depth_below_average_carpet_height, *float* or *int*, Default=0.0  
        If `adapt_water_table_height_to_average_carpet_height=True` then this value determines, how far below the average carpet height the water table will be for aech timestep.  
        So if `adapted_depth_below_average_carpet_height = 3.0`the water-table will always be three cm below the average moss carpet height.
        Basically, we more or less assure certain water availability.

        k_elong, *float*, Default = -1.39 (calue from the paper Hayward and Clymo, 1983)
        Defines the parameters of all plants in the environment for the exposure effect modulation regarding mass growth. 
        This effects models, how well are plants growing if they exceed the average moss carpet height (approximated by average height of the neighborhood).
        The exposure effect is respected by multiplying the growth values by the value obtained by the exposure effect (a exponential function with height above average carpet height).
        This parameter determines the steepness of the exponential function: Negative values punish, positive values support the growth, if the plant grew heigher than its neighbors.
        
        k_prod, *float*, Default = -1.39 (calue from the paper Hayward and Clymo, 1983)
        Defines the parameters of all plants in the environment for the exposure effect modulation regarding height growth. 
        This effects models, how well are plants growing if they exceed the average moss carpet height (approximated by average height of the neighborhood).
        The exposure effect is respected by multiplying the growth values by the value obtained by the exposure effect (a exponential function with height above average carpet height).
        This parameter determines the steepness of the exponential function: Negative values punish, positive values support the growth, if the plant grew heigher than its neighbors.
        '''
        # save starting point
        start_time_stamp = time.time()

        # A boolean that will save, whether we want to use dynamical values for water-table depth
        use_dyn_water_table_height = False

        # A boolean that will save, whether we want to use dynamical values for external shade
        use_dyn_external_shade = False

        # make the threedimensional np.array with the same shape as environment and the maps
        self._results_heights = np.zeros((self._timesteps+1, self.get_environment().get_number_of_rows(), self.get_environment().get_number_of_plants_in_one_row()))
        self._results_masses = np.zeros((self._timesteps+1, self.get_environment().get_number_of_rows(), self.get_environment().get_number_of_plants_in_one_row()))
        self._results_water = np.zeros((self._timesteps+1, self.get_environment().get_number_of_rows(), self.get_environment().get_number_of_plants_in_one_row()))
        self._results_shade = np.zeros((self._timesteps+1, self.get_environment().get_number_of_rows(), self.get_environment().get_number_of_plants_in_one_row()))

        # Check for initiation of environment
        if not self.check_for_environment():
            print(f'Simulation.run(): Create new Environment object for Simulation')
            # make new environment object
            initial_environment = Environment(species = self.get_species(), number_of_rows = self.get_params()['number_of_rows'], number_of_spots_per_row = self.get_params()['number_of_spots_per_row'], init_mode_height=self.get_params()['INIT_MODE'], mean_height=self.get_params()['init_mean'], mean_std=self.get_params['init_std'])
            self.set_environment(initial_environment)
        else:
            print(f'Simulation.run(): There already is a environment object.')

        ##### PLANTMAP: ############################################################
        ##### Create new one to start with if none was passed by making new Environment ######################
        if initial_plantmap == None:
            print(f'Simulation.run(): Created new Plantmap with species {self.get_species()}.')
            new_plantmap = Plantmap(species = self.get_species(), number_of_rows = self.get_params()['number_of_rows'], number_of_spots_per_row = self.get_params()['number_of_spots_per_row'], items = None)
            new_plantmap.set_up(self.get_species(), init_mode_height=self.get_params()['INIT_MODE'], mean_height=self.get_params()['init_mean'], std=self.get_params()['init_std'])
            
            # Set new plantmap with newly created Plants (so e.g. masses of plants are zero, heights are distributed around 0)
            self.get_environment().set_plantmap(new_plantmap)
            
            # set up neighborhood relations and reference all plants to its new environment
            self.get_environment().add_environment_to_plants_and_tell_neighbors()
        else:
            print(f'Simulation.run(): Using the passed initial plantmap object.')
            # If a initial plant map has been passed, RESET environment
            self.get_environment().set_plantmap(initial_plantmap)

        ## WATERMAP: DYNAMICAL OR NOT ###########################################

        # If we just want constant water tables 
        if not constant_watermap==None:
            # print
            print(f'Simulation.run(): We use constant watermap of values: {constant_watermap.get_items()}')

            # update map object in environment
            self.get_environment().set_watermap(constant_watermap)

            # FIXME: Delete this line
            print(f'Simulation.run(): The environment updated constant watermap to: {self.get_environment().get_watermap().get_items()}')

        # if we want to use a time series of water table-heights
        if not watermap_series == None:

            # check for length
            if not (len(watermap_series) == (self.get_timesteps() + 1) or len(watermap_series) == (self.get_timesteps())): # + 1 due to the initial condition
                
                # print Warning
                print(f'Simulation.run(): Passed watermap_series for dynamical values has len: {len(watermap_series)}. \n But len({self.get_timesteps()} or len({self.get_timesteps() + 1}) (if you are also passing a constant_map object as the initial condition) is needed)')
            
                # update the use of dynamical water tables: It is not used
                use_dyn_water_table_height = False

            # if length is equal to timesteps, so the initial cndition is missing, we will treat constant_watermap, if existing, as the initial condition
            elif len(watermap_series) == (self.get_timesteps()):

                # if we have a constant map then use it as initial map
                if isinstance(constant_watermap, Watermap):
                    print(f'Simulation.run(): Set constant watermap as the initial condition, as len(water_map_series) = timesteps ({len(watermap_series)} = {self.get_timesteps()}))')
                    # make the constant map the initial condition
                    
                    # update map object in environment
                    self.get_environment().set_watermap(constant_watermap)

                    # extend series by initial condition
                    watermap_series = [constant_watermap] + watermap_series

                    # update the use of timeseries
                    use_dyn_water_table_height = True
                
                # if there is no
                elif not isinstance(constant_watermap, Watermap):

                    # take the first entry of the watermap series and make it the initial condition for water
                    watermap_series = [watermap_series[0]] + watermap_series

                    # update map object in environment
                    self.get_environment().set_watermap(watermap_series[0])

                    # update the use of timeseries
                    use_dyn_water_table_height = True

                    print(f'Simulation.run(): Dynamical Watermap is used. First entry of the series will additionally be the inital condition. ({len(watermap_series)} = {self.get_timesteps()} + 1))')



            # if we do got exactly the timetspes+1 length
            elif len(watermap_series) == (self.get_timesteps() + 1):
                  
                  print(f'Simulation.run(): Dynamical Watermap is used. First entry of the series will be the inital condition. ({len(watermap_series)} = {self.get_timesteps()}))')

                  # get first entry as the initial condition
                  initial_water_heights = watermap_series[0]

                  # set watermap in environment
                  self.get_environment().set_watermap(initial_water_heights)

                  # update the use of timeseries
                  use_dyn_water_table_height = True
            
            else:
                print(f'Simulation.run(): Dynamical watermap is used, but none of the cases was applied.')

        else:
            # print()
            print(f'SIMULATION.run(): No dynamical watermap series is used')

        ## SHADEMAP: DYNAMICAL OR NOT ###########################################

        # If we just want constant water tables 
        if not constant_shademap==None:

            # update map object in environment
            self.get_environment().set_shademap(constant_shademap)

        # if we want to use a time series of water table-heights
        if not shademap_series == None:

            # check for length
            if not (len(shademap_series) == (self.get_timesteps() + 1) or len(shademap_series) == (self.get_timesteps())): # + 1 due to the initial condition
                
                # print Warning
                print(f'Simulation.run(): Passed shademap_series for dynamical values has len: {len(shademap_series)}')

                # update use of dynamical values: NOT USED
                use_dyn_external_shade = False
            
            # if length is equal to timesteps, so the initial condition is missing, we will treat constant_shademap, if existing, as the initial condition
            elif len(shademap_series) == (self.get_timesteps()) and (not constant_shademap == None):
                # TODO: Make this case split up like for watermap
                print(f'Simulation.run(): Set constant shademap as the initial condition, as len(shade_map_series) = timesteps ({len(shademap_series)} = {self.get_timesteps()}))')

                # make the constant map the initial condition
                # update map object in environment
                self.get_environment().set_shademap(constant_shademap)

                # extend series by initial condition
                shademap_series = [constant_shademap] + shademap_series

                # update use of dynamical values: USED
                use_dyn_external_shade = True

            # if we do got exactly the timetspes+1 length
            elif len(shademap_series) == (self.get_timesteps() + 1):
                  
                print(f'Simulation.run(): Dynamical Shademap is used. First entry of the series will be the inital condition. ({len(shademap_series)} = {self.get_timesteps()}))')

                # get first entry as the initial condition
                initial_external_shades = shademap_series[0]

                # set watermap in environment
                self.get_environment().set_shademap(initial_external_shades)

                # update use of dynamical values: USED
                use_dyn_external_shade = True

        #### END OF CHECK FOR CONSTANT OR DYNAMICAL VALUES FOR WATER AND EXTERNAL SHADE #####################

        # save initial conditions (watermap and shademap in environment are now
        # 1. just 0.0, if no constant_map, or time series or both have been passed
        # 2. just a constant, defined by constant_Xmap, if no Xseries have been passed or one of length timesteps instead of timesteps + 1
        # 3. the first entry of the timeseries of Xseries if length was equal to timesteps + 1

        #### CHECK FOR ADAPTIVE WATERMAP and set to this water level if wanted ####################################################################
        if adapt_water_table_height_to_average_carpet_height:
            current_height, current_mass_values = self.load_plants_height_and_masses_values()
            cur_average_carpet_height = np.average(current_height)
            items_below_carpet = np.zeros_like(self.get_environment().get_watermap().get_items()) + cur_average_carpet_height - adapted_depth_below_average_carpet_height
            # set the height of the water table 3cm below the mean surface level (like probably described in Table 5, C(5))
            # cur_water_map_fig_6.set_up(constant_value=cur_average_carpet_height - adapted_depth_below_average_carpet_height)
            self.get_environment().get_watermap().set_items(items_below_carpet)
        
        water_heights = self.load_water_values()
        shade_values = self.load_shade_values()
        height_values, mass_values = self.load_plants_height_and_masses_values()

        # save initial conditions 
        self._results_water[0] = water_heights
        self._results_shade[0] = shade_values
        self._results_heights[0] = height_values
        self._results_masses[0] = mass_values

        # current watermap
        cur_water_map = self.get_environment().get_watermap()

        # current shademap
        cur_shade_map = self.get_environment().get_shademap()

        # update parameters k_elong and k_prod in plants via environment
        self.get_environment().set_k_prod_and_k_elong_for_all_plants(k_prod=k_prod, k_elong=k_elong)

        # run the simulation with all timestpes
        for i in range(self._timesteps):
            # FIXME: DELETE testprint
            # print(f'Simulation.run(): shademap data: {cur_shade_map.get_items()}')
            # print(f'Simulation.run(): watermap data: {cur_water_map.get_items()}')
            # print(f'Simulation.run(): GROW_ALL_PLANTS(), k_prod: {k_prod} ')
            
            # print(f'Simulation.run(): GROW_ALL_PLANTS(), timestep: {i} after initial conditions')

            # grow all plant in the environment
            # NOTE: Here we could pass water or shademap
            # TODO: pass senseful map objects
            ###########################################################################################
            # UNCOMMENT IF WATER TABLE SHALL BE AT -3cm FOR ALL TIMESTEPS
            self.get_environment().grow_all_plants(watermap=cur_water_map, shademap=cur_shade_map, print_log=print_log)
            ###########################################################################################

            ###########################################################################################
            # TEST: ACCORDING TO FIGURE SIX: KEEP WATER TABLE 3cm BELOW AVERAGE SURFACE
            
            # self.get_environment().grow_all_plants(watermap=cur_water_map, shademap=cur_shade_map)

            ############# UPDATE Watermap to the average carpet height #######################################
            
            if adapt_water_table_height_to_average_carpet_height:
                cur_water_map_fig_6 = cur_water_map
                current_height, current_mass_values = self.load_plants_height_and_masses_values()
                cur_average_carpet_height = np.average(current_height)
                items_below_carpet = np.zeros_like(cur_water_map_fig_6.get_items()) + cur_average_carpet_height - adapted_depth_below_average_carpet_height
                # set the height of the water table 3cm below the mean surface level (like probably described in Table 5, C(5))
                # cur_water_map_fig_6.set_up(constant_value=cur_average_carpet_height - adapted_depth_below_average_carpet_height)
                cur_water_map.set_items(items_below_carpet)

            ############ END Watermap changes according to FIGURE 6 ####################################

            # load all data created by the model runs
            water_heights = self.load_water_values()
            shade_values = self.load_shade_values()
            height_values, mass_values = self.load_plants_height_and_masses_values()

            # save the data in the results
            # save initial conditions 
            self._results_water[i+1] = water_heights
            self._results_shade[i+1] = shade_values
            self._results_heights[i+1] = height_values
            self._results_masses[i+1] = mass_values

            # UPDATE ENVIRONMENTAL CONDITIONS
            # if we do use dynamical values for the shade
            if use_dyn_water_table_height:
                cur_water_map = watermap_series[i+1]

            # UPDATE ENVIRONMENTAL CONDITIONS
            # if we do use dynamical values for the shade
            if use_dyn_external_shade:
                cur_shade_map = shademap_series[i+1]
        
        # timestamp
        end_time_stamp = time.time()

        # runtime
        duration = end_time_stamp - start_time_stamp

        # Print Information 
        print(f'Simulation.run(): Finished Run. Some details:\nSimulated timesteps: {self._timesteps}\n Duration: {duration} s\nshape environment (spots in row, rows): {(self.get_environment().get_number_of_plants_in_one_row(), self.get_environment().get_number_of_rows())} \nShape results_height (timesteps, number_of_rows, spots_in_row): {self._results_heights.shape}')

        # Return results: heights, masses, shade, water
        return self._results_heights, self._results_masses, self._results_shade, self._results_water

    def run_LAOLA(self, constant_watermap:Watermap=None, constant_shademap:Shademap=None, watermap_series=None, shademap_series=None, print_log = False):
        '''
        ## RETURN 
        # RUNS Environment.grow_all_plants_LAOLA() instead of Environment.grow_all_plants() 
        Returns four 3D numpy arrays with results for all timesteps for each height, mass, external shade and water-table depth
        Runs a simulation for the number of timesteps given in self._timesteps.
        It measures the runtime, 
        creates multiple 3D np.arrays to save all the twodimensional results of water, shade and growth (height and mass) according to the shape of environment (which is again defined by the Simulation object),
        runs environment.grow_all_plants(optional_watermap, optional_shademap) and saves the results here for each timestep.
        Prints a short summary of the results.

        ## PARAMETER
        constant_watermap: *Watermap*  
        If None, a constant watermap with water table of height 0.0 will be used for all timesteps.  
        If a watermap with constant values shall be used for all timesteps, this map will be used.  
        If, additionally, a watermap _series_ (`watermap_series`) is given, then `constant_watermap` can function as the initial condition.  
        To achieve this case the `len(watermap_series)` should be equal to `Environment.get_timesteps()` and not `Environment.get_timesteps() + 1`).

        constant_shademap: *Shademap*  
        If None, a constant shademap with external shade of 0.0 will be used for all timesteps.  
        If a shademap, representing the external shade at each spot, with constant values shall be used for all timesteps, this map will be used.  
        If, additionally, a shademap _series_ (`shademap_series`) is given, then `constant_shademap` can function as the initial condition.   
        To achieve this case the `len(shademap_series)` should be equal to `Environment.get_timesteps()` and not `Environment.get_timesteps() + 1`).

        watermap_series: *Series of watermaps*
        Length of `Environment.get_timesteps()` or `Environment.get_timesteps() + 1` needed.   
        In the first case, if constant_watermap is given, the constant_watermap will be used as the initial condition.
        If passed, the entries of this series will be used for each timestep as the watermap (representing the water-table height above an arbitrary zero).  

        shademap_series: *Series of shademaps*
        Length of `Environment.get_timesteps()` or `Environment.get_timesteps() + 1` needed.   
        In the first case, if constant_shademap is given, the constant_shademap will be used as the initial condition.
        If passed, the entries of this series will be used for each timestep as the shademap (representing the external shade caused by vascular plants).  


        '''
        # save starting point
        start_time_stamp = time.time()

        # A boolean that will save, whether we want to use dynamical values for water-table depth
        use_dyn_water_table_height = False

        # A boolean that will save, whether we want to use dynamical values for external shade
        use_dyn_external_shade = False

        # make the threedimensional np.array with the same shape as environment and the maps
        self._results_heights = np.zeros((self._timesteps+1, self.get_environment().get_number_of_rows(), self.get_environment().get_number_of_plants_in_one_row()))
        self._results_masses = np.zeros((self._timesteps+1, self.get_environment().get_number_of_rows(), self.get_environment().get_number_of_plants_in_one_row()))
        self._results_water = np.zeros((self._timesteps+1, self.get_environment().get_number_of_rows(), self.get_environment().get_number_of_plants_in_one_row()))
        self._results_shade = np.zeros((self._timesteps+1, self.get_environment().get_number_of_rows(), self.get_environment().get_number_of_plants_in_one_row()))

        # Check for initiation of environment
        self.check_for_environment()

        ## WATERMAP: DYNAMICAL OR NOT ###########################################

        # If we just want constant water tables 
        if not constant_watermap==None:
            # print
            print(f'Simulation.run(): We use constant watermap of values: {constant_watermap.get_items()}')

            # update map object in environment
            self.get_environment().set_watermap(constant_watermap)

            # FIXME: Delete this line
            print(f'Simulation.run(): The environment updated constant watermap to: {self.get_environment().get_watermap().get_items()}')

        # if we want to use a time series of water table-heights
        if not watermap_series == None:

            # check for length
            if not (len(watermap_series) == (self.get_timesteps() + 1) or len(watermap_series) == (self.get_timesteps())): # + 1 due to the initial condition
                
                # print Warning
                print(f'Simulation.run(): Passed watermap_series for dynamical values has len: {len(watermap_series)}. \n But len({self.get_timesteps()} or len({self.get_timesteps()}) (if you are also passing a constant_map object as the initial condition) is needed)')
            
                # update the use of dynamical water tables: It is not used
                use_dyn_water_table_height = False
            # if length is equal to timesteps, so the initial cndition is missing, we will treat constant_watermap, if existing, as the initial condition
            elif len(watermap_series) == (self.get_timesteps()) and (not constant_watermap == None):

                print(f'Simulation.run(): Set constant watermap as the initial condition, as len(water_map_series) = timesteps ({len(watermap_series)} = {self.get_timesteps()}))')

                # make the constant map the initial condition
                # update map object in environment
                self.get_environment().set_watermap(constant_watermap)

                # extend series by initial condition
                watermap_series = [constant_watermap] + watermap_series

                # update the use of timeseries
                use_dyn_water_table_height = True

            # if we do got exactly the timetspes+1 length
            elif len(watermap_series) == (self.get_timesteps() + 1):
                  
                  print(f'Simulation.run(): Dynamical Watermap is used. First entry of the series will be the inital condition. ({len(watermap_series)} = {self.get_timesteps()}))')

                  # get first entry as the initial condition
                  initial_water_heights = watermap_series[0]

                  # set watermap in environment
                  self.get_environment().set_watermap(initial_water_heights)

                  # update the use of timeseries
                  use_dyn_water_table_height = True

        else:
            # print()
            print(f'No dynamical watermap series is used')

        ## SHADEMAP: DYNAMICAL OR NOT ###########################################

        # If we just want constant water tables 
        if not constant_shademap==None:

            # update map object in environment
            self.get_environment().set_shademap(constant_shademap)

        # if we want to use a time series of water table-heights
        if not shademap_series == None:

            # check for length
            if not (len(shademap_series) == (self.get_timesteps() + 1) or len(shademap_series) == (self.get_timesteps())): # + 1 due to the initial condition
                
                # print Warning
                print(f'Simulation.run(): Passed shademap_series for dynamical values has len: {len(shademap_series)}')

                # update use of dynamical values: NOT USED
                use_dyn_external_shade = False
            
            # if length is equal to timesteps, so the initial condition is missing, we will treat constant_shademap, if existing, as the initial condition
            elif len(shademap_series) == (self.get_timesteps()) and (not constant_shademap == None):

                print(f'Simulation.run(): Set constant shademap as the initial condition, as len(shade_map_series) = timesteps ({len(shademap_series)} = {self.get_timesteps()}))')

                # make the constant map the initial condition
                # update map object in environment
                self.get_environment().set_shademap(constant_shademap)

                # extend series by initial condition
                shademap_series = [constant_shademap] + shademap_series

                # update use of dynamical values: USED
                use_dyn_external_shade = True

            # if we do got exactly the timetspes+1 length
            elif len(shademap_series) == (self.get_timesteps() + 1):
                  
                print(f'Simulation.run(): Dynamical Shademap is used. First entry of the series will be the inital condition. ({len(shademap_series)} = {self.get_timesteps()}))')

                # get first entry as the initial condition
                initial_external_shades = shademap_series[0]

                # set watermap in environment
                self.get_environment().set_shademap(initial_external_shades)

                # update use of dynamical values: USED
                use_dyn_external_shade = True

        #### END OF CHECK FOR CONSTANT OR DYNAMICAL VALUES FOR WATER AND EXTERNAL SHADE #####################

        # save initial conditions (watermap and shademap in environment are now
        # 1. just 0.0, if no constant_map, or time series or both have been passed
        # 2. just a constant, defined by constant_Xmap, if no Xseries have been passed or one of length timesteps instead of timesteps + 1
        # 3. the first entry of the timeseries of Xseries if length was equal to timesteps + 1
        water_heights = self.load_water_values()
        shade_values = self.load_shade_values()
        height_values, mass_values = self.load_plants_height_and_masses_values()

        # FIXME: Delete this line
        print(f'Simulation.run(): self._results_water.shape: {self._results_water.shape}')

        # save initial conditions 
        self._results_water[0] = water_heights
        self._results_shade[0] = shade_values
        self._results_heights[0] = height_values
        self._results_masses[0] = mass_values

        # current watermap
        cur_water_map = self.get_environment().get_watermap()

        # current shademap
        cur_shade_map = self.get_environment().get_shademap()

        # run the simulation with all timestpes
        for i in range(self._timesteps):
            # FIXME: DELETE testprint
            print(f'Simulation.run(): watermap data: {cur_water_map.get_items()}')
            
            print(f'Simulation.run(): GROW_ALL_PLANTS(), timestep: {i} after initial conditions')

            # grow all plant in the environment
            # NOTE: Here we could pass water or shademap
            # TODO: pass senseful map objects
            ###########################################################################################
            # UNCOMMENT IF WATER TABLE SHALL BE AT -3cm FOR ALL TIMESTEPS
            self.get_environment().grow_all_plants_LAOLA(watermap=cur_water_map, shademap=cur_shade_map, print_log=print_log)
            ###########################################################################################

            ###########################################################################################
            # TEST: ACCORDING TO FIGURE SIX: KEEP WATER TABLE 3cm BELOW AVERAGE SURFACE
            
            # self.get_environment().grow_all_plants(watermap=cur_water_map, shademap=cur_shade_map)

            ############# UPDATE Watermap according to figure 6 #######################################
            cur_water_map_fig_6 = Watermap(number_of_rows=self.get_environment().get_number_of_rows(), number_of_spots_per_row=self.get_environment().get_number_of_plants_in_one_row(), items=None)
            current_height, current_mass_values = self.load_plants_height_and_masses_values()
            cur_average_carpet_height = np.average(current_height)
            cur_water_map_fig_6.set_up()
            # set water table depth 3cm below all plants
            cur_water_map_fig_6.set_items(current_height - 3.0)
            cur_water_map = cur_water_map_fig_6
            ## update the water table, such that we are 3cm below current carpet height
            self.get_environment().set_watermap(cur_water_map_fig_6)
            ############ END Watermap changes according to FIGURE 6 ####################################

            # load all data created by the model runs
            water_heights = self.load_water_values()
            shade_values = self.load_shade_values()
            height_values, mass_values = self.load_plants_height_and_masses_values()

            # save the data in the results
            # save initial conditions 
            self._results_water[i+1] = water_heights
            self._results_shade[i+1] = shade_values
            self._results_heights[i+1] = height_values
            self._results_masses[i+1] = mass_values

            # UPDATE ENVIRONMENTAL CONDITIONS
            # if we do use dynamical values for the shade
            if use_dyn_water_table_height:
                cur_water_map = watermap_series[i+1]

            # UPDATE ENVIRONMENTAL CONDITIONS
            # if we do use dynamical values for the shade
            if use_dyn_external_shade:
                cur_shade_map = shademap_series[i+1]
        
        # timestamp
        end_time_stamp = time.time()

        # runtime
        duration = end_time_stamp - start_time_stamp

        # Print Information 
        print(f'Simulation.run(): Finished Run. Some details:\nSimulated timesteps: {self._timesteps}\n Duration: {duration} s\nshape environment (spots in row, rows): {(self.get_environment().get_number_of_plants_in_one_row(), self.get_environment().get_number_of_rows())} \nShape results_height (timesteps, number_of_rows, spots_in_row): {self._results_heights.shape}')

        # Return results: heights, masses, shade, water
        return self._results_heights, self._results_masses, self._results_shade, self._results_water
