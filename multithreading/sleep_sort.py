from multiprocessing.pool import ThreadPool
from threading import Thread
from time import sleep
from typing import List


def sort(lst: List[float]):
    sortedlst = []

    def sleeper_func(value):
        sleep(value)
        sortedlst.append(value)

    sleepers = []
    for value in lst:
        sleepers.append(Thread(target=sleeper_func, args=(value,)))
        sleepers[-1].start()

    for sleeper in sleepers:
        sleeper.join()

    return sortedlst


def sort_pool(lst: List[float]):
    def sleeper_func(value):
        sleep(value)
        return value
    pool = ThreadPool(len(lst))
    sortedlst = pool.imap_unordered(sleeper_func, lst)
    return list(sortedlst)


print(sort_pool(np.random.randint(0, 10, 10050)))
