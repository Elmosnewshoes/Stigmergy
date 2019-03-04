""" ==========
    Written by: Bram Durieux,
    Delft University of Technology, Delft, The Netherlands
    ========== """

import numpy as np
import small_functions as fun
import matplotlib.pyplot as plt
from matplotlib import cm, gridspec
import matplotlib.colors as colors
from map import MeshMap
import time
from mpl_toolkits.mplot3d import axes3d, Axes3D #<-- Note the capitalization!

from domain import AntDomain
from ant import Ant


def plot_surf(X,Y,Z):
    tic = time.time()
    fig = plt.figure()
    print("init fig in {:.4f} seconds".format(time.time()-tic))
    tic = time.time()
    # ax = Axes3D(fig)
    ax = fig.gca()
    print("Set axis in {:.4f}".format(time.time()-tic))
    Z= np.add(Z,0.01)
    tic = time.time()
    the_plot = ax.pcolormesh(X,Y,Z, norm=colors.LogNorm(vmin=Z.min(), vmax=Z.max()), cmap='PuBu')
    # the_plot = ax.plot_surface(X,Y,Z, norm=colors.LogNorm(vmin=Z.min(), vmax=Z.max()), cmap='PuBu')
    print("Make the contour in {:.4f}".format(time.time()-tic))
    ax.set_title('pcolor plot')
    tic = time.time()
    fig.colorbar(the_plot, ax = ax)
    print("Colorbar in {:.4f}".format(time.time()-tic))
    tic = time.time()
    plt.show()
    print("Render the plot in {:.4f}".format(time.time()-tic))
    x= np.random.rand(1000,1000)
    print(x.nbytes)

def run():
    D = AntDomain(size=[1000,1000], pitch = 2)
    D.set_gaussian(sigma = 25)
    print(D.Gaussian.map.shape)
    print(D.Gaussian.map.sum())
    D.local_add_pheromone([150,150])
    plot_surf(D.Map.X,D.Map.Y,D.temp_map)

    X = np.identity(10)
    print(X)
    X[1,0:2] = [1,1]
    print(X)

def test_ant_speed(n = 50):
    timing = {'get_pheromone':0,
              'observed_pheromone':0,
              'gradient_step':0,
              'update_sensors':0,
              'sim_checks':0,
              'add_pheromone':0,
              'update_map':0,
              'evaporate':0,
              'ttl':0}
    out_of_bounds = False
    limits = [1000,1000]
    ant = Ant(limits = limits, start_pos = np.dot(0.5,limits), speed=10)
    dom = AntDomain(size = limits, pitch = 1, food = {'location': [850,500],'radius':50},
        nest = {'location': [150,500],'radius':50})
    dom.set_gaussian(sigma = 10, significancy =1e2)
    print(dom.Gaussian.map.shape)

    # == Prime the map ==
    for i in range(50):
        loc = np.array(limits)*np.random.rand(1,2)[0]
        dom.add_pheromone(Q =0.125,sigma = 50,loc=loc,peak_1=True)
    dom.update_pheromone()


    for i in range(n):
        # == Get the pheromone from the map ==
        t1 = time.time()
        p = dom.get_pheromone_level(ant.sens_loc,islist=True)
        timing['get_pheromone']+=(time.time()-t1)*1000

        # == Get perceived pheromone ==
        t2 = time.time()
        obs_pher = ant.observed_pheromone(p)
        timing['observed_pheromone']+=(time.time()-t2)*1000

        # == Perform the steps ==
        t3 = time.time()
        ant.gradient_step(obs_pher,gain = 0.005, SNR = 0.05)
        timing['gradient_step']+=(time.time()-t3)*1000

        # == simulation intelligence ==
        # == Some simulation specific intelligence ==
        t4 = time.time()
        if ant.foodbound and dom.inrange(ant.pos.vec,'food'):
            ant.foodbound = False
            ant.reverse()
            print("Found food, looking for nest")
        elif not(ant.foodbound) and dom.inrange(ant.pos.vec, 'nest'):
            ant.foodbound = True
            ant.reverse()
            print("Found nest, looking for food")
        timing['sim_checks']+=(time.time()-t4)*1000

        # == addint the pheromone to the map ==
        t5 = time.time()
        if not ant.out_of_bounds:
            dom.local_add_pheromone(ant.pos.vec, peak_1 = True, Q = 0.05) # add pheromone to the map
        timing['add_pheromone']+=(time.time()-t5)*1000

        # == Updating import matplotlib.pyplot as pltthe map ==
        t6 = time.time()
        dom.update_pheromone()
        timing['update_map']+=(time.time()-t6)*1000

        # == evaporate ==
        t7 = time.time()
        dom.evaporate(xsi = 0.995)
        timing['evaporate']+=(time.time()-t7)*1000

    for key, value in timing.items():
        timing[key] = value/n

    timing['ttl']=timing['get_pheromone'] + timing['observed_pheromone'] + timing['gradient_step']  + timing['sim_checks']  + timing['add_pheromone']

    print("""
          Map: get pheromone -> {get_pheromone:.4f} msec
          Ant: observe pheromone -> {observed_pheromone:.4f} msec
          Ant: gradient_step -> {gradient_step:.4f} msec
          Ant: sim checks -> {sim_checks:4f} msec
          Map/Ant: add pheromone -> {add_pheromone:.4f} msec
          Map: update map -> {update_map:.4f} msec
          Map: evaporate -> {evaporate:.4f} msec
          Total Ant time ==>> {ttl:.4f} msec
          """.format(**timing))

def test_size():
    X = np.random.rand(1000,1000)
    print(X[X>1e-3].size)

def make_pheromone_plot_sim(n = 1000):
    # sim stuff
    limits = [1000,1000]
    out_of_bounds = False
    ant = Ant(limits = limits, start_pos = np.dot(0.5,limits), speed=10)
    dom = AntDomain(size = limits, pitch = 1, food = {'location': [850,500],'radius':50},
        nest = {'location': [150,500],'radius':50})
    dom.set_gaussian(sigma = 10, significancy =1e2)


    # == Prime the map ==
    for i in range(50):
        loc = np.array(limits)*np.random.rand(1,2)[0]
        dom.add_pheromone(Q =0.125,sigma = 50,loc=loc,peak_1=True)
    dom.update_pheromone()
    dom.set_total_pheromone(volume =1e5)

    # plot stuff
    x = np.arange(n).reshape(n,1)
    y = np.zeros((n,1))
    plt.ion()
    # fig, (ax_imshow, ax_points) = plt.subplots(1,2)
    fig = plt.figure(figsize = (8,6))

    gs = gridspec.GridSpec(1, 2, width_ratios=[3, 1])
    ax_imshow = plt.subplot(gs[0])
    ax_points = plt.subplot(gs[1])

    fig.suptitle('Title of figure', fontsize=20)

    # ax_points.title.set_text('Entropy')
    ax_points.plot([0],[0], 'ro')
    ax_points.set_xlim(0,n)


    # ax_imshow.title.set_text('Pheromone map')
    ax_imshow.imshow(np.zeros(dom.Map.map.shape),cmap ='PuBu')

    plt.tight_layout()


    for i in range(n):
        p = dom.get_pheromone_level(ant.sens_loc,islist=True)
        obs_pher = ant.observed_pheromone(p)
        ant.gradient_step(obs_pher,gain = 0.005, SNR = 0.05)
        if ant.foodbound and dom.inrange(ant.pos.vec,'food'):
            ant.foodbound = False
            ant.reverse()
            print("Found food, looking for nest")
        elif not(ant.foodbound) and dom.inrange(ant.pos.vec, 'nest'):
            ant.foodbound = True
            ant.reverse()
            print("Found nest, looking for food")

        if not ant.out_of_bounds:
            dom.local_add_pheromone(ant.pos.vec, peak_1 = True, Q = 0.125) # add pheromone to the map

        dom.update_pheromone()
        dom.evaporate() #maintain constant total pheromone
        sum = round(dom.Map.map.sum(),2)
        entropy = dom.Map.entropy
        print(f"Total pheromone volume = {sum} with entropy: {entropy}")
        y[i] = entropy
        ax_points.clear()
        ax_points.plot(x[y!=0],y[y!=0], linestyle=':', color='cornflowerblue', markersize=3, marker = '8')
        ax_points.set_ylim(0,max(y)*1.05)

        ax_imshow.clear()
        ax_imshow.imshow(dom.Map.map,cmap = 'PuBu')

        # ax_points.figure.canvas.draw()
        # ax_imshow.figure.canvas.draw()
        fig.canvas.draw()

    plt.show(block=True)


if __name__ =='__main__':
    # run()
    # test_ant_speed(n=5000)
    # test_size()
    # make_pheromone_plot_sim(n = 100)
    D = AntDomain([1000,1000])
    D.set_total_pheromone(1e9)
    D.Map.init_map('random')
    D.evaporate()
    str = "Entropy of the map = {entropy}"
    print(str.format(entropy = D.Map.entropy))
    D.Map.init_map('identity')
    D.evaporate()
    print(str.format(entropy = D.Map.entropy))
