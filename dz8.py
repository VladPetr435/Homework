def fibonacci():

 prew = cur = 1

 elements = [0, 1, 1]

 for n in range(100):

    tmp = prew + cur

    prew = cur

    cur = tmp

    elements.append(cur)

 print(elements)

def speed_test():

 import time

 t0 = time.time()

 fibonacci()

 t1 = time.time()

 total = t1-t0

 print(total)