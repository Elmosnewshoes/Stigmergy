# distutils: language = c++

from libc.math cimport M_PI as PI
from libc.math cimport fmin as cmin

cdef void override(ant_state * s, t_max, double * dt):
    s[0].omega = s[0].omega*(1-cmin(s[0].time/t_max,1.)) + s[0].omega*cmin(s[0].time/t_max,1.)/dt[0]

cdef void simple(ant_state* s, rotate_args* args, unsigned int * cur_step):
    " rotate the ant based on angular velocity omega "
    " compute the angular speed (degrees/second) based on sensing "
    " perturb the sensed pheromone quantity with noise "
    # omega(k) = alpha*(L-R+epsilon*covariance)
    s[0].omega = args[0].alpha*180./PI*(s[0].Q_obs.lft-s[0].Q_obs.rght + s[0].noise_vec_1[cur_step[0]]*args[0].covariance_1)

cdef void weber(ant_state* s, rotate_args* args, unsigned int * cur_step):
    " rotate the ant based on angular velocity omega "
    " compute the angular speed (degrees/second) based on sensing "
    " perturb the sensed pheromone quantity with noise "
    # omega(k) = alpha*(L-R+epsilon*covariance)/(L+R) + epsilon_2*covariance_2
    " notice a small regulator parameter in the denominator"
    s[0].omega = args[0].alpha*180./PI*((s[0].Q_obs.lft-s[0].Q_obs.rght+s[0].noise_vec_1[cur_step[0]]*args[0].covariance_1)/(s[0].Q_obs.lft+s[0].Q_obs.rght+args[0].k)+s[0].noise_vec_2[cur_step[0]]*args[0].covariance_2)
