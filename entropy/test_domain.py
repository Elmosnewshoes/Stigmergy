from core.domain import Domain
from core.plugins.helper_classes import point

def run():
    domain_dict = {'size': [1000,500],
                   'pitch': 1,
                   'nest':{'location': [250,250],'radius':50},
                   'food':{'location': [750,250],'radius':50}}
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

if __name__ == '__main__':
    run()
