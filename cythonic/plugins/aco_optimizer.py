import numpy as np
def dummy_fun(x,y, z):
    return 2.*x**2 -2.*x*y -3*y+2*y**2+2*z**2 +1.5

class opt:
    def __init__(self,opts,name,k,beta):
        self.name = name
        self.opts = opts #options
        self.n = opts.shape[0] # number of options
        self.q = np.zeros(self.n, dtype = np.float_) #pheromone vector
        self.p = np.arange(0,self.n, 1,dtype=np.int_) # [0,1,2,...,n] all choices
        self.weights = self.calc_weights(k,beta) # weights for calculating probabilities


    def calc_weights(self,k, beta):
        " Probability of choosing route x is proportional to: P(x) = (tau_x+k)^beta/sum_i((tau_i+k)^b) for all i in I, and x member of I"
        return np.power(self.q+k, beta)/np.sum(np.power(self.q+k,beta))


    def update_weights(self,k,beta):
        " calculate the probability vector based on pheromone concentrations "
        self.weights = self.calc_weights(k,beta)

    def add_pheromone(self, i,q,):
        " add pheromone to the pheromone vector "
        #index i, quantity q
        self.q[i]+=q

    def evaporate(self, tau):
        " evaporate the pheromone "
        self.q *= tau

    def greedy(self):
        " return the index of the choice with the most pheromone "
        return int(np.argmax(self.q))

    def parameter(self, i):
        return self.opts[i]

    @property
    def summer(self):
        " return the sum of all pheromones "
        return np.sum(self.q)

    @property
    def choose(self):
        " draw a random choice based on probability defined in self.calc_weights "
        x = np.random.rand()
        choice = self.p[np.where(np.cumsum(self.weights) > x)][0]
        return int(choice)

    def __enter__(self):
        """ return when class is casted in 'with object as ..:"""
        return self

    def __exit__(self, type, value, traceback):
        """ Accompanies __enter__"""
        pass

class ant:
    def __init__(self, ant_id ):
        self.routes = []
        self.scores = []
        self.id = ant_id

    @property
    def score(self ):
        " return latest score "
        return self.scores[-1]
    @score.setter
    def score(self, x):
        " keep track of the performance of the routes "
        self.scores.append(x)

    @property
    def get_route(self):
        " return the latest route "
        return self.routes[-1]

    def new_route(self ):
        " append the list of routes with a new one "
        self.routes.append([])

    def add_segment(self, segment):
        " add a new step to the current route "
        self.routes[-1].append(segment)


    def __enter__(self):
        """ return when class is casted in 'with object as ..:"""
        return self

    def __exit__(self, type, value, traceback):
        """ Accompanies __enter__"""
        pass

import matplotlib.pyplot as plt
class plotter:
    def __init__(self, n, obj_list):
        plt.ion()
        self.vecs = []
        self.names = []
        self.x = []
        self.fig, self.axes = plt.subplots(n,1)
        self.figs = []
        self.fig.tight_layout()
        self.fig.canvas.draw()
        for obj in obj_list:
            self.vecs.append([obj.weights,obj.weights])
            self.x.append(obj.opts)
        for x in self.axes:
            self.figs.append(x)

    def renew(self, obj_list):
        for i in range(len(obj_list)):
            self.vecs[i] = [obj_list[i].weights, obj_list[i].weights]
            try:
                self.figs[i].clear()
                # self.figs[i].remove()
            except:
                pass
            self.figs[i] = self.axes[i].matshow(self.vecs[i],vmin=0,extent=(self.x[i][0],self.x[i][-1],0,1))
            self.axes[i].set_xlabel(obj_list[i].name)
            plt.pause(0.005)
            # self.fig.canvas.draw()
            # plt.draw()

import time

class optimizer:
    def __init__(self, fun, k, beta, n_ants):
        self.k = k
        self.ant_list = []
        self.beta = beta
        self.fun = fun
        self.fun_pars = []
        self.best = 1e99
        self.best_route = []
        self.worst = -1e99
        self.scores = []
        self.t = []
        self.iter = 0
        for i in range(n_ants):
            self.ant_list.append(ant(i))

    def route2args(self,route):
        " return parameters for a route "
        args = np.zeros(len(route),dtype = np.float_)
        for i in range(len(route)):
            args[i] = self.fun_pars[i].parameter(route[i])
        return args

    def add_par(self,choices, name):
        " add a parameter (dimension) to the list "
        self.fun_pars.append(opt(choices,name, self.k,self.beta))

    def get_route(self,mode='greedy'):
        " get the current optimal route "
        route = []
        for par in self.fun_pars:
            route.append(par.greedy())
        return route

    def get_pars(self,mode = 'greedy'):
        " corresponding parameters for a route "
        pars = self.route2args(self.get_route(mode))
        return pars

    def eval_fun(self, mode = 'greedy'):
        " function evaluation "
        pars = self.get_pars(mode)
        return self.fun(*pars)

    def add_pheromone(self, index_list, q, neighbours = False):
        " add q pheromone to the specified routes in index_list "
        for i in range(len(index_list)):
            self.fun_pars[i].add_pheromone(index_list[i],q)
            if neighbours:
                if index_list[i] > 0: self.fun_pars[i].add_pheromone(index_list[i]-1,q*0.2)
                if index_list[i] < self.fun_pars[i].n-1: self.fun_pars[i].add_pheromone(index_list[i]+1,q*0.2)

    def evaporate(self, tau):
        " do evaporate and re-calculate probabilities on all options "
        for pars in self.fun_pars:
            pars.evaporate(tau)
            pars.update_weights(self.k,self.beta)


    def append_score(self,score, step):
        " append the pre-allocated scorekeeping vectors "
        self.t[self.iter] = step
        self.scores[self.iter] = score
        self.iter+=1

    def iteration(self,step):
        " let all agents draw a reinforced random route "
        iteration_best = 1e99
        iteration_worst = -1e99
        for agent in self.ant_list:
            agent.new_route() # append list of historic routes
            for par in self.fun_pars:
                " draw a reinforced-random route for each variable/dimension/option "
                agent.add_segment(par.choose)

            " evaluate the route "
            args=self.route2args(agent.get_route).copy()
            agent.score = self.fun(*args)
            self.append_score(agent.score,step)

            " compare the score "
            if agent.score < iteration_best:
                iteration_best = agent.score
            if agent.score > iteration_worst:
                iteration_worst = agent.score
        return iteration_best, iteration_worst

    def regular_update(self,best,worst, q, tau):
        if best < self.best:
            self.best = best
        if worst > self.worst:
            self.worst = worst
        for agent in self.ant_list:
            " update proportional to ratio "
            frac = np.dot(self.worst-agent.score, 1/(self.worst - self.best))
            self.add_pheromone(agent.get_route, frac*q)
            if agent.score == self.best:
                self.best_route = agent.get_route #keep track of best route

    def elitist_update(self,best, q, tau, neighbours = False):
        if best < self.best:
            " elitist update strategy "
            self.best = best.copy()
            for agent in self.ant_list:
                " only update the best ants "
                if agent.score == self.best:
                    self.best_route = agent.get_route # store the best route
                    self.add_pheromone(agent.get_route, q, neighbours)

    def run(self,steps, q, tau,method='elitist', plot_interval = 0, neighbours = False):
        " evaporation rate tau, deposit quantity q "
        segments = len(self.fun_pars)
        cost = np.zeros(steps, dtype = np.float_)
        plot = plotter(segments, self.fun_pars)
        self.scores = np.zeros(int(steps*len(self.ant_list)), dtype = np.float_) #  y-axis for scatterplot
        self.t = np.zeros(int(steps*len(self.ant_list)), dtype = np.float_) # x-axis for scatter plot

        #loop all steps`
        for i in range(steps):
            # scorekeeper:
            iteration_best, iteration_worst = self.iteration(i)
            if method =='elitist':
                self.elitist_update(iteration_best,q, tau, neighbours)
                self.evaporate(tau)
            elif method == 'regular':
                self.regular_update(best = iteration_best,worst = iteration_worst,q=q,tau=tau)
                self.evaporate(tau)

            cost[i]=self.eval_fun(mode='greedy')
            print(f"Step {i}")
            if i%plot_interval ==0 and plot_interval != 0:
                plot.renew(self.fun_pars)
        plt.close()
        print(f" Best attempt whas: {self.fun(*self.route2args(self.best_route))}")
        return cost

k =.5 #normalizer
beta = 1.6

steps = 50
q = 1.5
tau = .8 # evap rate

plot_interval = max(1,int(steps/25))

x_range = np.arange(-5,5.1,0.5)
y_range = np.arange(-5,5.1,0.5)
z_range = np.arange(-5,5.1,0.5)
O = optimizer(dummy_fun, k,beta, n_ants = 25)
O.add_par(x_range, 'x')
O.add_par(y_range, 'y')
O.add_par(z_range, 'z')
result = O.run(steps, q=q, tau=tau, method='elitist', plot_interval = plot_interval, neighbours = True)
print(f" Optimal parameters: {O.get_pars()} with cost {O.eval_fun()} at step {np.argmin(result)}")
plt.figure(1, figsize=(9, 8))
plt.plot(range(steps),result)
plt.scatter(O.t,O.scores, alpha=.25,s=100, marker = 'D')
plt.show(block=True)
print(result.min())
