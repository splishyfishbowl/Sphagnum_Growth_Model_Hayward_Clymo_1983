# Import Numpy
import numpy as np

class Growth_Processes_Model:
    

    def __init__(self):
        self._number_of_days_experiment_conducted = 77
        self._print_log = False

        # Variables regarding the polynomial growth functions
        self._treat_values_outside_polynomial_growth_as_constants = True
        self._approximate_height_by_mass = False
        self._cap_zero = True
        self._minimum_water_table_distance_allowed = 0.0
        self._maximum_water_table_distance_allowed = 14.0
        self._minimum_shade_value_allowed = 0.0
        self._maximum_shade_value_allowed = 1.3
        print('Growth_Processes_Model initialized')
    
    ####### GETTER ################################################
    def get_cap_zero(self):
        '''
        Defines whether we allow negative growth as results from our polynomial equations.
        If True, they are not allowed and replaced by zero.
        If False, they are allowed.
        '''
        return self._cap_zero

    def get_number_of_days_experiment_conducted(self):
        '''
        Get the duration in days the experiment took place.
        Is the value by which we normalize the polynomial functions.
        '''
        return self._number_of_days_experiment_conducted
    
    def get_approximate_height_by_mass(self):
        '''
        Returns whether we approximate height growth rates above 15 cm by using the growth mass rates and interpolation
        '''
        return self._approximate_height_by_mass

    def get_print_log(self):
        return self._print_log
    
    def get_treat_values_outside_polynomial_growth_as_constants(self):
        return self._treat_values_outside_polynomial_growth_as_constants
    
    def get_minimum_water_table_distance_allowed(self):
        '''
        Returns the value for the lower bound for water-table distance values, we want to consider.
        Values of wtd lower than this, are considered to be the minimum water table distance (see polynomials for growth mass and growth height).
        '''
        return self._minimum_water_table_distance_allowed
    
    def get_maximum_water_table_distance_allowed(self):
        '''
        Returns the value for the upper bound for water-table distance values, we want to consider.
        Values of wtd higher than this, are considered to be the maximum water table distance (see polynomials for growth mass and growth height).
        '''
        return self._maximum_water_table_distance_allowed
    
    def get_minimum_shade_value_allowed(self):
        '''
        Returns the value for the lower bound for shade values, we want to consider.
        Values of shade lower than this are considered to be the minimum shade value (see polynomials for growth mass and growth height).
        '''
        return self._minimum_shade_value_allowed
    
    def get_maximum_shade_value_allowed(self):
        '''
        Returns the value for the upper bound for shade values, we want to consider.
        Values of shade higher than this are considered to be the maximum shade value (see polynomials for growth mass and growth height).
        '''
        return self._maximum_shade_value_allowed

    ####### SETTER #################################################
    def set_cap_zero(self, cap_zero: bool):
        '''
        Defines whether we allow negative growth as results from our polynomial equations.
        If True, they are not allowed and replaced by zero.
        If False, they are allowed.
        '''
        self._cap_zero = cap_zero

    def set_print_log(self, print_log:bool):
        self._print_log = print_log
    
    def set_treat_values_outside_polynomial_growth_as_constants(self, treat_values_outside_polynomial_growth_as_constants: bool):
        '''
        If True, the polynomials in growth_mass and growth_height are only used on the bounds defined by  
        - _minimum_water_table_distance_allowed (Default: 0.0)
        - _maximum_water_table_distance_allowed (Default: 14.0)
        and
        - _minimum_shade_value_allowed (Default: 0.0)
        - _maximum_shade_value_allowed (Default: 1.3)

        If values are outside, they will be treated as the bound values. So outside of the bounds, the functions become constant.
        '''
        self._treat_values_outside_polynomial_growth_as_constants = treat_values_outside_polynomial_growth_as_constants
    
    def set_approximate_height_by_mass(self, approximate_height_by_mass: bool):
        '''
        Sets, whether we approximate height growth rates above 15 cm by using the growth mass rates and interpolation.
        '''
        # FIXME Delete
        print(f'Growth_Processes_Model.set_approximate_height_by_mass(): turned to {approximate_height_by_mass}')
        self._approximate_height_by_mass = approximate_height_by_mass

    def set_minimum_water_table_distance_allowed(self, min_wtd=0.0):
        '''
        Default = 0.0
        Sets the value for the lower bound for water-table distance values, we want to consider.
        Values of wtd lower than this, are considered to be this water table distance (see polynomials for growth mass and growth height).
        '''
        self._minimum_water_table_distance_allowed = min_wtd

    def set_maximum_water_table_distance_allowed(self, max_wtd=14.0):
        '''
        Default = 14.0
        Sets the value for the upper bound for water-table distance values, we want to consider.
        Values of wtd higher than this, are considered to be this water table distance (see polynomials for growth mass and growth height).
        '''
        self._maximum_water_table_distance_allowed = max_wtd

    def set_minimum_shade_allowed(self, min_shade=0.0):
        '''
        Default = 0.0
        Sets the value for the lower bound for shade values, we want to consider.
        Values of shade lower than this are considered to be this shade value (see polynomials for growth mass and growth height).
        '''
        self._minimum_shade_value_allowed = min_shade

    def set_maximum_shade_value_allowed(self, max_shade=1.3):
        '''
        Default = 1.3
        Sets the value for the upper bound for shade values we want to consider.
        Values of shade higher than this are considered to be this shade value (see polynomials for growth mass and growth height).
        '''
        self._maximum_shade_value_allowed = max_shade

    ##################################################################

   ##### METHODS #####################################################

    def polynomial_respects_bounds_by_constant(self, wtd:float | int, shade:float | int):
        '''
        ## Returns
        Returns the values corrected by the bounds
        Maps all values of wtd and shade into the bounds.

        Checks for the bounds defined by
        - _minimum_water_table_distance_allowed (Default: 0.0)
        - _maximum_water_table_distance_allowed (Default: 14.0)
        and
        - _minimum_shade_value_allowed (Default: 0.0)
        - _maximum_shade_value_allowed (Default: 1.3)

        If values are outside, they will be treated as the bound values. So outside of the bounds, the functions become constant.
        
        ## Parameter
        - wtd: *float* or *Integer*
        The distance to the water table in cm, positive value (e.g. between 0.0 and 14.0)

        - shade: *float* or *Integer*  
        The external shade value as an absorbance value.
        '''
        # Get the bounds
        min_wtd = self.get_minimum_water_table_distance_allowed()
        max_wtd = self.get_maximum_water_table_distance_allowed()
        min_shade = self.get_minimum_shade_value_allowed()
        max_shade = self.get_maximum_shade_value_allowed()

        # we are checking the bounds
        wtd_in_bounds = (wtd < min_wtd) * min_wtd  + (wtd >= min_wtd) * (wtd <= max_wtd) * wtd + (wtd > max_wtd) * max_wtd 
        shade_in_bounds = (shade < min_shade) * min_shade  + (shade >= min_shade) * (shade <= max_shade) * shade + (shade > max_shade) * max_shade

        # return corrected values
        return wtd_in_bounds, shade_in_bounds
    

    def get_extinction_coef(self, water_table_depth_in_cm:float, ext_shade = 0.0):
        '''
        ## RETURN VALUES
        - extinction_coef: (array, float) coefficient to modulate Beers Law.  
                            First entry: extinction coefficient for S. capillifolium  
                            Second entry: extinction coefficient for S. papillosum
        ## DESCRIPTION
        Calculates the extinction coefficient used in Beers Law and returns it as an ARRAY
        
        ## PARAMETERS 
            - ext_shade: External shade (as a value of absorbance, e.g. 0.2) determined by the environmental conditions. By default 0 (mimics the conditions when no vascular plants are nearby)
            - water_table_depth_in_cm:  Water table depth in cm. Measured from the tip of the plant to the water table surface
        

        NOTES/QUESTIONS:
            - Not 100% sure, if this really describes the coefficient from Beers Law or a mortality rate (p. 857, first paragraph)
            - Coefficients are found on p. 857, Table 6 (EXT)
        
        TODOS: 
            - Handle the array type in the return object
        
        ASSUMPTIONS:
            - constant for values outside [3,15] x [0, 0.8] !
            - This value describes the extinction coefficient for Beers Law (my interpretation of the paper)
            - Quadratic multidimensional fitted function is applicable to determine such coefficient depending on shade / water table depth
            - The absorbance (extinction) of light with accumulated biomass is uniquely calculated for each environmental conditions determined by Shade and Water-table-depth.
            This seems logically as the extinction coefficient is modeling a optic denisty of the investigated (homogenous) medium. 
            In our case, this medium consists of moss plants. If we have different environmental conditions (i.e. Shade and Water-table-depth) the optic density could change as well. 
            So an extinction coefficient depending on the environmental conditions could be reasonable.
        '''
        extinction_coef = [0.0, 0.0]

        # Renaming variables for simplicity
        s = ext_shade # shade by vascular plants
        w = water_table_depth_in_cm

        # See description of table 6
        # Extinction coefficient remains constant for values of 
        # wtd outside of 3-15 cm
        # and shade of 0-0.8
        if w < 3.0:
            w = 3.0
        if w > 15.0:
            w = 15.0
        if s < 0.0:
            s = 0.0
        if s > 0.8:
            s = 0.8

        # calculating values by fitted function according to Table 6 on page 857
        extinction_coef[0] = 0.89 + 0.085 * w + (-1) * 0.73 * s + (-1) * 0.093 * w * s
        extinction_coef[1] = 0.71 + 0.022 * w + (-1) * 0.58 * s + (-1) * 0.027 * w * s

        # return
        return extinction_coef
    # DONE
    def self_shade(self, DL:float, ext_coefficient:float, log_absorbance_extS: float):
        '''
        DESCRIPTION:
        When a plant is below the surface of the average carpet height, we want to model the light availability by using Beers Law.
        When a plant is above the average height of the carpet we will use one as the return value to model fully available light. 
        The value is than fed into the growth function.
        NOTE: We calculate Beers Law ($I(d) = I_0 \cdot e^{-\mu \cdot d}$). But watch out! We already have negative values for $d$. 
        That is why we are basically doing ($I(d) = I_0 \cdot e^{\mu \cdot d}, \quad \text{ with } d \leq 0$).  
        If a plant is above the carpet we therefore obtain $I_0$ = extS as the light that is available at the surface of the moss carpet.
        
        PARAMETERS:
            - DL: (difference to the average height of the six surrounding plants (Individual height - average height). Six plants because the plants are arranged in rows with an offset of half a cells width.
                POSITIVE for heights ABOVE the average height of the surrounding plants.
                NEGATIVE for ...     BELOW ... .
            - ext_coefficient:  constant that is multiplied by the DL. Modulates the exponential relationship. Is obtained by another fitted function depending on shade and water-table-depth. This is described in detail in The ecology of Sphagnum (Hayward and Clymo, 1982)
            - extS: The value of external shade (e.g. by surrounding vascular plants) as a relative unit light NOT able to pass. 
                    For exampe extS = 0.46 means that 54% of the daylight passes to the surface of the carpet. 

        RETURN VALUES:
            - DL > 0 : 1 * extS, as we have no shade produced by other Sphagnum plants. So we are maintaining the incident radiation
            - DL <= 0: Beers Law is applied, we return $I_0 \cdot e^{\mu \cdot DL}$. NOTE: $DL \leq 0$

        NOTES/QUESTIONS:
        What do we take as a coefficent? -> The extinction coefficient is calculated by the fitted function depending on WTD and shade

        TODOS:
        - Make it two-dimensional (e.g. ext_coefficient is an two-dimensional array)
            

        ASSUMPTIONS:
        - Exponential decrease is applied 
        - accumulation of biomass is simplified by depth below DL (which again is an local average height) -> "local exposure"
        - Fitting the curve for calculation of the extinction coefficient is reasonable 
        - If the the plant is above mean average height there is no shade (which in reality could be the case, e.g. if there are three tall and three small individuals as neighbours)
        '''
        # if plant is above the average height there wont be any shade due to other Sphagnum plants, so we just return the external shade (logarithmic value of the ration Input/Output light) 
        if (DL > 0):
            if self.get_print_log():
                print(f'self_shade: We just returned the "normal" shade value {log_absorbance_extS}.')
            return log_absorbance_extS
        

        # if the individual is below the average height of the carpet, we use Beers Law
        else:
            # get the ratio of light out of the absorbance value extS (see Grace and Woolhouse, p. 65: WE HAVE AN E_BASIS!!!)
            incoming_radience_at_surface_level = 1.0 * np.exp(-log_absorbance_extS)

            # DL is negative here, as we are below the mean surface
            available_light_under_carpet_at_depth_DL = (incoming_radience_at_surface_level * np.exp(DL * ext_coefficient))

            # Absorbance is defined as the logarithm of the ratio of initial light flux intensity to the light at the measured depth
            # that is why, we have calculated, how much light is coming at the surface (already passed calluna vulgaris, therefore weakened)
            # the logarithm of the ratio here is given by the external_shade as a absorbance measure
            # to get the logarithmic value now of the ratio of the initial light (1.0) divided by the light intensity at level of the capitulum below the moss carpet,
            # we had to calculate the light flux at the moss carpet surface (=incoming_radience_at_surface_level) and calculate from it  the intensity at the capitulums (=available_light_under_carpet_at_depth_DL)
            # And then, we calculate the absorbance, so a logarithmic value, of the ratio initial light (before calluna vulgaris) to light at the capitulum
            # This is done in the following line and shall be our self_shade
            self_shade_logarithmic_absorbance = np.log(1.0 / available_light_under_carpet_at_depth_DL)

            # print
            if self.get_print_log():
                print(f'self_shade: We calculated the self shade value {self_shade_logarithmic_absorbance}.')
            return (self_shade_logarithmic_absorbance)
    # DONE    
    def calculate_DL(self, length:float, length_neighbourhood_mean:float):
        '''
        DESCRIPTION:
        Calculates difference between individula's length and the length of the neighbourhood (by default, the average length of the neighbor plants). 
        In the paper, we consider 6 neighbors. As we have rows with offset in the model, we get the mentioned six neighbors.
        
        PARAMETERS:
            - length: (float) Individuals height
            - length_neighbourhood_mean:  (float) The average of
            
        RETURN VALUES:
            - Difference of the parameters
        

        NOTES/QUESTIONS:
            - Mean is maybe fairly simple but improvable
        

        TODOS:
            - Implement mean-getting-function
            

        ASSUMPTIONS:
            - We only take six neighbours and calculate the mean length. This of course is an questionable assumption 
        
        '''
        return (length - length_neighbourhood_mean)

    def exposure_effect(self, DL:float, WTD:float, k:float):
        '''
        NOTE:
        - k could be really interesting for sensitivity analysis as it was not measured and is kind of a black-Box parameter.

        DESCRIPTION:
        Models the exposure of a single plant to being above the average carpet height. 
        This is an assumtption to "fill" a model gap in the system: 
        The experiment could not tell us, how the growth of an individual plant is affected (e.g. due to water availability) when the plant is higher than the "average Sphagnum carpet".
        This is also highlighted in FIG 4. by the dashed line.
        DL is negative when the plant's top lays below the average height 
        and is positive when the plant's top lays above.
        The constant k determines, how strong this influences the overall exposure to e.g. water availability.
        Not to be confused with the Self-Shade process where Beers Law is used to determine light availability.
        This process here is more a correction of growth as (potentially disadvantegeous) growing conditions above moss carpet were not further investigated.

        PARAMETERS:
            - DL: difference to the average height of the six surrounding plants (Individual height - average height). Six plants because the plants are arranged in rows with an offset of half a cells width.
                Positive for heights above the average height of the surrounding plants.
                Negative for ...     below ... .
            - WTD: water table depth measured in cm from tip of the plant to the water-table
            - k:  constant that is multiplied by the DL. Determines, how quickly the conditions worsen with the height above the sphagnum carpet. Usually negative. Not measured, experiments were taken.

        RETURN VALUES:
            - DL > 0 : Exponential value of parameters multiplied -> will be multilied with the growth functions results to model comparison
            - DL <= 0: 1

        NOTES/QUESTIONS:
        Is the rate k only specific for species? -> no, for elongation/ mass growth specific 
        Could we implement it more in a manner of "microtopographic types" instead of species? -> FURTHER IMPLEMENTATION

        TODOS:
            - implement DL
            - find out k values -> only one is given?! -> I will firstly try to use the same example given for both exposure effects (-1.39)
            - 

        ASSUMPTIONS:
        - Exponential decrease is applied to model exponentially decreasing quality of conditions when growing above average carpet height
        - accumulation of biomass is simplified by depth below DL (which again is an local average height) -> "local exposure"
        
        
        '''
        # for plants above the carpet, we model exponential exposure
        if (DL > 0):
            return np.exp(DL * k)
            
        # when plant is below carpet we only consider the growth functions result
        # This is why we return 1, as this value is multiplied to the grwoth functions result
        else:
            return float(1.0)

    def growth_mass(self, WTD: float, S:float):
        '''
        ## DESCRIPTION
        Returns fitted cubic function values NORMALIZED by duration of experiment.
        We calculate the growth in mass for the two sphagnum species [S. capillifolium, S. papillosum]. 
        This growth rate value originally is an absolute value for the growth after the whole experiment in mg/plant. 
        Fitted cubic functions were used to interpolate and the used coefficients can be found on p. 857 (14 internal) in Table 6.
        We later will normalize these obtained values by dividing them by the number of days the experiment was conducted.
        
        ## PARAMETERS
            - WTD: Water Table depth (measured from the top of a plant to the respective water table, in [cm])
            - S:   A unitless value representing the percentage of light that is absorbed. 
                Note that we fist have to determine the value of light flux above the sphagnum carpet. 
                This constant is determined by other (vascular) vegetation and general light conditions.

        ## RETURN VALUES
        Values refer to the cubic interpolation functions of the paper.
        returns two growth values [mg] in form of an array.The first entry corresponds to S. capillofolium, the second to papillosum. 

        NOTE:
        Note, that we still have to NORMALIZE these returned values as they just give us the absolute values measured at the end of the experiment.
        Note that we fist have to determine the value of light flux above the sphagnum carpet. 
        This constant is determined by other (vascular) vegetation and general light conditions.

        TODOS:
                - Check for Bounds
                - Implement edge behaviour
                - Data Type consistency

        ASSUMPTIONS:
        The cubic functions are thought to be fitting and representing the WTD- and S-growth relations measured.
        
        '''    
        # repsect bounds, if desired: Treating values outside as constant
        if self.get_treat_values_outside_polynomial_growth_as_constants():
            WTD, S = self.polynomial_respects_bounds_by_constant(WTD, S)

        # cubic equations [S. capillifolium, S. papillosum]
        growth_mass = [0.0,0.0]
        
        # growth for S. capillifolium
        growth_mass[0] = 1.7   + 0.72 * WTD +  5.5 * S + (-0.60) * WTD * S + (-0.028) * np.power(WTD, 2) + (-9.0) * np.power(S,2) + (-0.0003) * np.power(WTD, 3) +   3.9 * np.power(S,3)  + 0.031 * np.power(WTD, 2) * S + (-0.046) * WTD * np.power(S,2)

        # Normalize to get daily growth rate
        growth_mass[0] = growth_mass[0] / self.get_number_of_days_experiment_conducted()

        # growth for S. papillosum
        growth_mass[1] = 10.9  + 1.3 * WTD  + 3.5 * S  + (-3.6) * WTD * S  +  (0.027) * np.power(WTD, 2) +  (5.2) * np.power(S,2) + (-0.0069) * np.power(WTD, 3) + (-4.4) * np.power(S,3) + 0.13 * np.power(WTD, 2) * S  +   1.22  * WTD * np.power(S,2)
        
        # Normalize to get daily growth rate
        growth_mass[1] = growth_mass[1] / self.get_number_of_days_experiment_conducted()

        # cast for float numpy array
        growth_mass = np.array(growth_mass)
        growth_mass.astype(float)

        # cap negativ values if wanted
        if self.get_cap_zero():
            # cap it, if it is below zero
            growth_mass[0] = np.maximum(0.0, growth_mass[0])
            growth_mass[1] = np.maximum(0.0, growth_mass[1])
        
        # return array with first entry capillifolium, second entry papillosum
        return growth_mass

    # DONE    
    def growth_length(self, WTD:float, S:float):
            '''
            DESCRIPTION:
            We calculate the DAILY growth in length for the two sphagnum species [S. capillifolium, S. papillosum]. 
            It is a absolute value for the growth after the whole experiment in cm/plant. 
            Fitted cubic functions were used to interpolate and the used coefficients can be found on p. 857 (14 internal) in Table 6.
            We later will normalize these obtained values by dividing them by the number of days the experiment was conducted.
            
            PARAMETERS:
                - WTD: Water Table depth (measured from the top of a plant to the respective water table, in [cm])
                - S:   A unitless value representing the percentage of light that is absorbed. 
                    Note that we fist have to determine the value of light flux above the sphagnum carpet. 
                    This constant is determined by other (vascular) vegetation and general light conditions.

            RETURN VALUES:
            returns two growth values in form of an Numpy array.The first entry corresponds to S. capillofolium, the second to papillosum. 

            NOTES/QUESTIONS:
            Note, that we still have to NORMALIZE these returned values as they just give us the absolute values measured at the end of the experiment.
            Note that we fist have to determine the value of light flux above the sphagnum carpet. 
            This constant is determined by other (vascular) vegetation and general light conditions.

            TODOS:
                - Check for Bounds
                - Implement edge behaviour

            ASSUMPTIONS:
            The cubic functions are thought to be fitting and representing the WTD- and S-growth relations measured.
            
            '''
            # repsect bounds, if desired and we do not want to get approximated heights: Treating values outside as constant
            if self.get_treat_values_outside_polynomial_growth_as_constants() and not self.get_approximate_height_by_mass():
                WTD, S = self.polynomial_respects_bounds_by_constant(WTD, S)
            
            # cubic equations [S. capillifolium, S. papillosum]
            growth_length = [0.0,0.0]
            
            # growth for S. capillifolium
            growth_length[0] = 0.79 + 0.57 * WTD  +  5.1 * S  +   0.057 * WTD * S + (-0.082) * np.power(WTD, 2) + (-3.8) * np.power(S,2) + 0.003 * np.power(WTD, 3)   + 1.2 * np.power(S,3) + 0.018 * np.power(WTD, 2) * S + (-0.28) * WTD * np.power(S,2)

            # Normalize to get daily growth rate
            growth_length[0] = growth_length[0] / self.get_number_of_days_experiment_conducted()

            # growth for S. papillosum
            growth_length[1] = 1.5  + 0.097 * WTD + 10.6 * S  + (-0.77) * WTD * S + (-0.014) * np.power(WTD, 2) + (-7.2) * np.power(S,2) + 0.00026 * np.power(WTD, 3) + 0.3 * np.power(S,3) + 0.018 * np.power(WTD, 2) * S +   0.36  * WTD * np.power(S,2)
            
            # Normalize to get daily growth rate
            growth_length[1] = growth_length[1] / self.get_number_of_days_experiment_conducted()

            # cast for float numpy array
            growth_length = np.array(growth_length)
            growth_length.astype(float)

            # return array with first entry capillifolium, second entry papillosum
            return growth_length
        
        # Processes
        # Calculates length growth
        # Returns rate of elongation

    def approximate_height_growth_by_mass_outside_bounds(self, wtd, shade, upper_bound_wtd:float=14.0):
        '''
        The mass growth functions do make some sense for higher values.
        The height growth functions do not, as they go to infinity, when wtd values are high.
        This happens for wtd > 14 values
        '''
        # check for the upper_bound of wtd
        if wtd > upper_bound_wtd:
            # print(f'GPM.approximate_height_growth_by_mass_outside_bounds() wtd outside of bounds (wtd > {upper_bound_wtd}): ({wtd} > {upper_bound_wtd})')
            # wtd > 14, now get the value of height growth at the current conditions of shade and water_table depth of 14 cm (so the edge value in the polynomial)
            height_growth_wtd_bound = self.growth_length(WTD=upper_bound_wtd, S=shade)

            # mass value at the edge
            mass_growth_wtd_bound = self.growth_mass(WTD=upper_bound_wtd, S=shade)

            # get the mass value at the outbound conditions
            mass_growth_outside_bound = self.growth_mass(WTD=wtd, S=shade)

            # cap it, if it is below zero
            mass_growth_outside_bound[0] = np.maximum(0.0, mass_growth_outside_bound[0])
            mass_growth_outside_bound[1] = np.maximum(0.0, mass_growth_outside_bound[1])

            # THE FOLLOWING ONLY WORKS BECAUSE MASSES ARE DECLINING FOR WATER TABLE DEPTHS < 40cm
            ratio_mass_outbound_edge = mass_growth_outside_bound / mass_growth_wtd_bound

            # Now we assume that this ratio is also applying to the value of the growth rate in LENGTH outside the bounds for the values:
            # height_growth_outside_bound / height_growth_wtd_14 = mass_growth_outside_bound / mass_growth_wtd_14
            height_growth_outside_bound = height_growth_wtd_bound * ratio_mass_outbound_edge

            # return this array of approximated height values
            return height_growth_outside_bound
        
        # if we are inside water bounds
        else:
            # print(f'GPM.approximate_height_growth_by_mass_outside_bounds() wtd INSIDE of bounds (wtd =< {upper_bound_wtd}): ({wtd} =< {upper_bound_wtd})')

            # return normal height values
            return self.growth_length(wtd, S=shade)


    # Calculate Height growth
    # returns rate (ARRAY) of two growth heights for each species
    def elongation(self, species:str, WTD:float, extS:float, k_elong:float, length_plant:float, average_neighbor_length:float):
        '''
        ## DESCRIPTION
        One of the two GROWTH PROCESSES for a single individual Sphagnum model. The process is determined by a growth function (a fitted polynomial to experiment findings)
        and the light flux related exposure effect (a modulated exponential function, derived from Beer's Law and extended by individual rates as a x-stretch factor).

        ## PARAMETERS
        - species, string: species name ('capillifolium' or 'papillosum'). If capillifolium: return growth_rate_length[0], if papillosum: return growth_rate_length[1]
        - WTD, float: water-table depth in cm
        - S, float: external (!) shade, not the self shade value (will be calculated by get_ext_coefficient())
        - k_elong, float: a specific parameter determining the slope of the exponential function used to model the exposure effect for plants above the average carpet height
        - length_plant, float: the plants height in cm
        - average_neighbor_length, float: The average height of all six (or what neighborhood is defined) neighbors 
         
        Parameters only neccessary for 
            - growth_function
            - exposure effect
            - calculation of DL
            Further explanation can be found there

        ## RETURN-VALUE
        returns a 
            - growth_rate_length: (array, float), rate, in terms of a gowth in length for a time unit (e.g. day) divided by the duration of a timestep.   
              If capillifolium: return growth_rate_length[0], if papillosum: return growth_rate_length[1]
        ## NOTES/QUESTIONS
        The polynomial function of growth function and exposure effect are NOT time dependent. They only take in Water-Table-Depth (WTD, [cm]) and Shading ([%]) 
        and calculate the (absolute) growth during the whole experiments timespan. 
        As there is NO SPECIFIC PROCEDURE OF TEMPORAL NORMALIZATION (= how much does a plant grow in one day instead of observing the whole duration)
        I will Assume, that we can divide absolut growth by the number of days the experiment took place.
        

        ASSUMPTIONS:
        I will assume, that elongation rates can be obtained by dividing the results of the polynomial equations by the number of the days the experiment took place.
        C6 is only mentioned in the model description diagram, but nowhere else
        
        '''
        # FIXME: Delete this line, testing
        # print(f'elongation(): the external shade value S passed to the function: {extS}')

        # Calculate DL (the simple subtraction length-average_neighbor_length is not done here to be able to modify the procedure of calculation in the seperate method)
        DL = self.calculate_DL(length_plant, average_neighbor_length)

        # calculate exposure constant according to polynomial equations
        # needed to model growth above moss carpet
        exposure = float(self.exposure_effect(DL, WTD, k_elong))
        
        # Calculate extinction coefficient for Beers Law in self_shade()
        # Depends on species, too
        if species == 'capillifolium':
            ext_coef = self.get_extinction_coef(water_table_depth_in_cm=WTD, ext_shade= extS)[0]
        elif species == 'papillosum':
            ext_coef = self.get_extinction_coef(water_table_depth_in_cm=WTD, ext_shade= extS)[1]
        
    
        # 1. external shade and 
        # 2. self shade
        self_shade_value = self.self_shade(log_absorbance_extS = extS, DL = DL, ext_coefficient = ext_coef)
        
        # If globally is set, that we want to print...
        if self.get_print_log():
            print(f'elongation(): exposure = {exposure}')
            print(f'elongation(): ext_coef = {ext_coef}')
            print(f'elongation(): EXT SHADE = {extS}')
            print(f'elongation(): SELF SHADE = {self_shade_value}')

        # Get growth values from polynomial functions
        # FIXME: is self_shade_value the right value? Does it represent shade or light intensity? And can we just convert one to another?
        # SPECIES dependency
        if species == 'capillifolium':
            growth = self.growth_length(WTD, self_shade_value)[0]

            # overwrite if desired, when we are outside bounds for wtd, by the approximation of mass
            if self.get_approximate_height_by_mass():
                print(f'GPM.elongation(): We are in the length approximation! (Capillifolium)')
                growth = self.approximate_height_growth_by_mass_outside_bounds(wtd=WTD, shade=self_shade_value)[0]
        
        elif species == 'papillosum':

            growth = self.growth_length(WTD, self_shade_value)[1]
        
            # overwrite if desired, when we are outside bounds for wtd, by the approximation of mass
            if self.get_approximate_height_by_mass():

                # print(f'GPM.elongation(): We are in the length approximation! (Papillosum)')
                growth = self.approximate_height_growth_by_mass_outside_bounds(wtd=WTD, shade=self_shade_value)[1]
        
        # Save length_growth
        growth_rate_length = growth * exposure # NOTE: growth is an twodimensional array
        
        # NOTE: Two-dimensional numpy array is returned
        return growth_rate_length

    # Calculate Mass growth
    # returns rate (ARRAY) of two growth masses for each species
    def net_productivity(self, species:str, WTD:float, extS:float, k_prod:float, length_plant:float, average_neighbor_length:float):
        '''
        DESCRIPTION:
        One of the two GROWTH PROCESSES for a single individual Sphagnum model. The process is determined by a growth function (a fitted polynomial to experiment findings)
        and the light flux related exposure effect (a modulated exponential function, derived from Beer's Law and extended by individual rates as a x-stretch factor).

        PARAMETERS:
        Parameters only neccessary for 
            - self_shade
            - growth_function
            - exposure effect
            Further explanation can be found there. NOTE: We pass a value for the EXTERNAL shade, so this value has to be modulated according to Beers Law

        RETURN-VALUE:
        returns a 
            RATE (array, float) 
        in terms of a gowth in mass for a time unit (e.g. day) divided by the duration of a timestep for two species. 

        NOTES/QUESTIONS:
        The polynomial function of growth function and exposure effect are NOT time dependent. They only take in Water-Table-Depth (WTD, [cm]) and Shading ([%]) 
        and calculate the (absolute) growth during the whole experiments timespan. Note that we have in both growth processes cubic functions. Only the parameters vary according to
        growth in length or mass.
        As there is NO SPECIFIC PROCEDURE OF TEMPORAL NORMALIZATION (= how much does a plant grow in one day instead of observing the whole duration)
        I will Assume, that we can divide absolut growth by the number of days the experiment took place.

        ASSUMPTIONS:
        I will assume that elongation rates can be obtained by dividing the results of the polynomial equations by the number of the days the experiment took place.
        
        '''
        # Calculate DL (the simple subtraction length-average_neighbor_length is not done here to be able to modify the procedure of calculation in the seperate method)
        DL = self.calculate_DL(length_plant, average_neighbor_length)

        # Calculate extinction coefficient for Beers Law in self_shade()
        # Depends on species, too
        if species == 'capillifolium':
            ext_coef = self.get_extinction_coef(water_table_depth_in_cm=WTD, ext_shade= extS)[0]
        elif species == 'papillosum':
            ext_coef = self.get_extinction_coef(water_table_depth_in_cm=WTD, ext_shade= extS)[1]

        
        # TODO: Insert Self-shade to modulate external shade
        # Calculate the available light (expressed as absorbance of light) by considering 
        # 1. external shade and 
        # 2. self shade
        S = self.self_shade(log_absorbance_extS = extS, DL = DL, ext_coefficient = ext_coef)
        
        # Species dependent
        #  WTD = water-table-depth,   S = Shade (external and self)
        if species == 'capillifolium':
            growth = self.growth_mass(WTD, S)[0]
        elif species == 'papillosum':
            growth = self.growth_mass(WTD, S)[1]
        
        exposure = self.exposure_effect(DL, WTD, k_prod) # NOTE: one-dimensional at the moment
        
        if self.get_print_log():
            print(f'net_productivity(): ext_coef = {ext_coef}')
            print(f'net_productivity(): EXT SHADE = {extS}')
            print(f'net_productivity(): SELF SHADE = {S}')
            print(f'net_productivity(): exposure = {exposure}')

        # Save productivity rate
        net_prod_rate = growth * exposure

        # TODO: Return rate
        return net_prod_rate

    def grow_one_timestep(self, species:str, WTD:float, S:float, k_prod:float, k_elong:float, length_plant:float, average_neighbor_length:float, print_log=False):
        '''
        NOTE: 
        This method is called by the plants and calculates their actual growth for one timestep.
        Returns the additional growth in height (elongation_value) and mass (net_productivity_value) for one timestep.


        DESCRIPTION:
        Called by plant objects to calculate growth.
        This method calculates the growth in length (elongation_value) and in mass (net_productivity_value) normalized to a daily value.
        The values therefore can be added to the calling plant object attributes mass and height

        PARAMETERS:
        - species: String that determines, which polynomial equations for growth rates are used (either 'capillifolium' or 'papillosum')
        - WTD: Water-table depth of the plant (object) in cm
        - S: Shade value of the plant (object) as a value of absorbance
        - k_prod: parameter for the exposure effect for growth in mass NOTE: not really given, experimented with in the paper
        - k_elong: parameter for the exposure effect for growth in length NOTE: not really given, experimented with in the paper
        - length_plant: the height of the plant
        - average_neighbor_length: plant intern attribute, that usually describes the average height of the six surrounding plants

        - print: boolean, if True, the passed parameters are printed

        QUESTIONS:
        - 

        
        '''
        if print_log:
            # update global print_log
            self.set_print_log(True)
        elif print_log==False:
            # update to No printing
            self.set_print_log(False)

        # If desired, we can print the parameters
        if self.get_print_log():
            print("---------------------- LOG Growth processes model: grow_one_timestep ------------------------")
            print(f'Species: {species}')
            print(f'Water-Table-depth: {WTD}')
            print(f'Shade: {S}')
            print(f'k_elong: {k_elong}')
            print(f'k_prod: {k_prod}')
            print(f'length_plant: {length_plant}')
            print(f'Average_neighbor_length: {average_neighbor_length}')
            
        
        # Return growth values
        # Calculate the elongation (growth in LENGTH value)
        elongation_value = self.elongation(species, WTD, S, k_elong, length_plant, average_neighbor_length)
        
        if self.get_print_log():
            print(f'GROW_ONE_TIMESTEP() elongation_values: self.elongation(WTD, S, k_elong, length_plant, average_neighbor_length) = self.elongation({WTD}, {S}, {k_elong}, {length_plant}, {average_neighbor_length})= {elongation_value}')

        # Clacluate the amount of growth in MASS
        net_productivity_value = self.net_productivity(species, WTD, S, k_prod, length_plant, average_neighbor_length)
        if self.get_print_log():
            print(f'GROW_ONE_TIMESTEP() net_productivity_value = self.net_productivity(WTD, S, k_prod, length_plant, average_neighbor_length) = self.net_productivity({WTD}, {S}, {k_prod}, {length_plant}, {average_neighbor_length})={net_productivity_value}')
        
        # return
        return elongation_value, net_productivity_value