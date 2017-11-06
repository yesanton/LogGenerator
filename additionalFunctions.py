
import random
from random import randint
def sampleSubSets(ar):
    set1 = set(ar)
    tempAr = []
    while 1:
        t_n = randint(1, 3) % (len(set1) + 1)
        t1 = random.sample(set1, t_n)
        set1.difference_update(t1)

        if t1:
            tempAr.append(t1)
        if not set1:
            break


    return tempAr