from Growth_Processes_Model import Growth_Processes_Model
import numpy as np
import matplotlib.pyplot as plt

def main():
    processes = Growth_Processes_Model()
    mean = 0.0
    std = 0.5
    length = 6

    six_neighbor_values = np.random.normal(mean, std, length)
    average_neighbor = np.average(six_neighbor_values)

    print(f'Random values for neighbors: {six_neighbor_values}')

    # capillifolium 
    mass = 0.0
    height = np.random.normal(mean, std) # start with random height
    print(f'mass: {mass}')
    print(f'height: {height}')

    # water table
    wth= -3.0
    external_shade = 0.0

    wtd = height - wth
    print(f'wtd: {wtd}')

    ext_coefficient = processes.get_extinction_coef(wtd, ext_shade=external_shade)[0]
    print(f'extinction coefficient: {ext_coefficient}')

    DL = height - average_neighbor
    print(f'DL: {DL}')

    exposure = processes.exposure_effect(DL, wtd, -1.39)
    print(f'exposure: {exposure}')

    self_shade = processes.self_shade(DL=DL, ext_coefficient=ext_coefficient, extS=external_shade)
    print(f'external_shade: {external_shade}')
    print(f'self_shade: {self_shade}')

    DLs = np.linspace(-5.0, 0.0, 100)
    self_shades = np.zeros(len(DLs))

    for i, dl in enumerate(DLs):
        self_shades[i] = processes.self_shade(DL=dl, ext_coefficient=ext_coefficient, extS=external_shade)
          
    #plot
    plt.plot(DLs, self_shades, label='self_shade value')
    plt.xlabel('DL')
    plt.ylabel('shade (as absorbance)')
    plt.show()

# 
if __name__ == '__main__':
    main()