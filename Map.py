import numpy as np
from Plant import Plant 
import warnings

class Map:
    # TODO: Define how to let "gaps" where we do not want to have plants growing
    # TODO: Iterator class

    def __init__(self, number_of_spots_per_row, number_of_rows, items, resolution = 1.0):
        self._number_of_spots_per_row = number_of_spots_per_row 
        # number_of_rows is here meant as spatial dimensions of the area
        self._number_of_rows = number_of_rows
        self.items = items
        self.resolution = resolution

        # used to enforce a controlled first value setting for the values we want to have here
        self._set_up = False
    
    # Check for Set-Up
    def _check_set_up(self):
        if self._set_up:
            pass
        else:
            raise PermissionError(f'Map Object has to be properly set up by running set_up() to be usable. Run set_up() to fill the items with default object. Then set them properly with Plantmap.set_items() or do it individually for each plant.')

    # GETTER
    def get_set_up(self):
        return self._set_up

    def get_number_of_spots_per_row(self):
        # Check for proper Set_up
        self._check_set_up()

        return self._number_of_spots_per_row
    
    def get_number_of_rows(self):
        # Check for proper Set_up
        self._check_set_up()

        return self._number_of_rows
    
    def get_items(self):
        # Check for proper Set_up
        self._check_set_up()

        return self.items
    
    def get_resolution(self):
        # Check for proper Set_up
        self._check_set_up()

        return self.resolution
    
    def get_item_at(self, location: tuple):
        '''
        To be implemented by subclasses
        '''
        # To be implemented by subclasses
        pass
    
    # SETTER

    def set_number_of_spots_per_row(self, number_of_spots_per_row):
        # Check for proper Set_up
        self._check_set_up()

        # check for Integer
        if not(isinstance(number_of_spots_per_row, int)):
            raise TypeError(f"Wrong DataType, a {type(number_of_spots_per_row)} for width was given. We need an integer.")
            
        else:
            self.number_of_spots_per_row = number_of_spots_per_row

    def set_number_of_rows(self, number_of_rows):
        # Check for proper Set_up
        self._check_set_up()

        # check for Integer
        if not(isinstance(number_of_rows, int)):
            raise TypeError(f"Wrong DataType, a {type(number_of_rows)} for number of rows was given. We need an integer.")
            
        else:
            self.number_of_rows = number_of_rows    

    def set_items(self, items):
        # Check for proper Set_up
        self._check_set_up()

        # every subclass does this independently
        pass

    def set_single_item_at(self, new_item, location: tuple):
        # To be defined in every subclass
        # Check for dimensionlity of location
        if not(len(location) == 2):
            # raise Error
            raise TypeError(f'Map.set_single_item_at(): Location Not a two-dimensional tuple, a tuple of dimension {len(location)} was given.')
        else:
            # do nothing, to be implemented by the subclasses
            pass

    ### Methods ####

    def set_up(self):
        # If not yet set_up
        if not(self._set_up):
            self._set_up = True
    
    def check_map_compatibility(self, map_to_be_checked):
        '''
        Checks if the number_of_spots_per_row and HEIGHT attributes of the two maps are equal.
        Returns True if so and False otherwise.
        Meant as a tool to quickly and thoroughly check for the compatibility of two maps.

        PARAMETERS: 
        - self: Map Object
        - map_to_be_checked: Map Object to be checked for number_of_spots_per_row / height

        RETURN VALUES:
        compatible: boolean
        - True if attributes number_of_spots_per_row and height_geo of self and map_to_be_checked are equal
        - False otherwise
        '''
        compatible = False

        # Check for Map object
        if not(isinstance(map_to_be_checked, Map)):
            warnings.warn(f'Map.check_map_compatibility(): Wrong Type for map_to_be_checked. Expected Map object, {type(map_to_be_checked)} was given', TypeError)
        # If map_to_be_checked is a Map object than look for same number_of_spots_per_row and height 
        else:
            # Check dimensions
            compatible = (self.get_number_of_spots_per_row() == map_to_be_checked.get_number_of_spots_per_row() and self.get_number_of_rows() == map_to_be_checked.get_number_of_rows())
        
        # return if compatible in number_of_spots_per_row and Height
        # NOTE: In the subclasses we will implement the check for same type of Map (Water-, Plant-, Shade-)
        return compatible


####### PLANTMAP ###########################################

class Plantmap(Map):

    def __init__(self, species:str, number_of_spots_per_row, number_of_rows, items, resolution=1.0):
        super().__init__(number_of_rows=number_of_rows, number_of_spots_per_row=number_of_spots_per_row, items=items, resolution=resolution)
        if species in ['capillifolium', 'papillosum']:
            self._species = species
        else:
            raise ValueError(f'Plantmap.__init__(): {species} is no valid species name. We need capillifolium or papillosum.')
    
    def get_species(self):
        '''
        Returns the species name, that all plants are in the plant map
        '''
        # Check for existing species attribute
        if self._species == None:
            raise ValueError(f'Planmap.get_species(): NO SPECIES IS DEFINED!')
        
        else:
            return self._species
    
    def set_species(self, species:str):
        if species in ['capillifolium', 'papillosum']:
            self._species = species
        else:
            print(f'Plantmap.set_species(): No such species as {species}. No update was made.')

    def set_items(self, items):
        # TODO: Documentation
        super().set_items()
        # Check for List
        if not(isinstance(items, list)):
            raise TypeError(f'Plantmap.set_items(): Wrong Data Type for items in Plantmap, a list has to be passed, but a {type(items)} was given')
        
        # Check for dimensions by checking 
        # (TODO: Think about: Switch to Numpy arrays? Can they store self written classes)?
        elif not(len(items) == super().get_number_of_rows() and len(items[0]) == super().number_of_spots_per_row()):
            raise ValueError(f'Plantmap: The dimensions for the plantmap are not correct. A list of \n len {super().get_number_of_rows() } x len {super().get_number_of_spots_per_row() } \n  is needed. But a list of \n len {len(items) } x len {len(items[0])} \n was given')

        # TODO: Check for the length of ALL nested lists, not just items[0]

        else:
            # Check for only Plant objects
            for i, plantlist in enumerate(items):
                for j, plant in enumerate(plantlist):
                    if not(isinstance(plant, Plant)):
                        all_items_are_plants = False
                        raise TypeError(f'Plantmap, set_items(): Wrong data type of one element. The passed list of plants to the Plantmap object contains one NO-PLANT object at index ({i}, {j}).')
            
            # finally set neighbors
            self.items = items          
    
    def set_up(self, species:str = '', init_mode_height='', mean_height = 0.0, std = 1.0):
        '''
        ## PARAMS
        - species, String: either 'capillifolium' or 'papillosum', defines the plant species if set up,   
        Default '' will result in using the species we saved in Plantmap.__init__()
        - init_mode_height, String: If 'NORM_DIST' is passed, 
                                    plants heights are initiated by drawing from an 
                                    normal distribution 
                                    with mean = mean_height and
                                    standard_deviation = std

                                    If 'UNIFORM' is passed,
                                    plants heights are initiated by drawing from a
                                    uniform distribution
                                    of value mean_height

        - mean_height, float:       number describing the mean of the distribution, 0.0 by Default
        - std, float:               standard deviation describing the normal distribution, if applicable, 1.0 by Default
        DESCRIPTION:

        Initiates a default set of plants on this map with the given specs in the constructor.
        WITHOUT CALLING THIS METHOD NOTHING CAN BE DONE TO THIS MAP OBJECT

        What are default plants here?
        - height = 0
        - mass = 0
        - water_table_depth = 0 cm
        - shade = 0.0
        - location (given)
        - neighbors = None
        - environment = None

        NOTE: Sets the items (in this case, as we are in class Plantmap, Plant objects).
        It is done to check that a "two-dimensional", correctly formatted list is given.
        What requirements are necessary for the list to be suitable?
        - "Two-dimensional": We need a list, that contains list of equal length
        - data-type: plant objects are needed
        - length of inner list: number_of_spots_per_row (the attribute of the map)
        - lenght of outer lists: number_of_rows (the attribute of the map)
        
        If called, the super method is called and sets a marker (a boolean) to True to mark that this list has been properly set up.
        Without this call the other functions will return an Error.
        Sets the items to be default plants with a given location. 

        NOTE:
        • I discovered, that If we imagine the rows to be horizontically, the handling of the items in the maps does not make a lot of sense, as I practically access items like this:
            ◦ (x,y) item = items[x][y]
        • But our items array is like this:
        ◦   [[e11, e12, e13, …]
            [e21, e22, e23, …]
            [e31, e32, e33, …]
             ….. 
            ]

        • So if we imagine the rows to be represented by the inner arrays, than we have to acces in the manner 
            ◦ (x,y) = items[y][x]

        EDIT:
        We will follow: (x,y) = (row_number, number_of_spot_in_row):

                         (5,0)  (5,1)  (5,2)  (5,3)  (5,4)  (5,5)

        (0,5)       (0,0)  (0,1)  (0,2)  (0,3)  (0,4)  (0,5)       (0,0)
           (1,5)       (1,0)  (1,1)  (1,2)  (1,3)  (1,4)  (1,5)       (0,1)
        (2,5)       (2,0)  (2,1)  (2,2)  (2,3)  (2,4)  (2,5)       (0,2)
           (3,5)       (3,0)  (3,1)  (3,2)  (3,3)  (3,4)  (3,5)       (0,3)
        (4,5)       (4,0)  (4,1)  (4,2)  (4,3)  (4,4)  (4,5)       (0,4)
           (5,5)        (5,0)  (5,1)  (5,2)  (5,3)  (5,4) (5,5)     (0,5)

                    (0,0)  (0,1)  (0,2)  (0,3)  (0,4)  (0,5)

        '''
        # load species if neccessary
        if species == '':
            species = self.get_species()
            
        # print message regarding mode of initialization
        print(f'Mode for initiating plant height: {init_mode_height}')

        # Check if Map has already been set up
        if self.get_set_up():
            # Settig up
            print("Plantmap, set_up(): This Plantmap has already been set up.")
        
        # if it has NOT been Set up yet create Plantmap with defualt Plant object
        else:
            super().set_up()
            # helper list
            help_outer_list = []

            # print: FIXME DELETE
            print(f'Plantmap.set_up(): super().get_number_of_rows(): {super().get_number_of_rows()}')
            print(f'Plantmap.set_up(): super().get_number_of_spots_per_row(): {super().get_number_of_spots_per_row()}')


            # Initialize a set of plants with default constructor except location
            # of Plant objects (number values (mass, initial_height, ...) are 0, complex variables (neighbors, environment) are None)
            for row in range(super().get_number_of_rows()):
                print(f'ROW: {row}')

                # helps to save a list of plants
                help_inner_list = []

                for spot_in_row in range(super().get_number_of_spots_per_row()):
                    print(f'Spot_in_row: {spot_in_row}')

                    # create Plant objects with default constructor (see Description above for-loops, see Plant for default constructor)
                    local_plant = Plant(self.get_species(), location = (row, spot_in_row))

                    # if we want to get initial heights drawn from a normal distribution
                    if (init_mode_height == 'NORM_DIST'):

                        # draw a value from the normal distribution specified by the optional arguments for mean and standar deviation
                        random_height = np.random.normal(loc=mean_height, scale=std)

                        # set the height of the local plant to
                        local_plant.set_height(random_height)

                        # FIXME: DELETE following line Testprint
                        print(f'Plantmap.set_up(): Plants were initialized in height by value {random_height} from normal distribution with mean = {mean_height}\n and std = {std}.')
                    
                    # if we want to create Plants of a uniform height
                    elif(init_mode_height == 'UNIFORM'):

                        # make all plants the same height specified by mean height
                        local_plant.set_height(mean_height)

                        # FIXME: DELETE following line Testprint
                        print(f'Plantmap.set_up(): Plants were initialized in height by value {random_height} from uniform distribution with mean = {mean_height}.')
                    
                    # No special mode
                    else:
                        print('Plantmap.set_up(): No special distribution was applied for initial heights.')

                    
                    # Append plant object to help_inner_list
                    help_inner_list.append(local_plant)
                
                # FIXME: Delete this line
                print(f'len(help_inner_list): {len(help_inner_list)}')

                # fill the help_outer_list with the help_inner_list
                # That is how we get i entries in help_outer_list of lists with j entries
                # In other words: we append help_inner_list of length j exactly i times
                help_outer_list.append(help_inner_list) 

            # Finally set items by giving a number_of_spots_per_row x number_of_rows list
            self.items = help_outer_list
            

            # Spit a warning
            print(f'\n PLANTMAP.set_up(): Sucessfully set up PLANTMAP object with dimensions \n width = {super().get_number_of_rows()} and height = {super().get_number_of_rows()}. \n All plant objects are indeed plant objects and now have \n Water-table depth = 0 cm \n Shade = 0.0 \n mass = 0.0 g \n height = 0.0 cm \n neighbors = [] \n environment = None \n \n Setting all these attributes is still needed! \n Especially setting the Environment and Neighbors is crucial! \n', UserWarning)
            
    def check_map_compatibility(self, map_to_be_checked):
        '''
        Checks for same dimensions of Maps (number_of_spots_per_row and height) and for same Maptype

        RETURNS: 
        True: if .... 
                    - Attributes (height and number_of_spots_per_row) of map_to_be_checked are equal to attributes of this object 
                    - Same Map type (here a PLANTmap)
        Otherwise: False
        '''
        # call super function
        compatible_in_dimensions = super().check_map_compatibility(map_to_be_checked)

        # If number_of_spots_per_row and number_of_rows are already distinct for the two Maps, return False immediately
        if not(compatible_in_dimensions):
            return False
        
        else:
            # Check for same Map type
            compatible_in_maptype = isinstance(map_to_be_checked, Plantmap)

            # Assertion, gives a warning to be aware of wrong type 
            assert compatible_in_maptype, f'Plantmap.check_map_compatibility(): {type(map_to_be_checked)} given. Not compatible to this Plantmap.'
            
            # Return
            return compatible_in_maptype
        
    def set_single_item_at(self, new_item: Plant, location: tuple):
        '''
        Sets a new item (Plant object, shade value (float) or waterdepth (float)) in the items List.

        Parameters:
        - location: Two dimensions Tuple that defines the position in the system of maps (number_of_spots_per_row-coordinate, height-coordinate)
        - new_item (Plant object): Plant object to be set on a certain location
        '''
        super().set_single_item_at(new_item, location)
        
        # set correct Plant location
        new_item.set_location(location)

        # specify what shall happen if we want to set a plant in the list
        # TODO: Check for dimension, Bounds, 

        first_entry, second_entry = location[0], location[1]

        # Update Plant object
        self.get_items()[first_entry][second_entry] = new_item

    def get_items(self):
        '''
        Returns a list of plant objects.
        Overwrites the super method.
        '''
        # get items
        return self.items

    def get_item_at(self, index_row: int, index_spot_in_row: int ):
        '''
        Returns the Plant object at a certain location.
        If not a plant object assertion warning is given.
        Still in need to handle gaps of plants.

        TODO: See Todos below
        '''
    
        # access plantmap at given location
        plant = self.items[index_row][index_spot_in_row]

        # TODO: Bounds Handling
        # TODO: "gap handling"? -> if there is no plant but only peat / bog
        # Assert that we really got the plant we wanted and did not get a confused location due to the creation of the items in 
        # XMap.set_up(): The first entry corresponds to the x-axis but to the OUTER "shell" of the twodimensional array items. 
        # The second entry refers to the y-axis but to the second positional argument in the items-array
        if(isinstance(plant, Plant) and (plant.get_location() != (index_row, index_spot_in_row))):
            print(f'Plantmap.get_item_at(): WARNING, the given location {(index_row, index_spot_in_row)} do not correspond to the Plants internal location {plant.get_location()}.')

        # Check for Plant object
        assert isinstance(plant, Plant), f"Plantmap, get_item_at(): No plant object at location ({index_row}, {index_spot_in_row})"

        # Return
        return plant
    
    def get_heights_and_mass(self):
        '''
        Returns two twodimensional arrays with all the plants heights and masses:
        - heights (np.array) of shape (self.get_height(), self.number_of_spots_per_row())
        - masses  (np.array) of shape (self.get_height(), self.number_of_spots_per_row())
        '''
        # get all the plants
        plants = self.get_items()

        # make two dimensional numpy array placeholder
        heights = np.zeros((self.get_number_of_rows(), self.get_number_of_spots_per_row()))
        masses = np.zeros_like(heights)

        # Fill the placeholder with actual values
        for x in range(self.get_number_of_rows()):
            for y in range(self.get_number_of_spots_per_row()):
                
                # save height and mass at position (x,y)
                # NOTE: get_item_at makes sure that we get the right item
                local_plant = self.get_item_at(x, y)

                # access height and mass
                # NOTE: As we have a row (in x-direction) in each inner array, the first coordinate says which row (so the y-axis), 
                # while the second coordinate says which spot in the row (x-axis)
                # This is why the coordinates seem changed
                heights[x][y] = local_plant.get_height()
                masses[x][y] = local_plant.get_mass()
        
        # return both arrays
        return heights, masses

####### SHADEMAP ###########################################

class Shademap(Map):

    def __init__(self, number_of_spots_per_row, number_of_rows, items, resolution=1):
        super().__init__(number_of_rows=number_of_rows, number_of_spots_per_row=number_of_spots_per_row, items=items, resolution=resolution)

    def set_items(self, items : np.ndarray):
        super().set_items(items)
        # Check for correct data type 
        # TODO: Check for float
        if not(isinstance(items, np.ndarray)):
            # raise Error if not correct data type 
            raise TypeError(f'Shademap.set_items(): Numpy array expected, got {type(items)}')
        
        # Check for dimensionality
        elif(items.shape != (self.get_number_of_rows(), self.get_number_of_spots_per_row())):
            raise TypeError(f'Shademap.set_items(): items Numpy array has the wrong dimension, expected ({self.get_number_of_rows()} , {self.get_number_of_spots_per_row()}) but got {items.shape}')

        # if conditions are matched
        else:
            self.items = items
    
    def set_up(self, constant_value=0.0):
        '''
        DESCRIPTION:

        Initiates a default set of values for shade on this map with the given specs in the constructor.
        WITHOUT CALLING THIS METHOD NOTHING CAN BE DONE TO THIS MAP OBJECT

        What is default shade here?
        - shade = 0.0 (refers to no external shade at all)

        Sets the items (in this case, as we are in class Shademap, float values).
        
        If called, the super method is called and sets a marker (a boolean) to True to mark that this objectist has been properly set up.
        Without this call the other functions will return an Error.

        '''
        super().set_up()

        # create Numpy Array with zeros of shape number_of_spots_per_row and number_of_rows
        values = np.zeros((self.get_number_of_rows(), self.get_number_of_spots_per_row()), float)

        # save the constant value for all spots if desired
        if constant_value != 0.0:
            values[:,:] = constant_value

        # Set the items attribute
        self.items = values

        # warn that further specification of values is needed
        print(f'Sucessfully set up Shademap object with dimensions \n number_of_rows = {super().get_number_of_rows()} \n number_of_spots_per_row = {super().get_number_of_spots_per_row()} . \n Values of Shade are still to be specified.') 

    def check_map_compatibility(self, map_to_be_checked):
        '''
        Checks for same dimensions of Maps (number_of_spots_per_row and height) and for same Maptype

        RETURNS: 
        - True: if .... 
                    1. Attributes (height and number_of_spots_per_row) of map_to_be_checked are equal to attributes of this object 
                    2. Same Map type (here a Shademap)

        -
        '''
        # call super function
        compatible_in_dimensions = super().check_map_compatibility(map_to_be_checked)

        # If number_of_spots_per_row and height are already distinct for the two Maps, return False immediately
        if not(compatible_in_dimensions):
            return False
        
        else:
            # Check for same Map type
            compatible_in_maptype = isinstance(map_to_be_checked, Shademap)

            # Assertion, gives a warning to be aware of wrong type 
            assert compatible_in_maptype, f'Shademap.check_map_compatibility(): {type(map_to_be_checked)} given. Not compatible to this Shademap.'
            
            # Return
            return compatible_in_maptype

    def set_single_item_at(self, new_item: float, location: tuple):
        '''
        Sets a new item (Plant object, shade value (float) or waterdepth (float)) in the items List.

        Parameters:
        - location: Two dimensions Tuple that defines the position in the system of maps (number_of_spots_per_row-coordinate, height-coordinate)
        - new_item (float): value of shade between 0 and 1.0
        '''
        super().set_single_item_at()

        # specify what shall happen if we want to set a plant in the list
        # TODO: Check for dimension, Bounds, 

        x, y = location[0], location[1]

        self.get_items()[x][y] = new_item

####### WATERMAP ###########################################

class Watermap(Map):

    def __init__(self, number_of_spots_per_row, number_of_rows, items, resolution=1):
        super().__init__(number_of_rows=number_of_rows, number_of_spots_per_row=number_of_spots_per_row, items=items, resolution=1.0)
    
    def set_items(self, items: np.ndarray):
        super().set_items(items)
        # Check for correct data type
        if not(isinstance(items, np.ndarray)):
            # raise Error if not correct data type 
            raise TypeError(f'Watermap.set_items(): Numpy array expected, got {type(items)}')
        
        # Check for dimensionality
        elif(items.shape != (self.get_number_of_rows(), self.get_number_of_spots_per_row())):
            raise TypeError(f'Watermap.set_items(): items Numpy array has the wrong dimension, expected ({self.get_number_of_rows()}, {self.get_number_of_spots_per_row()}) but got {items.shape}')

        # if conditions are matched
        else:
            self.items = items
    
    def set_up(self, constant_value = 0.0):
        '''
        DESCRIPTION:

        Initiates a default set of values for water-table depth on this map with the given specs in the constructor.
        WITHOUT CALLING THIS METHOD NOTHING CAN BE DONE TO THIS MAP OBJECT

        What is default shade here?
        - water-table depth = 0.0 (refers to perfect water table at the top of the plant)

        Sets the items (in this case, as we are in class Watermap, float values).
        
        If called, the super method is called and sets a marker (a boolean) to True to mark that this objectist has been properly set up.
        Without this call the other functions will return an Error.

        ## PARAMETER
        constant_value *float*  
        If _not_ zero, all entries are set to this value

        '''
        super().set_up()

        # create Numpy Array with zeros of shape number_of_spots_per_row and number_of_rows
        values = np.zeros((self.get_number_of_rows(), self.get_number_of_spots_per_row()), float)

        # save the constant value for all spots if desired
        if constant_value != 0.0:
            values[:,:] = constant_value

        # Set the items attribute
        self.items = values

        # warn that further specification of values is needed
        print(f'Sucessfully set up WATERMAP object with dimensions \nnumber_of_rows = {super().get_number_of_rows()} \nnumber_of_spots_per_row = {super().get_number_of_spots_per_row()}. \n Values of Water-table depth are still to be specified.') 
    
    def check_map_compatibility(self, map_to_be_checked: Map):
        '''
        Checks for same dimensions of Maps (number_of_spots_per_row and number_of_rows) and for same Maptype

        RETURNS: 
        True: if .... 
                    - Attributes (number_of_rows and number_of_spots_per_row) of map_to_be_checked are equal to attributes of this object 
                    - Same Map type (here a Watermap)

        False otherwise.
        '''
        # call super function
        compatible_in_dimensions = super().check_map_compatibility(map_to_be_checked)

        # If number_of_spots_per_row and number_of_rows are already distinct for the two Maps, return False immediately
        if not(compatible_in_dimensions):
            # print
            print(f'Watermap.check_map_compatibility(): Watermaps were not comaptible. \nProbably due to shape: \nno rows (map saved here): {super().get_number_of_rows()}\nno spots (map saved here): {super().get_number_of_spots_per_row()} \nno rows (new map): {map_to_be_checked.get_number_of_rows()}\nno spots (new map): {map_to_be_checked.get_number_of_spots_per_row()}')
            return False
        
        else:
            # Check for same Map type
            compatible_in_maptype = isinstance(map_to_be_checked, Watermap)

            # Assertion, gives a warning to be aware of wrong type 
            assert compatible_in_maptype, f'Watermap.check_map_compatibility(): {type(map_to_be_checked)} given. Not compatible to this Watermap.'
            
            # Return
            return compatible_in_maptype

    def set_single_item_at(self, new_item: float, location: tuple):
        '''
        Sets a new item (Plant object, shade value (float) or waterdepth (float)) in the items List.

        Parameters:
        - location: Two dimensions Tuple that defines the position in the system of maps (number_of_spots_per_row-coordinate, number_of_rows-coordinate)
        - new_item (float): value of waterdepth 
        '''
        super().set_single_item_at()

        # specify what shall happen if we want to set a plant in the list
        # TODO: Check for dimension, Bounds, 

        row, spot_in_row = location[0], location[1]

        # Update value
        self.get_items()[row][spot_in_row] = new_item