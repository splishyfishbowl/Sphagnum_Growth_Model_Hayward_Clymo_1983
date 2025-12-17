# import the Growth_processes_Model
from Growth_Processes_Model import Growth_Processes_Model
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import cm
from matplotlib import colors



def main():
    print('Hello World from Plot_growth_length.py')

    greens = cm.get_cmap('Greens')
    purples = cm.get_cmap('Purples')
    
    # keep only the darker 50% of the colormap
    dark_greens = greens(np.linspace(0.5, 1.0, 256))
    dark_greens = plt.matplotlib.colors.ListedColormap(dark_greens)

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
    WTD = np.arange(0, 40, 0.25)
    S = np.arange(0, 1.3, 0.1)
    Z = np.zeros((len(S), len(WTD)))
    mass_growth = np.zeros((len(S), len(WTD)))
    length_growth_pap = np.zeros((len(S), len(WTD)))
    mass_growth_pap = np.zeros((len(S), len(WTD)))

    WTD, S = np.meshgrid(WTD, S) # returns a tuple of (x_coordinates (as many times as len(S)), y_coordinates (as many as there are len(WTD))
    print(WTD)

    # Calculate the values
    for i,wtd in enumerate(WTD[0]):
        for j,s in enumerate(S[:,0]):
            
            # we plot the length growth for capillifollium (and omit papillosum) -> ...ngth(wtd, s)[0]
            Z[j][i] = growth_model.approximate_height_growth_by_mass_outside_bounds(wtd=wtd, shade=s)[0]
            mass_growth[j][i] = growth_model.growth_mass(WTD=wtd, S=s)[0]

            length_growth_pap[j][i] = growth_model.approximate_height_growth_by_mass_outside_bounds(wtd=wtd, shade=s)[1]
            mass_growth_pap[j][i] = growth_model.growth_mass(WTD=wtd, S=s)[1]
            # print(Z[j][i])

    
    elev = 30
    azim = -30
    roll = 00

    # Plot length########################################

    # Plot the surface for wtd up to 20 cm
    fig, ax = plt.subplots(nrows=2,ncols=2, figsize = (10, 10), subplot_kw={"projection": "3d"})
    # ax.plot_surface(Y, X, Zplane, cmap=cm.Greens)
    ax[0][0].plot_surface(S, WTD, Z, cmap=light_greens)
    ax[0][0].set_proj_type("ortho")
    ax[0][0].invert_yaxis()
    # ax.invert_xaxis()
    ax[0][0].view_init(elev, azim, roll)
    ax[0][0].set(title = "Growth in Length of $ \t{S. capillifolium}$", ylabel = "Water Table depth[cm]", xlabel = "Absorbance")
    # plt.savefig("/home/louis-dee/Desktop/Uni/Moorprojekt/Zwischenstand 04-04/Plot_growth_length", dpi = 300)
    
    # Plot the surface for wtd up to 15
    # fig2, ax2 = plt.subplots(subplot_kw={"projection": "3d"})
    # ax.plot_surface(Y, X, Zplane, cmap=cm.Greens)
    print(Z.shape)
    print(WTD.shape)
    ax[0][1].plot_surface(S[:,0:60], WTD[:, 0:60], Z[:,0:60], cmap=light_greens)
    ax[0][1].set_proj_type("ortho")
    ax[0][1].invert_yaxis()
    # ax2.invert_xaxis()
    ax[0][1].view_init(elev, azim, roll)
    ax[0][1].set(title = "Growth in Length of $ \t{S. capillifolium}$", ylabel = "Water Table depth[cm]", xlabel = "Absorbance")
    # plt.savefig("/home/louis-dee/Desktop/Uni/Moorprojekt/Zwischenstand 04-04/Plot_growth_length", dpi = 300)
    

    # Plot mass ###############################################################################

     # Plot the surface for wtd up to 20 cm
    # fig, ax = plt.subplots(subplot_kw={"projection": "3d"})
    # ax.plot_surface(Y, X, Zplane, cmap=cm.Greens)
    ax[1][0].plot_surface(S, WTD, mass_growth, cmap=dark_greens)
    ax[1][0].set_proj_type("ortho")
    ax[1][0].invert_yaxis()
    # ax.invert_xaxis()
    ax[1][0].view_init(elev, azim, roll)
    ax[1][0].set(title = "Growth in Mass of $ \t{S. capillifolium}$", ylabel = "Water Table depth[cm]", xlabel = "Absorbance")

    # Plot the surface for wtd up to 15
    # fig2, ax2 = plt.subplots(subplot_kw={"projection": "3d"})
    # ax.plot_surface(Y, X, Zplane, cmap=cm.Greens)
    ax[1][1].plot_surface(S[:,0:60], WTD[:, 0:60], mass_growth[:,0:60], cmap=dark_greens)
    ax[1][1].set_proj_type("ortho")
    ax[1][1].invert_yaxis()
    # ax2.invert_xaxis()
    ax[1][1].view_init(elev, azim, roll)
    ax[1][1].set(title = "Growth in Mass of $ \t{S. capillifolium}$", ylabel = "Water Table depth[cm]", xlabel = "Absorbance")
    # plt.savefig("/home/louis-dee/Desktop/Uni/Moorprojekt/Zwischenstand 04-04/Plot_growth_length", dpi = 300)
    fig.set_layout_engine(layout='tight')
    

    ##### PAPILLOSUM ################################################################################
    # Plot length########################################

    # Plot the surface for wtd up to 20 cm
    fig2, ax2 = plt.subplots(nrows=2,ncols=2, figsize = (10, 10), subplot_kw={"projection": "3d"})
    # ax.plot_surface(Y, X, Zplane, cmap=cm.Greens)
    ax2[0][0].plot_surface(S, WTD, length_growth_pap, cmap=light_greens)
    ax2[0][0].set_proj_type("ortho")
    ax2[0][0].invert_yaxis()
    # ax.invert_xaxis()
    ax2[0][0].view_init(elev, azim, roll)
    ax2[0][0].set(title = "Growth in Length of $ \t{S. papillosum}$", ylabel = "Water Table depth[cm]", xlabel = "Absorbance")
    # plt.savefig("/home/louis-dee/Desktop/Uni/Moorprojekt/Zwischenstand 04-04/Plot_growth_length", dpi = 300)
    
    # Plot the surface for wtd up to 15
    # fig2, ax2 = plt.subplots(subplot_kw={"projection": "3d"})
    # ax.plot_surface(Y, X, Zplane, cmap=cm.Greens)
    print(Z.shape)
    print(WTD.shape)
    ax2[0][1].plot_surface(S[:,0:60], WTD[:, 0:60], length_growth_pap[:,0:60], cmap=light_greens)
    ax2[0][1].set_proj_type("ortho")
    ax2[0][1].invert_yaxis()
    # ax2.invert_xaxis()
    ax2[0][1].view_init(elev, azim, roll)
    ax2[0][1].set(title = "Growth in Length of $ \t{S. papillosum}$", ylabel = "Water Table depth[cm]", xlabel = "Absorbance")
    # plt.savefig("/home/louis-dee/Desktop/Uni/Moorprojekt/Zwischenstand 04-04/Plot_growth_length", dpi = 300)
    

    # Plot mass ###############################################################################

     # Plot the surface for wtd up to 20 cm
    # fig, ax = plt.subplots(subplot_kw={"projection": "3d"})
    # ax.plot_surface(Y, X, Zplane, cmap=cm.Greens)
    ax2[1][0].plot_surface(S, WTD, mass_growth_pap, cmap=dark_greens)
    ax2[1][0].set_proj_type("ortho")
    ax2[1][0].invert_yaxis()
    # ax.invert_xaxis()
    ax2[1][0].view_init(elev, azim, roll)
    ax2[1][0].set(title = "Growth in Mass of $ \t{S. papillosum}$", ylabel = "Water Table depth[cm]", xlabel = "Absorbance")

    # Plot the surface for wtd up to 15
    # fig2, ax2 = plt.subplots(subplot_kw={"projection": "3d"})
    # ax.plot_surface(Y, X, Zplane, cmap=cm.Greens)
    ax2[1][1].plot_surface(S[:,0:60], WTD[:, 0:60], mass_growth_pap[:,0:60], cmap=dark_greens)
    ax2[1][1].set_proj_type("ortho")
    ax2[1][1].invert_yaxis()
    # ax2.invert_xaxis()
    ax2[1][1].view_init(elev, azim, roll)
    ax2[1][1].set(title = "Growth in Mass of $ \t{S. capillifolium}$", ylabel = "Water Table depth[cm]", xlabel = "Absorbance")
    # plt.savefig("/home/louis-dee/Desktop/Uni/Moorprojekt/Zwischenstand 04-04/Plot_growth_length", dpi = 300)
    fig2.set_layout_engine(layout='tight')

    plt.show()



    
# 
if __name__ == '__main__':
    main()