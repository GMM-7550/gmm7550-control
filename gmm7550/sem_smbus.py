import smbus
import threading

class SMBus(smbus.SMBus):

    def __init__(self, b):
        super().__init__(b)
        self.sem = threading.Semaphore()

    def acquire(self):
        return self.sem.acquire()

    def release(self):
        return self.sem.release()
