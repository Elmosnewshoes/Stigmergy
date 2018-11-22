cdef class point:
    cdef public double[2] xy
    cdef public double cx(self)
    cdef public double cy(self)

cdef class index:
    # unsigned integer, grid location
    cdef:
        public unsigned long[2] xy
        public unsigned long cx(self)
        public unsigned long cy(self)
