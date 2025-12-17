# import the Growth_processes_Model
from Growth_Processes_Model import Growth_Processes_Model
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import cm
from matplotlib import colors


### PLOTTING the original paper polynomial equations

def main():
    

    greens = cm.get_cmap('Greens')
    purples = cm.get_cmap('Purples')
    oranges = cm.get_cmap('Oranges')
    greys = cm.get_cmap('Greys')
    
    # keep only the darker 50% of the colormap
    dark_greens = greens(np.linspace(0.5, 1.0, 256))
    dark_greens = plt.matplotlib.colors.ListedColormap(dark_greens)

    light_greys  = greys((np.linspace(0.2, 0.7, 256)))
    light_greys = plt.matplotlib.colors.ListedColormap(light_greys)

    # keep only lighter 50 %
    dark_purples = purples(np.linspace(0.4, 1.0, 256))
    dark_purples = plt.matplotlib.colors.ListedColormap(dark_purples)

    # get a Growth_Processes_Model instance
    growth_model = Growth_Processes_Model()

    # do not cap the water table and shade values
    growth_model.set_treat_values_outside_polynomial_growth_as_constants(False)
    growth_model.set_approximate_height_by_mass(True)

    # Plotting of the polynomial equations
    plt.style.use('_mpl-gallery')

    # Make data
    # WTD   0.0 - 14.0
    # Shade 0.0 -  1.3
    WTD = np.arange(0, 40, 0.1)
    S = np.arange(0, 1.3, 0.1)
    length_growth_cap = np.zeros((len(S), len(WTD)))
    mass_growth_cap = np.zeros((len(S), len(WTD)))
    length_growth_pap = np.zeros((len(S), len(WTD)))
    mass_growth_pap = np.zeros((len(S), len(WTD)))

    WTD, S = np.meshgrid(WTD, S) # returns a tuple of (x_coordinates (as many times as len(S)), y_coordinates (as many as there are len(WTD))
    print(WTD)

    # Calculate the values
    for i,wtd in enumerate(WTD[0]):
        for j,s in enumerate(S[:,0]):
            
            # we plot the length growth for capillifollium (and omit papillosum) -> ...ngth(wtd, s)[0]
            length_growth_cap[j][i] = growth_model.approximate_height_growth_by_mass_outside_bounds(wtd=wtd, shade=s)[0]
            mass_growth_cap[j][i] = growth_model.growth_mass(WTD=wtd, S=s)[0]

            length_growth_pap[j][i] = growth_model.approximate_height_growth_by_mass_outside_bounds(wtd=wtd, shade=s)[1]
            mass_growth_pap[j][i] = growth_model.growth_mass(WTD=wtd, S=s)[1]
            # print(Z[j][i])

    
    elev = 30
    azim = -30
    roll = 00


    # Create figure
    fig = plt.figure(figsize=(14, 10))
    gs = fig.add_gridspec(2, 2, hspace=0.35, wspace=0.1)  # spacing between subplots

    # fontsize ax labels
    fontsize = 13
    fontsize_numbers = 11
    # Create 4 subplots (3D)
    ax00 = fig.add_subplot(gs[0,0], projection='3d')
    ax01 = fig.add_subplot(gs[0,1], projection='3d')
    ax10 = fig.add_subplot(gs[1,0], projection='3d')
    ax11 = fig.add_subplot(gs[1,1], projection='3d')

    # --- TOP ROW: S. capillifolium ---
    ax00.plot_surface(S, WTD, length_growth_cap, cmap=dark_purples)
    ax00.set_proj_type("ortho")
    ax00.invert_yaxis()
    ax00.view_init(elev, azim, roll)
    ax00.set_xlabel("Absorbance", fontsize = fontsize)
    ax00.set_ylabel("Water Table depth [cm]", fontsize = fontsize)
    ax00.set_zlabel('Growth [cm / d]', fontsize = fontsize)
    ax00.tick_params(axis='both', which='major', labelsize=fontsize_numbers) 
    ax00.set_title("", color=(0.29, 0.0, 0.51), fontstyle="oblique", fontsize=14)

    ax01.plot_surface(S, WTD, mass_growth_cap, cmap=dark_greens)
    ax01.set_proj_type("ortho")
    ax01.invert_yaxis()
    ax01.view_init(elev, azim, roll)
    ax01.set_xlabel("Absorbance", fontsize = fontsize)
    ax01.set_ylabel("Water Table depth [cm]", fontsize = fontsize)
    ax01.set_zlabel('Growth [mg / d]', fontsize = fontsize)
    ax01.tick_params(axis='both', which='major', labelsize=fontsize_numbers) 
    ax01.set_title("", color="darkgreen", fontstyle="oblique", fontsize=14)

    # --- BOTTOM ROW: S. papillosum ---
    ax10.plot_surface(S, WTD, length_growth_pap, cmap=dark_purples)
    ax10.set_proj_type("ortho")
    ax10.invert_yaxis()
    ax10.view_init(elev, azim, roll)
    ax10.set_xlabel("Absorbance", fontsize = fontsize)
    ax10.set_ylabel("Water Table depth [cm]", fontsize = fontsize)
    ax10.set_zlabel('Growth [cm / d]', fontsize = fontsize)
    ax10.tick_params(axis='both', which='major', labelsize=fontsize_numbers) 
    ax10.set_title("Height", color=(0.29, 0.0, 0.51), fontstyle="oblique", fontsize=17)

    ax11.plot_surface(S, WTD, mass_growth_pap, cmap=dark_greens)
    ax11.set_proj_type("ortho")
    ax11.invert_yaxis()
    ax11.view_init(elev, azim, roll)
    ax11.set_xlabel("Absorbance", fontsize = fontsize)
    ax11.set_ylabel("Water Table depth [cm]", fontsize = fontsize)
    ax11.set_zlabel('Growth [mg / d]', fontsize = fontsize)
    ax11.tick_params(axis='both', which='major', labelsize=fontsize_numbers) 
    ax11.set_title("Mass", color="darkgreen", fontstyle="oblique", fontsize=17)

    # --- Super labels for species ---
    fig.text(0.5, 0.95, "S. capillifolium", ha="center", va="bottom", fontsize=20, fontstyle="italic")
    fig.text(0.5, 0.48, "S. papillosum", ha="center", va="bottom", fontsize=20, fontstyle="italic")
    plt.savefig("/home/louis-dee/GitHub/Moss_growth/.venv_Model_Sphag/HaywardAndClymo1983/Thesis_Tex_files/Plots/Replication/polynomials_appr_by_mass.pdf")
    
    plt.show()




    
# 
if __name__ == '__main__':
    main()