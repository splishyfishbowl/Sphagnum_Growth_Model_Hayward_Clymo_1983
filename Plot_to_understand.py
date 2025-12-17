# import the Growth_processes_Model
from Growth_Processes_Model import Growth_Processes_Model
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import cm



def main():
    print('Hello World from Plot_to_understand.py')

    # get a Growth_Processes_Model instance
    growth_model = Growth_Processes_Model()

    # Plotting of the polynomial equations
    plt.style.use('_mpl-gallery')

    # Make data
    WTD = np.arange(0, 14, 0.25)
    S = np.arange(0, 1.0, 0.1)
    cap = np.zeros((len(S), len(WTD)))
    pap = np.zeros((len(S), len(WTD)))

    WTD, S = np.meshgrid(WTD, S) # returns a tuple of (x_coordinates (as many times as len(S)), y_coordinates (as many as there are len(WTD))

    # Calculate the values
    for i,wtd in enumerate(WTD[0]):
        for j,s in enumerate(S[:,0]):
            
            # we plot the length growth for capillifollium (and omit papillosum) -> ...ngth(wtd, s)[0]
            cap[j][i], pap[j][i] = growth_model.get_extinction_coef(water_table_depth_in_cm=wtd, ext_shade=s)

    elev = 30
    azim = -30
    roll = 00

    # Plot the surface
    fig, ax = plt.subplots(subplot_kw={"projection": "3d"})
    # ax.plot_surface(Y, X, Zplane, cmap=cm.Greens)
    ax.plot_surface(S, WTD, cap, cmap=cm.Blues)
    ax.set_proj_type("ortho")
    # ax.invert_yaxis()
    ax.invert_xaxis()
    ax.view_init(elev, azim, roll)
    ax.set(title = "Growth in Length of $ \t{S. capillifolium}$", ylabel = "Water Table depth[cm]", xlabel = "Absorbance")
    # plt.savefig("/home/louis-dee/Desktop/Uni/Moorprojekt/Zwischenstand 04-04/Plot_growth_length", dpi = 300)
    fig2, ax2 = plt.subplots(subplot_kw={"projection": "3d"})
    ax2.plot_surface(S, WTD, pap, label=f'ext_pap for wtd={wtd}, shade={s}')
    ax2.legend()
    ax2.view_init(elev, azim, roll)
    ax2.invert_xaxis()
    plt.tight_layout()
    plt.show()
# 
if __name__ == '__main__':
    main()