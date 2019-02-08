import inspect
from cythonic.database.__init__ import dummy

def db_path():
    " return the full path to the database "
    path = inspect.getabsfile(dummy)
    return '/'.join(path.split('/')[:-1])+'/'
