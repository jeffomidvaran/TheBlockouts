import time

class Timer:
    ''' 
        Use as an alternate to sleep when you 
        don't want to freeze the agent's actions 
    '''
    def __init__(self, delay_time):
        self.start_time = time.time()
        self.delay_time = delay_time
        self.stop_time = self.start_time + delay_time
    
    def time_elapsed(self):
        if(self.stop_time <= time.time()):
            self.start_time = time.time()
            self.stop_time = self.start_time + self.delay_time
            return True
        else:
            return False


# #### example code ##### 
# if __name__  == '__main__':
#     '''take an action every n number of seconds'''
#     t = Timer(1)
#     while(True):
#         if(t.time_elapsed() == True):
#             print("timer elapsed")