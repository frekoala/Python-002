def partial(func, *args, **keywords):
    def newfunc(*fargs, **fkeywords):
        newkeywords = keywords.copy()
        newkeywords.update(fkeywords)
        return func(*args, *fargs, **newkeywords)

    newfunc.func = func
    newfunc.args = args
    newfunc.keywords = keywords
    return newfunc


def add(a, b):
    return a + b


if __name__ == '__main__':
    add1 = partial(add, 3)
    add2 = partial(add, 1)
    print(add1.__dict__)
    print(add2.__dict__)
    print(add1(2))
    print(add2(3))