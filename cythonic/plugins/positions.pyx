cdef class point:
    " double, location pair [x,y] in mm "
    def __cinit__(self,x,y):
        self.x = x
        self.y = y

    cdef double cx(self):
        return self.xy[0]
    cdef double cy(self):
        return self.xy[1]

    @property
    def x(self):
        return self.xy[0]
    @x.setter
    def x(self,double x):
        self.xy[0] =x

    @property
    def y(self):
        return self.xy[1]
    @y.setter
    def y(self,double y):
        self.xy[1] =y

    def __repr__(self):
        return "x: {}, y: {}".format(str(self.x),str(self.y))
# cdef struct location:
#     # unsigned integer, grid location
#     unsigned int x,y
