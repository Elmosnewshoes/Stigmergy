from core.visualization import StigmergyPlot

def run_plot(beta = 1e-3, gain = 1, n=500,dt =.5):
    from core.domain import Domain
    from core.ant import Ant, lin_fun
    domain_dict = {'size': [1000,1000],
                   'pitch':.5}
    D = Domain(**domain_dict)
    D.Gaussian = D.init_gaussian(sigma=5,significancy =1e2)
    P = StigmergyPlot(Map=D.Map,)


    ant_settings = {'start_pos': [250,250],'angle': 45,'speed':15,'limits': [1000,1000],'l': 50,
            'antenna_offset': 30,'drop_quantity':1,'noise_gain':1,'gain':gain,'beta':beta,'drop_fun':'linear'}
    ant = Ant(**ant_settings)
    D.Gaussian = D.init_gaussian(sigma=5,significancy =1e2)
    P = StigmergyPlot(Map=D.Map, shown='stigmergy')
    ant = Ant(**ant_settings)
    for i in range(n+1):

        ant_loc = ant.pos
        left,right = [ant.sensors['left'], ant.sensors['right']]
        D.local_add_pheromone(ant_loc,1e6)

        P.draw_scatter(ant_loc.x,ant_loc.y, marker = 'o')
        P.draw_scatter(left.x,left.y, name='left',marker = '.')
        P.draw_scatter(right.x,right.y, name ='right',marker='.')
        P.draw_stigmergy(D.Map.map)
        P.draw()
        ant.observe_pheromone(lin_fun,[0,0])
        ant.gradient_step(dt=dt)

    P.hold_until_close()


if __name__=='__main__':
    run_plot()
