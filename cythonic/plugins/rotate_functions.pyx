# distutils: language = c++

from libc.math cimport M_PI as PI
from libc.math cimport fmin as cmin, sqrt as csqrt, pow as cpow, asin as casin

cdef void override(ant_state * s, double * l ,double * t_max, double * override_max, double * dt):
    " === nudge an ant in the direction of the nest such that theta = omega*dt*(1-rho) + rho*theta_nest"
    cdef double R = csqrt(cpow(s[0].pos.x-s[0].nest.x,2)+cpow(s[0].pos.y-s[0].nest.y,2))
    cdef double theta_offset  # optimal angle correction
    if R < l[0]: # do nothing when very close
        return
    else:
        theta_offset = (180/PI*(casin((s[0].pos.y-s[0].nest.y)/R)+PI)-s[0].theta)%360
        if theta_offset > 180:
            theta_offset -= 360
        s[0].omega = theta_offset/dt[0]*override_max[0]*cmin(s[0].time/t_max[0],1.)+(1-override_max[0]*cmin(s[0].time/t_max[0],1.))*s[0].omega

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
