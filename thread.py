# import _thread
# import time
#
# # Define a function for the thread
# def print_time( threadName, delay):
#    count = 0
#    while count < 5:
#       time.sleep(delay)
#       count += 1
#       print ("%s: %s" % ( threadName, time.ctime(time.time()) ))
#
# # Create two threads as follows
# try:
#    _thread.start_new_thread( print_time, ("Thread-1", 2, ) )
#    _thread.start_new_thread( print_time, ("Thread-2", 4, ) )
# except:
#    print ("Error: unable to start thread")
#
# while 1:
#    pass

# import threading
# import time
#
# exitFlag = 0
#
# class myThread (threading.Thread):
#    def __init__(self, threadID, name, counter):
#       threading.Thread.__init__(self)
#       self.threadID = threadID
#       self.name = name
#       self.counter = counter
#    def run(self):
#       print ("Starting " + self.name)
#       print_time(self.name, self.counter, 5)
#       print ("Exiting " + self.name)
#
# def print_time(threadName, delay, counter):
#    while counter:
#       if exitFlag:
#          threadName.exit()
#       time.sleep(delay)
#       print ("%s: %s" % (threadName, time.ctime(time.time())))
#       counter -= 1
#
# # Create new threads
# thread1 = myThread(1, "Thread-1", 1)
# thread2 = myThread(2, "Thread-2", 2)
#
# # Start new Threads
# thread1.start()
# thread2.start()
# thread1.join()
# thread2.join()
# print ("Exiting Main Thread")

#!/usr/bin/python3

# import threading
# import time
#
# class myThread (threading.Thread):
#    def __init__(self, threadID, name, counter):
#       threading.Thread.__init__(self)
#       self.threadID = threadID
#       self.name = name
#       self.counter = counter
#    def run(self):
#       print ("Starting " + self.name)
#       # Get lock to synchronize threads
#       threadLock.acquire()
#       print_time(self.name, self.counter, 3)
#       # Free lock to release next thread
#       threadLock.release()
#
# def print_time(threadName, delay, counter):
#    while counter:
#       time.sleep(delay)
#       print ("%s: %s" % (threadName, time.ctime(time.time())))
#       counter -= 1
#
# threadLock = threading.Lock()
# threads = []
#
# # Create new threads
# thread1 = myThread(1, "Thread-1", 1)
# thread2 = myThread(2, "Thread-2", 2)
#
# # Start new Threads
# thread1.start()
# thread2.start()
#
# # Add threads to thread list
# threads.append(thread1)
# threads.append(thread2)
#
# # Wait for all threads to complete
# for t in threads:
#    t.join()
# print ("Exiting Main Thread")




# exitFlag = 0
#
# class myThread (threading.Thread):
#    def __init__(self, threadID, name, q):
#       threading.Thread.__init__(self)
#       self.threadID = threadID
#       self.name = name
#       self.q = q
#    def run(self):
#       print ("Starting " + self.name)
#       process_data(self.name, self.q, 1)
#       print ("Exiting " + self.name)
#
# def process_data(threadName, q, delay):
#    while not exitFlag:
#       queueLock.acquire()
#       if not workQueue.empty():
#          time.sleep(delay)
#          data = q.get()
#          queueLock.release()
#
#          print ("%s processing %s" % (threadName, data))
#          # print("get ident: {}".format(threading.get_ident()))
#          # print("active count: {}".format(threading.active_count()))
#          # print("current thread: {}".format(threading.current_thread()))
#          # print("enumerate: {}".format(threading.enumerate()))
#          # print("main thread: {}".format(threading.main_thread()))
#
#       else:
#          queueLock.release()
#          time.sleep(1)
#
# threadList = ["Thread-1", "Thread-2", "Thread-3"]
# nameList = ["One", "Two", "Three", "Four", "Five"]
# queueLock = threading.Lock()
# workQueue = queue.Queue(10)
# threads = []
# threadID = 1
#
# # Create new threads
# for tName in threadList:
#    thread = myThread(threadID, tName, workQueue)
#    thread.start()
#    threads.append(thread)
#    threadID += 1
#
# # Fill the queue
# queueLock.acquire()
# for word in nameList:
#    workQueue.put(word)
# queueLock.release()
#
# # Wait for queue to empty
# while not workQueue.empty():
#    pass
#    # print('hello')
#
# # Notify threads it's time to exit
# exitFlag = 1
#
# # Wait for all threads to complete
# for t in threads:
#    t.join()
# print ("Exiting Main Thread")

# import queue
# import threading
# import time
#
# def do_stuff(q, delay):
#   while True:
#     print(q.get())
#     time.sleep(delay)
#     print("current thread: {}".format(threading.current_thread()))
#     q.task_done()
#
# q = queue.Queue(maxsize=0)
# num_threads = 99
#
# for i in range(num_threads):
#   worker = threading.Thread(target=do_stuff, args=(q, 1))
#   worker.setDaemon(True)
#   worker.start()
#
# for y in range (10):
#   for x in range(100):
#     q.put(x + y * 100)
#   q.join()
#   print("Batch " + str(y) + " Done")
#
#
# max_size=10
# master_variable=0
# first_clip=0
# queue_1=queue.Queue(maxsize=10)
# queue_2=queue.Queue(maxsize=10)
#
# def set_up_queues(x, var):
# if var==0:
#     global first_clip
#     first_clip=x
# else:
#     queue_1.put(x)
