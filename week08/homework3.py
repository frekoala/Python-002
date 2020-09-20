import time
from functools import wraps


def timer(func):
    @wraps(func)
    def inner(*args, **kwargs):
        start_time = time.time()
        func(*args, **kwargs)
        end_time = time.time()
        print(f'函数运行时长为:{end_time-start_time}秒')
    return inner

@timer
def func(a):
    while a < 10:
        time.sleep(0.1)
        a += 1

if __name__ == '__main__':
    func(4)       