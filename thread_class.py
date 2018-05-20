# -*- coding: utf-8 -*-
#!/usr/bin/env python2
"""
Created on 5/3/18
@author: Zachary Oliver
"""

from log import Log
# get log directory location
from ref_variables import LOG_DIR
from os_functions import evaluate_Time_Difference

from threading import BoundedSemaphore, Thread
import datetime

import multiprocessing


# Used by all threading instances to set the maximum number of threads which can run concurrently within the semaphore
# Assumption: Current Macbook has 2 CPU and 2 threads per CPU so 4 threads available although 1 will always be 
#               already used outside of threading to run the main program
# https://stackoverflow.com/questions/15057301/how-can-i-determine-sensible-thread-number-in-python
MAX_THREADS = multiprocessing.cpu_count() - 1

# Assumption: If the bounded semaphore is instantiated here, there will be multiple instances created
#           because Bounded_Semaphore_Threads will be called multiple times for each thread created.
#           It should instead be created by the script that is using it???
#           Don't know how to pass the BoundedSemaphore instances to a derived run() so will try it here.
#           Maybe this will work because then all threads will share the same BoundedSemaphore for
#           thread management?
threadLimiter = BoundedSemaphore(MAX_THREADS)

# http://ls.pwd.io/2013/06/parallel-s3-uploads-using-boto-and-threads-in-python/
# https://pymotw.com/2/threading/#limiting-concurrent-access-to-resources
# https://stackoverflow.com/questions/19369724/the-right-way-to-limit-maximum-number-of-threads-running-at-once
# https://www.pythoncentral.io/how-to-create-a-thread-in-python/
class Bounded_Semaphore_Thread(Thread):
    def __init__(self, target, name='', args=(), DEBUG=False):
        self.this_log = Log(prefix='thread_class', log_dir=LOG_DIR, DEBUG=DEBUG)
        self.this_log.append("created log file")
        
        msg = "thread_class.py --> Bounded_Semaphore_Thread --> inside init"
        self.this_log.append(msg)
        
        if not args:
            msg = "thread_class.py --> Bounded_Semaphore_Thread --> args: EMPTY!"
            self.this_log.append(msg)
        
        msg = "thread_class.py --> Bounded_Semaphore_Thread --> name: %s" % name
        self.this_log.append(msg)
        
        msg = "thread_class.py --> Bounded_Semaphore_Thread --> args: %s" % str(args)
        self.this_log.append(msg)
        Thread.__init__(self, target=target, name=name, args=args)

    def run(self, DEBUG=False):
        wait_start_time = datetime.datetime.now()
        
        msg = "thread_class.py --> Bounded_Semaphore_Thread --> %s -->  waiting: %s" % (self.getName(), str(datetime.datetime.now().time()))
        self.this_log.append(msg)
        
        threadLimiter.acquire()
        msg = "thread_class.py --> Bounded_Semaphore_Thread --> %s --> approved: %s" % (self.getName(), str(datetime.datetime.now().time()))
        self.this_log.append(msg)
        
        wait_finish_time = datetime.datetime.now()
        difference = evaluate_Time_Difference(wait_finish_time, wait_start_time)
        msg = "thread_class.py --> Bounded_Semaphore_Thread --> %s -------> wait time: %s" % (self.getName(), difference)
        self.this_log.append(msg)
        try:
            run_start_time = datetime.datetime.now()
            
            msg = "thread_class.py --> Bounded_Semaphore_Thread --> %s -->  running: %s" % (self.getName(), str(datetime.datetime.now().time()))
            self.this_log.append(msg)
            # http://www.pythonforbeginners.com/super/working-python-super-function
            super(Bounded_Semaphore_Thread, self).run()
        finally:
            msg = "thread_class.py --> Bounded_Semaphore_Thread --> %s -> completed: %s" % (self.getName(), str(datetime.datetime.now().time()))
            self.this_log.append(msg)
            
            run_finish_time = datetime.datetime.now()
            difference = evaluate_Time_Difference(run_finish_time, run_start_time)
            msg = "thread_class.py --> Bounded_Semaphore_Thread --> %s --------> run time: %s" % (self.getName(), difference)
            self.this_log.append(msg)
            
            difference = evaluate_Time_Difference(run_finish_time, wait_start_time)
            msg = "thread_class.py --> Bounded_Semaphore_Thread --> %s ------> total time: %s" % (self.getName(), difference)
            print msg
            self.this_log.append(msg)
            
            threadLimiter.release()
            msg = "thread_class.py --> Bounded_Semaphore_Thread --> %s --> released: %s" % (self.getName(), str(datetime.datetime.now().time()))
            self.this_log.append(msg)

