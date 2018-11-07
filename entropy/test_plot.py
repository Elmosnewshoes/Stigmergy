from core.visualization import StigmergyPlot

def run_plot():
    from core.domain import Domain
    from core.ant import Ant, lin_fun
    domain_dict = {'size': [1000,1000],
                   'pitch': 2,
                   'nest':{'location': [250,500],'radius':50},
                   'food':{'location': [750,500],'radius':50}}
    n = 500
    D = Domain(**domain_dict)
    D.Gaussian = D.init_gaussian(sigma=5,significancy =1e2)
    P = StigmergyPlot(Map=D.Map, n=n,pitch=D.pitch)


    ant_settings = {'start_pos': [500,100],
                    'angle': 45,
                    'speed': 20,
                    'limits': [1000,1000],
                    'l': 10,
                    'antenna_offset': 30,
                    'drop_quantity':1}
    A = Ant(**ant_settings)
    for i in range(n+1):

        ant_loc = A.pos
        left = A.sensors['left']
        right = A.sensors['right']
        D.local_add_pheromone(ant_loc,1e6)

        P.draw_scatter(ant_loc.x,ant_loc.y)
        P.draw_scatter(left.x,left.y, name='left')
        P.draw_scatter(right.x,right.y, name ='right')
        if i%10 == 0:
            P.draw_stigmergy(D.Map.map)
            P.draw()
        Q = [D.probe_pheromone(A.sensors['left']),
             D.probe_pheromone(A.sensors['right'])]
        A.observe_pheromone(lin_fun,Q)
        A.step(dt=1)

    P.hold_until_close()


if __name__=='__main__':
    run_plot()
