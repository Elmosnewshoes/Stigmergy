from core.domain import Domain
from core.plugins.helper_classes import point
import numpy as np

domain_dict = {'size': [1000,500],
               'pitch': 1,
               'nest':{'location': [250,250],'radius':50},
               'food':{'location': [750,250],'radius':50}}
def run():
    D = Domain(**domain_dict)
    D.Gaussian = D.init_gaussian(sigma=15)
    print('Class Map:', D.Map)
    print('Gaussian property peak:',D.Gaussian.peak)
    print('Entropy of Gaussian:',D.Gaussian.entropy())
    print('Map class of type Gaussian:',D.Gaussian)
    print('Total pheromone volume fresh map: ',D.Map.map.sum())
    xy = point(100,100)
    D.local_add_pheromone(target_pos=xy,Q= 2)
    print(f'Pheromone concentration at {xy}:',D.probe_pheromone(xy))
    assert D.probe_pheromone(xy) == D.Map.map.max()#check if all works correctly
    print('Total pheromone volume (Map.map.sum())',D.Map.map.sum())
    D.evaporate(0.9)
    print(D.Map.map.max())
    D.set_target_pheromone(10)
    D.evaporate()
    print(D.Map.map.max())
    print(D.Map.map.sum())
    xy = point(250,500)
    print(D.food_location.vec)
    print("Point {} is in range of food? {}".format(xy,D.inrange(xy,'food')))
    D.local_add_pheromone(point(301.13,359.72),1)


def time_domain():
    " time the domain methods "
    from time import time
    D=Domain(**domain_dict)
    D.Gaussian = D.init_gaussian(sigma=10,significancy=1e2)
    D.set_target_pheromone(D.Map.map.sum())
    n = int(1e3)

    tic = time()
    points = [point(*p) for p in np.random.rand(n,2)*domain_dict['size']]
    for p in points:
        D.local_add_pheromone(target_pos = p, Q=1)
    toc=time()
    print("Added pheromone in {} msec".format(1e3*(toc-tic)/n))

    tic = time()
    for _ in range(n):
        D.evaporate()
    toc = time()
    print("Evaporated in {} msec".format(1e3*(toc-tic)/n))

    tic = time()
    H = 0
    n_min = int(n/10)
    for _ in range(n_min):
        H+= D.Map.entropy()
    toc = time()
    print("Got entropy in {} msec".format(1e3*(toc-tic)/n_min))

    tic = time()
    for p in points:
        Q = D.probe_pheromone(p)
    toc = time()
    print("Probed in {} msec".format(1e3*(toc-tic)/n))

    tic = time()
    for p in points:
        truth = D.inrange(p)
    toc = time()
    print("Checked point in {} msec".format(1e3*(toc-tic)/n))


if __name__ == '__main__':
    run()
    time_domain()
