import numpy as np
import warnings 
from Growth_Processes_Model import Growth_Processes_Model
from typing import Optional
# Environment is imported when needed to avoid circular import

class Plant:
    def __init__(self, species:str, init_height = 0.0, init_mass = 0.0, init_local_water_table_depth = 0.0, init_local_shade_value = 0.0, k_prod = -1.39, k_elong = -1.39, location = (0.0, 0.0), neighbors = []):
        '''
        Instructor for Plant object
        - species (String)                        : defines the species ('capillifolium' or 'papillosum')
        - init_height (float)                  : absolute height of the capitulum in cm above defined zero at t = 0, Default 0.0
        - init_mass   (float)                  : absolute mass of the plant in TODO: define mass unit      at t = 0, Default 0.0
        - init_local_water_table_depth (float) : abolute water_table_height in cm above defined zero       at t = 0, Default 0.0
        - init_local_shade_value (float)       : external_shade_value as an absorbance                     at t = 0, Defaul, 0.0
        - k_prod (float, usually < 0)          : parameter for the exposure effect in mass_growth                  , Default -1.39 as this value was given in the paper
        - k_elong (float, usually < 0)         : parameter for the exposure effect in length_growth                , Default -1.39 as this value was given in the paper
        - location (tuple, twodimensional)     : position in environment                                           , Default (0.0, 0.0)
        - neighbors (list of plants)           : list of the neighbors to calculate average neighbor height        , Default [] (empty list)
        '''
        self._species = species
        self._height = init_height
        self._mass = init_mass
        self._local_water_table_depth = init_local_water_table_depth
        self._local_shade_value = init_local_shade_value
        self._k_prod = k_prod
        self._k_elong = k_elong
        self._location = location
        self._growth_processes_model = None
        self._environment = None
        self._imported_environment = False
        self._mass_growth_value = 0.0
        self._elong_growth_value = 0.0
        
        # Neighbor Type Check ######
        # Check for List
        if not(isinstance(neighbors, list)):
            raise TypeError(f'Plant.__init__(): Wrong Data Type for neighbors, a list has to be passed, but a {type(neighbors)} was given')
        
        # check for one-dimesnionality in an empty list
        # elif(isinstance(neighbors, list) and not(neighbors) and (len(neighbors[0])!= 1)):
            # raise TypeError(f'Wrong dimensions for the neighbor list object. We need a list with only one dimension. {len(neighbors[0])} were given.')
        
        # check for empty list, which is allowed here
        elif(isinstance(neighbors, list) and (len(neighbors)== 0)):
            
            # Test Print
            print('Plant.__init__(): Neighbors set in plant object')

            self._neighbors = neighbors
            print('Plant.__init__(): For the neighbors argument an empty list has been passed to a plant object during initialization. This is no problem and a well defined case.', UserWarning)
        
        else:
            # Check for only Plant objects or None objects
            for i, plant in enumerate(neighbors):
                
                # check for object type plant
                if not(isinstance(plant, Plant)):
                    print(f'Neighbors: \n {neighbors}')
                    raise TypeError(f'Plant.__init__(): Wrong data type of one element. The passed list of neighbors contains one NO-PLANT object at index {i}.')
            
            # Test Print
            print('Plant.__init__(): Neighbors set in plant object (eventually not defined yet!)')
            # finally set neighbors
            self._neighbors = neighbors 
        
        
    # GETTER ###############################################
    def get_species(self):
        '''
        Returns the species name
        '''
        return self._species
    
    def get_height(self):
        return self._height

    def get_mass_growth_value(self):
        '''
        Returns the current value of the saved mass growth value (calculated in get_growth_values() by the Growth_Processes_Model).
        This is done because, we want to calculate all the plants growth BEFORE we let them grow. Otherwise certain plants would consider some alreeady grown plants and some not grown yet in their neighborhood.

        TODO: 
        - Make multidimenional and adaptive to plant type?
        '''
        return self._mass_growth_value
    
    def get_elong_growth_value(self):
        '''
        Returns the current value of the saved height growth value (calculated in get_growth_values() by the Growth_Processes_Model).
        This is done because, we want to calculate all the plants growth BEFORE we let them grow. Otherwise certain plants would consider some alreeady grown plants and some not grown yet in their neighborhood.

        TODO: 
        - Make multidimenional and adaptive to plant type?
        '''
        return self._elong_growth_value
    
    def get_mass(self):
        return self._mass 
    
    def get_abs_local_water_table_height(self):
        return self._local_water_table_depth
    
    def get_local_shade_value(self):
        return self._local_shade_value
    
    def get_k_prod(self):
        return self._k_prod
    
    def get_k_elong(self):
        return self._k_elong
    
    def get_location(self):
        '''
        Returns the two-dimensional tuple of the location within the environments maps.
        '''
        # return location tuple
        return self._location
    
    def get_neighbors(self):
        return self._neighbors
    
    def get_environment(self):
        return self._environment
    
    def get_imported_environment(self):
        '''
        Returns True if Environment was imported by add_Environment()
        Returns False if not.
        '''
        return self._imported_environment
    
    def get_growth_processes_model(self) -> Optional[Growth_Processes_Model]:
        # Check if object exists and is of type Growth_Processes_Model
        if self._growth_processes_model != None and isinstance(self._growth_processes_model, Growth_Processes_Model):
            # return growth_processes_model
            return self._growth_processes_model
        
        # if growth_processes_model attribute (derived from environment object) is None or not the correct type
        else:
            # raise TypeError
            warnings.warn(f'\n Plant.get_growth_processes_model(): \n The attribute for the Growth_procceses_model is None or not of the class Growth_Processes_Model. \n Current attribute is of type {type(self._growth_processes_model)}.', UserWarning)
            return None
    
    
    # SETTER ###############################################
    def set_species(self, species: str):
        '''
        sets the species
        '''
        # check for valid species
        if species in ['capillifolium', 'papillosum']:

            # set species
            self._species = species
        else:
            print(f'Plant.set_species(): No species of name {species} is known. No update made.\n')

    def set_height(self, height):
        # Check data type
        if not(isinstance(height, float)):
            raise TypeError(f'Wrong Type for height value, a {type(height)} was given, but we need a float.')
        else:
            self._height = height

    def set_mass(self, mass):
        # Check data type
        if not(isinstance(mass, float)):
            raise TypeError(f'Wrong Type for mass value, a {type(mass)} was given, but we need a float.')
        else:
            self._mass = mass
    
    def set_elong_growth_value(self, elong_growth_value: float):
        '''
        Sets the current value of the saved elong growth value (calculated in get_growth_values() by the Growth_Processes_Model).
        This is saved because, we want to calculate all the plants growth BEFORE we let them grow. Otherwise certain plants would consider some already grown plants and some not grown yet in their neighborhood.

        TODO: 
        - Make multidimenional and adaptive to plant type?
        '''
        # update value
        self._elong_growth_value = elong_growth_value

    def set_mass_growth_value(self, mass_growth_value: float):
        '''
        Sets the current value of the saved mass growth value (self._mass_growth_value; calculated in get_growth_values() by the Growth_Processes_Model).
        This is saved because we want to calculate all the plants growth BEFORE we let them grow. Otherwise certain plants would consider some already grown plants and some not grown yet in their neighborhood.

        TODO: 
        - Make multidimenional and adaptive to plant type?
        '''
        # update value
        self._mass_growth_value = mass_growth_value 

    def set_abs_local_water_table_depth(self, local_water_table_depth):
        # Check data type
        if not(isinstance(local_water_table_depth, float)):
            raise TypeError(f'Wrong Type for water table deph value, a {type(local_water_table_depth)} was given, but we need a float.')
        else:
            self._local_water_table_depth = local_water_table_depth

    def set_local_shade(self, local_shade_value):
        # Check data type
        if not(isinstance(local_shade_value, float)):
            raise TypeError(f'Wrong Type for shade value, a {type(local_shade_value)} was given, but we need a float.')
        else:
            self._local_shade_value = local_shade_value

    def set_k_prod(self, k_prod):
        self._k_prod = k_prod
    
    def set_k_elong(self, k_elong):
        self._k_elong = k_elong

    def set_location(self, location):
        # Check data type
        if not(isinstance(location, tuple)):
            raise TypeError(f'Wrong Type for location value, a {type(location)} was given, but we need a tuple.')
        else:
            # Check dimensions (we need a )
            if not(len(location) == 2):
                raise TypeError(f'Wrong Dimensions for location tuple, {len(location)} was given, but we need a Two-dimensional Tuple.')
            else:
                # set location to new location value
                self._location = location

    def set_imported_environment(self):
        # if Environment is not already imported: Set to is imported
        if not self._imported_environment: self._imported_environment = True
        # status printing
        print(f'SUCESS, Plant.set_imported_environment(): \n imported_environment set to {self._imported_environment}\n ')
   
    def set_neighbors(self, neighbors):
        '''
        Shall set a List of neighbors (Plant objects). They are used to determine exposure and shading for growth. 
        Checks for...
        - a list of neighbors
        - type of objects in neighbors. All have to be plant objects

        TODO:
        - Handle Gap of Plants (I need a no Plant space holder)
        '''
        # Check for List
        if not(isinstance(neighbors, list)):
            raise TypeError(f'Wrong Data Type for neighbors, a list has to be passed, but a {type(neighbors)} was given')
        else:
            # Check for only Plant objects
            for i, plant in enumerate(neighbors):
                if not(isinstance(plant, Plant)):
                    all_neighbors_are_plants = False
                    raise TypeError(f'Wrong data type of at least one element. The passed list of neighbors contains one NO-PLANT object at index {i}.')
            
            # finally set neighbors
            self._neighbors = neighbors
    
    def set_environment(self, environment):

        # Check if there exists an environment
        if (self._environment == None):
            raise SyntaxError(f'Plant: there is no Environment object yet. Please use Plant.add_envrionment() to define a environment object for the plant Object.')
        
        # Environment exists
        else:
            # check if import of Environment was done
            # NOTE: Environment should only NOT be imported, if add_Environment was not called before -> call add_environment
            if not(self.get_imported_environment()):
                # import ENvironment class
                from Environment import Environment

                # Check for Data Type
                if not(isinstance(environment, Environment)):
                    raise TypeError(f'Wrong Data type for environment. A {type(environment)} object was given, but need a Environment object')
        
            # Set environment object
            self._environment = environment
            # update growth processes model
            self._growth_processes_model = environment.get_growth_proccesses_model()

    ### METHODS ###############################################
    def get_distance_to_water_table(self):
        '''
        DESCRIPTION
        Returns the local water-table depth, so the distance of the capitulum to the water table.
        Here we obtain the water table height by accessing the environment object (where we have to check wheter the plant already imported an environment object)
        and then accessing the watermap object at the plants location.
        We then substract capitulum height - Water_table_height.
        As the capitulum should usually be higher than the water table this shall give us a POSITIVE value.
        '''
        
        # Returns True if Environment was imported by add_Environment()
        # Returns False if not.
        # If we have a environment object ...
        if self._imported_environment:
            # get the absolute height of the water table
            absolute_water_table_height = self.get_abs_local_water_table_height()
            
            # get absolute height of the capitulum
            absolute_height_capitulum = self.get_height()

            # return distance
            abs_distance_to_water_table_depth = absolute_height_capitulum - absolute_water_table_height
            return abs_distance_to_water_table_depth
        
        # if we DO NOT have an environment object yet
        else:
            # give quick overview of what happens
            print(f"Plant.get_distance_to_water_table(): No environment object so far. We return the last saved value of self.local_water_table_height")
            return self.get_abs_local_water_table_height()

    def get_neighbors_impact(self):
        '''
        DESCRIPTION:
        Currently, this function is returning the mean height of the (six) neighbors of a plant.
        NOTE: For testing purposes, we let the function return 1.0 if neighborhood is not defined (like for our testplant)

        RETURN VALUES:
        mean_height_of_surroundings - (float): the mean height of the surrounding plants calculated by the own list of neighbors

        QUESTIONS:
        In Future: Can we find 1. a different neighborhood and 2. a different way of considering the neighbors plant height?
        
        TODO:
        Rethink calculation procedure and neighborhood selection.
        '''
        # Here, in the future modifications on the calculation of the environment shall take place
        # Current calculation: mean height of six surrounding plants

        # help variable
        sum_height_of_surroundings = 0

        for i, plant in enumerate(self.get_neighbors()):
            # Check for Plant object 
            if not(isinstance(plant, Plant)):
                # TODO: Uncomment this!
                raise TypeError(f'Plant: Error in Type (no Plant) while attempt to calculate mean height of surroundings ( get_neighbors_impact() )')
    
            else:
                # sum all plants heights
                sum_height_of_surroundings += plant.get_height()
        
        # Divide by number of neighbors in the neighbor list
        if not(len(self.get_neighbors()) == 0):
            mean_height_of_surroundings = sum_height_of_surroundings / len(self.get_neighbors())

        # Return
        return mean_height_of_surroundings

    def add_Environment(self, environment):
        '''
        TODO: Documentation

        DESCRIPTION:

        ASSUMPTIONS:

        NOTES:

        '''
        # Import
        from Environment import Environment

        # set _imported_environment to True
        self.set_imported_environment()

        # Check for Data Type
        if not(isinstance(environment, Environment)):
            raise TypeError(f'Wrong Data type for environment in add_Environment() in Plant. A {type(environment)} object was given, but need a Environment object')
        
        # Check if there is already an environment given
        elif(self.get_environment() != None):
            raise Warning(f'add_Environment: An environment attribute is already defined. No environment added.')
        
        else:
            self._environment = environment
            # Get the according growth_processes_model object
            self._growth_processes_model = environment.get_growth_proccesses_model()

    def update_environmental_conditions(self):
            # Check if environment is not None
            if(self.get_environment() == None or self.get_imported_environment() == False):
                warnings.warn(f'Plant.update_environmental_conditions(): Environment object is None or not added. Run add_Environement() first.', UserWarning)

            # if Environment attribute exists
            else:
                # ask environment for new environmental conditions at own location
                shade_as_absorbance_value = self.get_environment().get_shade_at(self.get_location())
                abs_water_table_depth_in_cm = self.get_environment().get_water_table_depth_at(self.get_location())
                
                # update shade value
                self.set_local_shade(shade_as_absorbance_value)

                # update water_table_depth
                self.set_abs_local_water_table_depth(abs_water_table_depth_in_cm)

                # NOTE: Update neighbors (check if neighbors have changed) could be a good idea if we for example have moss dying or, further in progress, if we have processes like expansion due to growth

    def get_growth_values(self, print_params=False):
        '''
        DESCRIPTION
        Function that simulates one growth step (here it is a day of growth).
        Uses the Growth_Processes_Model.py to calculate mass and height growth.

        NOTE: 
        - We only calculate the values but do NOT update the plants state variables (Height and mass)
        
        PARAMETERS
        - print_params (bool), Optional: If True, a Output of the Parameters is given in the console. Default is False.

        Further checks for correct type of Growth-Model.
        '''

        # Update current environmental conditions
        self.update_environmental_conditions()

        # local growth model
        loc_growth_processes = self.get_growth_processes_model()
        
        # Check for correct object type of growth_processes_model
        if (isinstance(loc_growth_processes, Growth_Processes_Model)):
            assert isinstance(loc_growth_processes, Growth_Processes_Model)

            if print_params:
                print(f'\nNEW PLANT GROW STEP of species {self.get_species()}')
                neighbors = self.get_neighbors()
                neighbor_heights = []
                for i, plant in enumerate(neighbors):
                    neighbor_heights.append(plant.get_height())
                
                print(f'Water-Table-depth: {self.get_abs_local_water_table_height()}')
                print(f'NO PARAM, but used in grow_step() as the distance to the water_table: {self.get_distance_to_water_table()}')
                print(f'Shade: {self.get_local_shade_value()}')
                print(f'k_elong: {self.get_k_elong()}')
                print(f'k_prod: {self.get_k_prod()}')
                print(f'length_plant: {self.get_height()}')
                print(f'Neighbors heights: {neighbor_heights}')
                print(f'Average_neighbor_length: Implemented in get_impact_neighbors. The result: \n get_neighbors_impact(): {self.get_neighbors_impact()}')
                print(f'END PLANT GROWTH\n')

            # access growth_model grow function
            # Here, the Growth_Process_Model is already managing the growth.
            # So this function leaves the plant already grown
            # NOTE: Should be correct code, but due to static checking, VSCode can not resolve
            # FIXME: Avoid magic number -1.39 for k_prod and k_elong                               species, WTD, S, k_prod, k_elong, length_plant, average_neighbor_length
            elongation_value, net_productivity_value = loc_growth_processes.grow_one_timestep(self.get_species(),self.get_distance_to_water_table(), self.get_local_shade_value(), self.get_k_prod(), self.get_k_elong(), self.get_height(), self.get_neighbors_impact(), print_log=print_params)

            # save values in private class attribute
            self.set_elong_growth_value(elongation_value) 
            self.set_mass_growth_value(net_productivity_value) 

    def grow_step(self, print_params=False):
            '''
            DESCRIPTION
            NOTE: Execute self.get_growth_values() before this function.
            Here we finally update the plants state variables (height and mass) by the values of growth calculated in self.get_growth_values().
            We add theses values to the current height and mass values of the plant.
            Finally we set the class attributes mass_growth_value and elong_growth_value to 0.0, to ensure that we have proper grwoth in the next step only, 
            if we first execute self.get_growth_values() beforehand.

            PARAMS
            - print_params (bool, optional): Gives an output of the current paramters and auxilary variables in this Plant object.
            '''

            # Print parameter if desired
            if print_params:
                print(f'\nNEW PLANT GROW STEP of SPECIES {self.get_species()}')
                neighbors = self.get_neighbors()
                neighbor_heights = []
                for i, plant in enumerate(neighbors):
                    neighbor_heights.append(plant.get_height())
                
                print(f'Water-Table-depth: {self.get_abs_local_water_table_height()}')
                print(f'NO PARAM, but used in grow_step() as the distance to the water_table: {self.get_distance_to_water_table()}')
                print(f'Shade: {self.get_local_shade_value()}')
                print(f'k_elong: {self.get_k_elong()}')
                print(f'k_prod: {self.get_k_prod()}')
                print(f'length_plant: {self.get_height()}')
                print(f'Neighbors heights: {neighbor_heights}')
                print(f'Average_neighbor_length: Implemented in get_impact_neighbors. The result: \n get_neighbors_impact(): {self.get_neighbors_impact()}')
                print(f'END PLANT GROWTH\n')
                    
            # Add growth to current state of plant
            # NOTE: We add these values to the current plants state variables
            self.set_height(self.get_height() + self.get_elong_growth_value()) 
            self.set_mass(self.get_mass() + self.get_mass_growth_value()) 

            # FOR SECURITY: Set the growth_rate_values to 0.0, so we have to execute get_growth_values before we are able to have reasonable get growth rates again
            self.set_mass_growth_value(0.0)
            self.set_elong_growth_value(0.0)

    def report_stats(self):
        '''
        Creates a dictionary that contains current Height, Biomass and Location.

        Returns this dict = {'Height': self.get_height(), 
                            'Biomass': self.get_mass(),
                            'Location': self.get_location(),
                            'Species': self.get_species()}
        '''
        # create dict with all the relevant data of the plant
        stats = {'Height': self.get_height(), 
                'Biomass': self.get_mass(),
                'Location': self.get_location(),
                'Species': self.get_species()}
        # return data
        return stats
    
    def report_params(self):
        '''
        Creates a dictionary that contains current 
        - k_prod: (MASS related) rate used in exposure effect (if plant grows above Sphagnum carpet (i.e. its defined neighborhood)) for decrease in growth in MASS
        - k_elong: (HEIGHT related) rate used in exposure effect (if plant grows above Sphagnum carpet (i.e. its defined neighborhood)) for decrease in growth in LENGTH
        - Water-Table depth: current Water-table-depth
        - Shade: current shade value
        - Location: Tuple of location in Plantmap
    

        params = {'k_prod': self.get_k_prod(),
                  'k_elong': self.get_k_elong(),
                  'Water-Table Depth': self.get_local_water_table_depth(), 
                  'Shade': self.get_local_shade_value(),
                  'Location': self.get_location(),
                  'Species': self.get_species()}
        '''
        # create dict with all the relevant data of the plant
        params = {'k_prod': self.get_k_prod(),
                  'k_elong': self.get_k_elong(),
                  'Water-Table Depth': self.get_local_water_table_depth(), 
                  'Shade': self.get_local_shade_value(),
                  'Location': self.get_location(),
                  'Species': self.get_species()}

        # return data
        return params