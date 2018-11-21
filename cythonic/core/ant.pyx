from cythonic.plugins.positions cimport point
from cythonic.plugins.functions cimport transform
import numpy as np

cpdef float cube(float x):
    return x*x*x

cdef class Ant:
    " default agent acting in a system "
    def __cinit__(self, double l, unsigned int id,
                    double speed, double gain, double sens_offset,
                    double[:] limits):
        " (virtual) hardware characteristics "
        self.id = id
        self.l = l
        self.v = speed
        self.gain = gain
        self.sens_offset = sens_offset

        " private RNG "

        " state "
        self.foodbound = False
        self.out_of_bounds = False

        " constraints "
        self.limits = point(limits[0], limits[1])

    # cdef void observe(str fun, ):


    cdef bint correct_bounds(self):
        " Check limits, place ant at boundary of neccesary "
        cdef bint xbound = True # assume out of bounds
        cdef bint ybound = True

        " slightly complicated code to ensure all-C performance "
        if self._pos.cx() >= self.limits.cx(): self._pos.xy[0] = self.limits.cx() #upper limit x
        elif self._pos.cx() <= 0.: self._pos.xy[0] = 0. #lower limit x
        else: xbound = False
        if self._pos.cy() >= self.limits.cy(): self._pos.xy[1] = self.limits.cy() #upper limit y
        elif self._pos.cy() <= 0: self._pos.xy[0] = 0. # lower limit y
        else: ybound = False #turns out, not out of bounds

        " return boolean for out_of_bounds"
        if xbound or ybound:
            return True
        else:
            return False

    cpdef void step(self,double dt):
        """ do a step in the current direction, do boundary checking as well """
        # self.rng.add_t(dt) #update timer of the RNG
        # self.time += dt #update internal timer

        " Update position "
        cdef double dL = self.v*dt
        self.pos.xy = transform(self._azimuth,&dL,&self._pos.xy)

        " correct for boundary "
        self.out_of_bounds = self.correct_bounds()
        self.set_sensors()

    cdef void set_sensors(self):
        self._left = transform(self._azimuth+self.sens_offset,&self.l,&self._pos.xy)
        self._right = transform(self._azimuth-self.sens_offset,&self.l,&self._pos.xy)

    cpdef void init_positions(self,double[:] xy):
        self._pos = point(xy[0], xy[1])
        self.set_sensors()


    @property
    def pos(self):
        return (self._pos.x, self._pos.y)
    @property
    def left(self):
        return (self._left.x, self._left.y)
    @property
    def right(self):
        return (self._right.x, self._right.y)
    @property
    def azimuth(self):
        return self._azimuth
    @azimuth.setter
    def azimuth(self,double x):
        if x >= 360.0:
            self._azimuth = x-360.0
        else:
            self._azimuth = x

    def __enter__(self):
        """ return when class is casted in 'with Ant as ..:"""
        return self
    def __exit__(self, type, value, traceback):
        """ Accompanies __enter__"""
        pass
