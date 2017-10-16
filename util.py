
#Util module

def frange(start, stop, step):
    if step == 0:
        yield stop
    else:
        if start < stop:
            i = start
            while i < stop:
                yield i
                i += step
            yield stop

        elif start > stop:
            i = start
            while i > stop:
                yield i
                i -= step
            yield stop

        else:
            yield stop

    

def sign(x):
    if x > 0:
        return 1
    if x < 0:
        return -1
    if x == 0:
        return 0
