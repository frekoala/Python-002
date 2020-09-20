

#作业2
from collections.abc import Iterable

def func(x):
    return x

def map_func(func,iter):
    assert isinstance(iter, Iterable), f'\'{type(iter).__name__}\' object is not iterable'
    for i in iter:
        yield func(i)

# list(map(func, range(10)))
print(list(map_func(func,range(10))))

