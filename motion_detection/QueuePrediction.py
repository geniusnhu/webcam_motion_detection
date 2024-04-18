from collections import deque, Counter
from queue import Queue

def check_consecutive(lst, value, freq=2):
    counter = 1
    for i in range(len(lst) - 1):
        if lst[i] == value and lst[i + 1] == value:
            counter += 1
            if counter == freq:
                return True
        else:
            counter = 1
    return False

class FIFOQueues(Queue):
    def __init__(self, maxsize=1):
        super().__init__(maxsize)

    def post_process(self, threshold):
        q = self.queue
        if len(q) == self.maxsize and q.count('motion') > threshold:
            return 'motion'
        return 'no_motion'
    
def post_process(queue, queue_maxsize, threshold):
    if len(queue) == queue_maxsize and queue.count('motion') > threshold:
        return 'motion'
    return 'no_motion'
