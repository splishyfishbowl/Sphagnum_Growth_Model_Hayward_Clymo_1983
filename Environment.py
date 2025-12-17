from Growth_Processes_Model import Growth_Processes_Model
from Map import Plantmap, Watermap, Shademap
from Plant import Plant
import warnings

class Environment:
    def __init__(self, species:str, number_of_rows: int, spots_per_row: int, init_mode_height='', mean_height = 0.0, std = 1.0):
        '''
        INCOMPLETE
        PARAMS
        - species, String: Will determine the species at the set up of Plantmap. Either 'capillifolium' or 'papillosum'
        - number_of_rows, Integer: number of spots for plant, shade, water per row, to be thought as the inner of the two-dimensional map arrays, I imagine them horizontically
        - height_map, Integer: number of rows for rows of plant, shade, water per row, to be thought as the outer of the two-dimensional map arrays arrays, I imagine them vertically
        - init_mode_height, String, (See Plantmap.set_up()): 
                                    If 'NORM_DIST' is passed, 
                                    plants heights are initiated by drawing from an 
                                    normal distribution 
                                    with mean = mean_height and
                                    standard_deviation = std

                                    If 'UNIFORM' is passed,
                                    plants heights are initiated by drawing from a
                                    uniform distribution
                                    of value mean_height

        - mean_height, float, (See Plantmap.set_up()):       
                                    number describing the mean of the distribution
        - std, float, (See Plantmap.set_up()):               
                                    standard deviation describing the normal distribution, if applicable
        '''
        # Dimensions of the Plantmap, Watermap and Shademap defined as 
        # (number_of_rows) x 
        # (_spots_per_row) x such rows
        self._number_of_rows = number_of_rows
        self._spots_per_row = spots_per_row
        
        # create Watermap
        self._watermap = Watermap(number_of_rows=number_of_rows, number_of_spots_per_row=spots_per_row, items=None)
        # Set up watermap -> all values are 0.0
        self._watermap.set_up()

        # create Watermap
        self._shademap = Shademap(number_of_rows=number_of_rows, number_of_spots_per_row=spots_per_row, items=None)
        # Set up watermap -> all values are 0.0
        self._shademap.set_up()

        # create Plantmap
        self._plantmap = Plantmap(species=species, number_of_rows=number_of_rows, number_of_spots_per_row=spots_per_row, items=None)
        # Set up and initiate plants as items
        self._plantmap.set_up(init_mode_height=init_mode_height, mean_height=mean_height, std=std)

        # initiate Growth_Processes_Model (contains all the Growth mechanisms)
        self._growth_processes = Growth_Processes_Model()

        # TODO: return initial conditions
        # return initial_heights_and_masses()

    # GETTER
    def get_number_of_plants_in_one_row(self):
        '''
        Returns the number of spots in one row in a plant-, shade- or watermap.
        Is more or less equal to the "width" of the map and to the length of a inner array in the arrays 
        items[[...],
               ...,
              [...]]
        '''
        return self._spots_per_row
    
    def get_number_of_rows(self):
        '''
        Returns the number of rows with width x spots in a row in plant-, shade- or watermap.
        '''
        return self._number_of_rows
    
    def get_plantmap(self):
        '''
        Returns the plantmap attribute (Plantmap object) 

        '''
        # assert type
        assert isinstance(self._plantmap, Plantmap), f"Environment.get_plantmap(): Plantmap attribute is no Plantmap object"
        return self._plantmap
    
    def get_watermap(self):
        '''
        Returns the watermap attribute
        '''
        assert isinstance(self._watermap, Watermap), f"Environment.get_watermap(): Watermap attribute is no Watermap object"
        return self._watermap
    
    def get_shademap(self):
        '''
        Returns the shademap attribute (Iterable)
        '''
        assert isinstance(self._shademap, Shademap), "Environment.get_shademap(): Shademap attribute is no Shademap object"
        return self._shademap
    
    def get_growth_proccesses_model(self):
        '''
        Returns the Growth_processes_model or None if not correct type or Object is None 
        '''
        # if growth_processes_model attribute (derived from environment object) is None or not the correct type
        if not(self._growth_processes != None and isinstance(self._growth_processes, Growth_Processes_Model)):
            # warn and return None
            warnings.warn(f'Environment: The attribute for the Growth_procceses_model is None or not of the class Growth_Processes_Model. \n Current attribute is of type {type(self._growth_processes)}.', UserWarning)
            return None
        
        # Check if object exists and is of type Growth_Processes_Model
        else:
            # return growth_processes_model
            return self._growth_processes
        
    def get_shade_at(self, location: tuple):

        '''
        DESCRIPTION:
        Returns a specific shade value at a given location. Called by plant objects to ask for environmental conditions at a specific location.
        
        Return Value:
        - 1.0 if no twodimensional tuple was given
        - the value saved in the current Shademap.item attribute (for Shademap, a two dimensional np.array) at index according to the tuple
        
        '''
        # Check dimensionality
        if not(len(location) == 2):
            warnings.warn(f'Environment.get_shade_at(): Not a two-dimensional tuple, a tuple of dimension {len(location)} was given. Returned -1.0.', ValueError)
            return -1.0
        else:
            # Save coordinates
            first_entry = location[0]
            second_entry = location[1]

            # TODO: Check for Bounds

            # spaceholder
            shade = self.get_shademap().get_items()[first_entry][second_entry]

            # Return shade value
            return shade
    
    def get_water_table_depth_at(self, location: tuple):
        '''
        DESCRIPTION:
        Returns a specific water-table depth value at a given location. Called by plant objects to ask for environmental conditions at a specific location.
        
        Return Value:
        - 1.0 if no twodimensional tuple was given
        - the value saved in the current Watermap.item attribute (for Watermap, a two dimensional np.array) at index according to the tuple
        '''
        # [] TODO: Check for Bounds

        # Check dimensionality
        if not(len(location) == 2):
            warnings.warn(f'Environment.get_water_table_depth_at(): Not a two-dimensional tuple, a tuple of dimension {len(location)} was given. Returned -1.0.', ValueError)
            return -1.0
        else:
            # Save coordinates
            first_entry = location[0]
            second_entry = location[1]

            # TODO: Check for Bounds

            # spaceholder
            wtd = self.get_watermap().get_items()[first_entry][second_entry]

            # Return shade value
            return wtd

    def get_plant_at(self, location: tuple):
        '''
        Returns a plant at a certain location.
        We assume torodical edge conditions.

        '''
        # Check dimensionality
        if not(len(location) == 2):
            warnings.warn(f'Environment.get_plant_at(): Not a two-dimensional tuple, a tuple of dimension {len(location)} was given. Returned -1.0.', ValueError)
            return -1.0
        else:
            # Save coordinates
            first_entry = location[0]
            second_entry = location[1]

            # TODO: Check for Bounds
            # NOTE: Here we say what the edge conditions are (here torodically)
            # first entry corresponds to width
            x_respecting_bounds = first_entry % self.get_number_of_plants_in_one_row()

            # second entry corresponds to height
            y_respecting_bounds = second_entry % self.get_number_of_rows()

            # return the desired plant
            plant_at_location = self.get_plantmap().get_item_at(x_respecting_bounds, y_respecting_bounds)
            return plant_at_location

    # SETTER
    def set_plantmap(self, plantmap: Plantmap):
        '''
        Sets the attribute plantmap'''
        # TODO: Ckeck for dimensionality, type
        print(f'Environment.set_plantmap(): Success')
        self._plantmap = plantmap

    def set_watermap(self, watermap: Watermap):
        '''
        Sets the watermap attribute to a specific watermap attribute.
        The old attribute object self._watermap checks for comaptability of the passed map object.
        '''
        # Check for dimensions and type
        if(self._watermap.check_map_compatibility(watermap)):

            # set attribute
            self._watermap = watermap
        else:
            # print Warning
            print(f'Environment.set_watermap(): Watermap could not be updated')

    def set_shademap(self, shademap: Shademap):
        '''
        Sets the shademap attribute to a specific shademap attribute.
        The old attribute object self._shademap checks for comaptability of the passed map object.
        '''
        # Check for dimensions and type
        if(self._shademap.check_map_compatibility(shademap)):

            # set attribute
            self._shademap = shademap
    
    def set_water_table_depth_at(self, water_table_depth: float, location: tuple):
        # get watermap attribute and update at the given location
        self.get_watermap().set_single_item_at(water_table_depth, location)
    
    def set_shade_at(self, shade: float, location: tuple):
        # get shademap attribute and update at the given location
        self.get_shademap().set_single_item_at(shade, location)

    def set_plant_at(self, plant , location: tuple):
        '''
        DESCRIPTION
        Sets the passed plant object at a certain location and integrates it to the Plantmap items.
        Checks for Plant object type of passed object plant. Raises Type Error if not.
        Updates the plants environment attribute.
        '''
        # import Plant to be able to check for this type
        from Plant import Plant

        # Check type
        if not(isinstance(plant, Plant)):
            # raise Type Error
            raise TypeError(f'Environment.set_plant_at(): Expected Plant object for first parameter plant. But {type(plant)} was given.')
        
        # If everything is fine
        else:
            # Update Environment
            plant.add_Environment(self)

            # Update and set the Plant object
            self.get_plantmap().set_single_item_at(plant, location)

            # get the neighbors in the Plantmap and update them
            neighbors = self.get_all_neighbors_at(location[0], location[1])
            plant.set_neighbors(neighbors=neighbors)

    def set_growth_processes_model(self, growth_processes: Growth_Processes_Model):
        '''
        Sets the growth processes attribute
        '''
        # check for type
        if not(isinstance(growth_processes, Growth_Processes_Model)):
            raise TypeError(f'Environment, set_growth_processes(): Type Error, Growth_Processes_Model object is needed, but a {type(growth_processes_model)} was given.')
        else:
            self._growth_processes = growth_processes

    # Methods
    def get_all_neighbors_at(self, location: tuple):
        '''
        Returns a list of plants (the neighbors at location).
        
        Parameters:
            - location (tuple, 2-dimensional): the location we want to get the neighbors:

        '''
        # Check dimensionality
        if not(len(location) == 2):
            warnings.warn(f'Environment.get_all_neighbors_at(): Not a two-dimensional tuple, a tuple of dimension {len(location)} was given. Returned -1.0.', ValueError)
            return -1.0
        else:
            # Save coordinates
            first_entry = location[0]
            second_entry = location[1]

            # get the plant, already handles bounds
            # local_plant = self.get_plant_at(first_entry, second_entry)

            # Get dimensions of the Maps
            width = self.get_number_of_plants_in_one_row()
            height = self.get_number_of_rows()

            w = first_entry
            h = second_entry

            # create list of neighbors
            # We have six neighbors for default neighborhood (offset rows, torodical edge conditions)
            list_of_neighbors = [self.get_plant_at(((w-1) % width, h % height)), 
                                    self.get_plant_at(((w-1) % width, (h +1) % height)),
                                    self.get_plant_at(((w % width), (h - 1) % height)),
                                    self.get_plant_at(((w % width), (h + 1) % height)),
                                    self.get_plant_at(((w + 1) % width, (h % 6))),
                                    self.get_plant_at(( w % width, (h + 1) % height))]
            
            # return neighbors
            return list_of_neighbors

    def tell_all_plants_its_neighbors(self):
        '''
        Shall pass the correct list of neighbouring plants to all plants in the plantmap (in the form of a list of plant objects).
        Also called everytime, a plant object is changed. 
        Currently, we are giving a a plant the six surrounding neighbors that are created by the offset of the rows by half a field.
        For example if we have a 5 x 5 grid and we have torodical edge conditions:
                        (5,0)  (5,1)  (5,2)  (5,3)  (5,4)  (5,5)

        (0,5)       (0,0)  (0,1)  (0,2)  (0,3)  (0,4)  (0,5)       (0,0)
           (1,5)       (1,0)  (1,1)  (1,2)  (1,3)  (1,4)  (1,5)       (0,1)
        (2,5)       (2,0)  (2,1)  (2,2)  (2,3)  (2,4)  (2,5)       (0,2)
           (3,5)       (3,0)  (3,1)  (3,2)  (3,3)  (3,4)  (3,5)       (0,3)
        (4,5)       (4,0)  (4,1)  (4,2)  (4,3)  (4,4)  (4,5)       (0,4)
           (5,5)        (5,0)  (5,1)  (5,2)  (5,3)  (5,4) (5,5)     (0,5)

                    (0,0)  (0,1)  (0,2)  (0,3)  (0,4)  (0,5)

        Here we see, that a plant (a, b) has the neighbors:
            - (a - 1, b)
            - (a - 1, b + 1)
            - (a    , b - 1)
            - (a    , b + 1)
            - (a + 1, b)
            - (a    , b + 1)
        
        For the torodical edge conditions, we have to take modulo 6 (or width/ height of the grid):
            - ((a - 1) % 6,  b % width)
            - ((a - 1) % 6, (b + 1) % 6)
            - (a % 6      , (b - 1) % 6)
            - (a % 6      , (b + 1) % 6)
            - ((a + 1) % 6,  b % 6)
            - (a % 6      , (b + 1) % 6)
        '''
        # Get dimensions of the Maps
        rows = self.get_number_of_rows()
        spots = self.get_number_of_plants_in_one_row()

        # FIXME: DELETE the Following line
        print(f'\nEnvironmen.tell_all_plants_its_neighbors(): number of rows: {rows}')
        print(f'Environmen.tell_all_plants_its_neighbors(): number of spots per row: {spots}\n')

        # Iterate over all positions
        for r in range(rows):
            for s in range(spots):

                # get the plant we are currently at
                current_plant = self.get_plant_at(r, s)

                # create list of neighbors
                # We have six neighbors for default neighborhood (offset rows, torodical edge conditions)
                list_of_neighbors = [self.get_plant_at((r-1) % rows, s % spots), 
                                     self.get_plant_at((r-1) % rows, (s + 1) % spots),
                                     self.get_plant_at((r % rows), (s - 1) % spots),
                                     self.get_plant_at((r % rows), (s + 1) % spots),
                                     self.get_plant_at((r + 1) % rows, (s % 6)),
                                     self.get_plant_at( r % rows, (s + 1) % spots)]
                
                # set neighbors
                current_plant.set_neighbors(list_of_neighbors)
                
    def add_this_Environment_to_all_referenced_plants(self):
        '''
        Description:
        Gets all the items from Plantmap and adds this Environment object to the plant objects in Plantmap.
        Two object types in the Plantmap are asserted: 

        - Plant objects
        - None objects

        Only if we have a Plant object we will ad the environment to it. If we have a None object we wont do anything to it.
        NOTE: The None object type is needed because later we want to let "blank space" where no plants are growing.

        '''
        # Try to set up Plantmap Object (but probably will already be done at this time)
        self.get_plantmap().set_up()

        # Small message that we are going to take the plantmap as complete
        print(f"\n Environment, add_this_Environment_to_all_referenced_plants(): \n Please ensure that all plants are in the Plantmap attribute. \n This method is iterating over all plants saved in plantmap. \n It will add this environment to all plants and will use its location for that. \n ")
        
        # Get all plants from the Plantmap
        plants = self.get_plantmap().get_items()
        
        # import Plant class
        from Plant import Plant

        # iterate over all the "twodimensional list"
        for index_width in range(len(plants)):

            # NOTE: assumes that all nested list have same length, 
            # TODO: That is to be ensured by Plantmap class
            for index_height in range(len(plants[0])):

                # get the Plant object at a ceratin index
                single_plant = plants[index_width][index_height]

                # Assert object type (Should be a Plant object, as set_items() and set single_item_at both ensure Plant type)
                assert isinstance(single_plant, Plant) or single_plant is None, f"Environment, add_this_Environment_to_all_referenced_plants(): \n Assertion of Plant object or None Object failed."

                # add environment to this plant object if it is a Plantobject
                # (we checked before for None or Plant object type)
                if single_plant is not None:

                    # add environment
                    single_plant.add_Environment(self)

        # Finally reports success
        print("Environment, add_this_Environment_to_all_referenced_plants(): \n Assertions of Plant / None obejct were done. \n Completed adding environment to all plants in Plantmap.")
    
    def grow_all_plants(self, watermap: Watermap, shademap: Shademap, print_log=False): 
        '''
        Description:
        Iterates over all plant in Plantmap and calls their Plant.get_growth_values() and Plant.grow_step() function.
        NOTE: We have to execute both in this order to get reasonable growth, see further in Plant.get_growth_values() and Plant.grow_step().
        If None, None objects are given as Map objects nothing is updated.
        Before that, it updates the watermap and shademap to be able to adjust water and light conditions.
        Plants are referring to these conditions and their growth depends on the conditions.
        Raises Type Error if not according Map objects nor None objects were given.

        Parameters:
        - watermap (Watermap or None): A Watermap object. If not None, this CAN be used to update all water-table-depth values at the Map.
        - shademap (Shademap or None): A Shademap object. If not None, this CAN be used to update all external shade values at the Map.
        
        '''
        # Update all environmental conditions if given
        # WATERMAP
        # NONE-case
        if (watermap is None):
            print(f'Environment, grow_all_plants(): watermap parameter is NONE. No values for water-table-depth were updated.')
        
        # if watermap is given, check type
        elif ((watermap is not None) and isinstance(watermap, Watermap)):
            
            # update water-table-depth values
            self.set_watermap(watermap = watermap)
            
        else:
            # raise Typeerror if no watermap or None was given
            raise TypeError(f'Environment, grow_all_plants(): Expected Watermap object for watermap parameter. But received {type(watermap)}.')
        
        # SHADEMAP
        # NONE-case
        if (shademap is None):
            print(f'Environment, grow_all_plants(): shademap parameter is NONE. No values for external shade were updated.')
        
        # if watermap is given, check type
        elif ((shademap is not None) and isinstance(shademap, Shademap)):
            
            # update water-table-depth values
            self.set_shademap(shademap = shademap)
        else:
            # raise Typeerror if no watermap or None was given
            raise TypeError(f'Environment, grow_all_plants(): Expected Shademap object for shademap parameter. But received {type(shademap)}.')

        # Use step method for all plants
        # Iterate over twodimensional itemlist
        plants = self.get_plantmap().get_items()

        # save width
        rows = self.get_number_of_rows()

        # save height
        # NOTE: We assume that all inner list have the same length (to be ensured in Map objects)
        spots = self.get_number_of_plants_in_one_row()

        # Iterate over all plants and let them calculate their growth rates
        # CALUCLATION OF GROWTH VALUES
        for x in range(rows):
            for y in range(spots):
                
                # get the plant object at location (x,y)
                plant = self.get_plantmap().get_item_at(x, y)
                plant.get_growth_values(print_params=print_log)
        
        # Iterate over all plants and let them calculate their actual growth
        # CALUCLATION OF GROWTH
        for x in range(rows):
            for y in range(spots):
                
                # get the plant object at location (x,y)
                plant = self.get_plantmap().get_item_at(x, y)
                plant.grow_step(print_params=print_log)

        # TODO: create data for report?
        # TODO: save last data in a dataframe?

    def grow_all_plants_LAOLA(self, watermap: Watermap, shademap: Shademap, print_log=False):
        '''
        Description:
        Iterates over all plant in Plantmap and calls their Plant.get_growth_values() and Plant.grow_step() function.
        NOTE: We have to execute both in this order to get reasonable growth, see further in Plant.get_growth_values() and Plant.grow_step().
        If None, None objects are given as Map objects nothing is updated.
        Before that, it updates the watermap and shademap to be able to adjust water and light conditions.
        Plants are referring to these conditions and their growth depends on the conditions.
        Raises Type Error if not according Map objects nor None objects were given.

        Parameters:
        - watermap (Watermap or None): A Watermap object. If not None, this CAN be used to update all water-table-depth values at the Map.
        - shademap (Shademap or None): A Shademap object. If not None, this CAN be used to update all external shade values at the Map.
        
        '''
        # Update all environmental conditions if given
        # WATERMAP
        # NONE-case
        if (watermap is None):
            print(f'Environment, grow_all_plants(): watermap parameter is NONE. No values for water-table-depth were updated.')
        
        # if watermap is given, check type
        elif ((watermap is not None) and isinstance(watermap, Watermap)):
            
            # update water-table-depth values
            self.set_watermap(watermap = watermap)
            
        else:
            # raise Typeerror if no watermap or None was given
            raise TypeError(f'Environment, grow_all_plants(): Expected Watermap object for watermap parameter. But received {type(watermap)}.')
        
        # SHADEMAP
        # NONE-case
        if (shademap is None):
            print(f'Environment, grow_all_plants(): shademap parameter is NONE. No values for external shade were updated.')
        
        # if watermap is given, check type
        elif ((shademap is not None) and isinstance(shademap, Shademap)):
            
            # update water-table-depth values
            self.set_shademap(shademap = shademap)
        else:
            # raise Typeerror if no watermap or None was given
            raise TypeError(f'Environment, grow_all_plants(): Expected Shademap object for shademap parameter. But received {type(shademap)}.')

        # Use step method for all plants
        # Iterate over twodimensional itemlist
        plants = self.get_plantmap().get_items()

        # save width
        rows = self.get_number_of_rows()

        # save height
        # NOTE: We assume that all inner list have the same length (to be ensured in Map objects)
        spots = self.get_number_of_plants_in_one_row()

        # Iterate over all plants and let them calculate their growth rates
        # CALUCLATION OF GROWTH VALUES
        for x in range(rows):
            for y in range(spots):
                
                # get the plant object at location (x,y)
                plant = self.get_plantmap().get_item_at(x, y)
                plant.get_growth_values(print_params=print_log)

                # NOTE: LAOLA feature HERE we directly grow each plant after calculation of the growth rate
                plant.grow_step(print_params=print_log)

        # TODO: create data for report?
        # TODO: save last data in a dataframe?

    def get_plant_at(self, index_row: int, index_spot_in_row: int):
        '''
        Description:
        Returns a plant at a given location.
        NOTE: BoundHandling of coordinates is done in Plantmap.get_item_at()
        
        Parameter:
        - location_x (Integer): coordinate related to the width of the simulated field
        - location_y (Integer): coordinate related to the height of the simulated field

        TODO:
        - Handle Gap (if we access at a gap of Plants)
        '''
        # Access items of Plantmap at certain location
        plant = self.get_plantmap().get_item_at(index_row, index_spot_in_row)

        # return Plant object
        return plant
    
    def add_environment_to_plants_and_tell_neighbors(self):

        '''
        This method executes 
            - Plant.add_this_Environment_to_all_referenced_plants()
            - Plant.tell_all_plants_its_neighbors()
        This lets all plants know in which environment object they are referenced 
        and maps the neighbors to each other (usually torodical, depends on what is defined in tell_all_plants_its_neighbors).
        So basically, we make the plants ready to grow in company and tell them which environmental data they 
        should consider.
        '''
        # say all plants that this is their environment
        self.add_this_Environment_to_all_referenced_plants()

        # in the following line we establish neighbor relations for the defined edge conditions
        self.tell_all_plants_its_neighbors()

        # print Messsage
        print(f'Environment.add_environment_to_plants_and_tell_neighbors() successfully established Plant-Environment and Plant-Plant references.') 

    def set_k_prod_and_k_elong_for_all_plants(self, k_prod:float, k_elong: float, print_log=False):
        '''
        ## DESCRIPTION
        Sets the parameter for the exposure effect for all Plants in Plantmap.

        ## PARAMETER
        - k_prod: *float*  
        Parameter to modulate the exposure effect for mass growth.   

        - k_elong: *float*
        Parameter to modulate the exposure effect for length growth.

        - print_log, *boolean*, *Deafult* **False**:
        Parameter that determines whether we print successful operations.

        '''
        #

        # set the new parameters for every plant 
        for row in range(self.get_plantmap().get_number_of_rows()):
            # check for Plant
            for spot in range(self.get_plantmap().get_number_of_spots_per_row()):

                # get the plant at the location
                plant = self.get_plantmap().get_item_at(index_row=row, index_spot_in_row=spot)

                if isinstance(plant, Plant):
                    # Update parameter values
                    plant.set_k_prod(k_prod=k_prod)
                    plant.set_k_elong(k_elong=k_elong)

                    if print_log:
                        print(f'Environment.set_k_prod_and_k_elong_for_all_plants(): \n All plants have now\n k_elong = {k_elong} and \nk_prod = {k_prod}.\n')
                
                # print Message if not
                else:
                    print(f'Environment.set_k_prod_and_k_elong_for_all_plants(): WARNING: One object in plantmap.get_items() was no plant (type of the {i}th item: {type(plant)}). \n')
            