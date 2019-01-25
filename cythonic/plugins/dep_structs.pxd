cdef struct dep_fun_args:
    double q # drop quantity
    double beta #f(x,t,beta) = as in exponential decay: x*exp(-beta*t)
    double return_factor #drop specific ratio of q when returning from food
