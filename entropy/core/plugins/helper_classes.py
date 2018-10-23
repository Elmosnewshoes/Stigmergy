class point:
    """ holds xy coordinates in mm (floats)"""
    def __init__(self, x, y):
        self.x = float(x)
        self.y = float(y)

    @property
    def vec(self):
        return [self.x, self.y]

class loc:
    """ holds xy coordinates in grid points (ints (unsigned))"""
    def __init__(self, x, y):
        self.x = int(x)
        self.y = int(y)

    @property
    def vec(self):
        return [self.x, self.y]

def run():
    """ test stuff """
    p = point(*[3,3])
    l = loc(*[3,3])
    print(p.vec)
    print(l.vec)

if __name__ == '__main__':
    run()
