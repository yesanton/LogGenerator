
#we define acticity to be in a way
# activity name | set_of_connected_activities (assigned on runtime) |
# set_of_elements_in_the_process (assigned on runtime) | Timestamp | Caseid (assigned on runtime)
from datetime import time


class Activity:
    def __init__(self, name, resources):
        self.name = name
        self.in_1_to_n = None
        self.in_n_to_1 = None
        self.in_n_to_m = None
        self.resources = resources

    def setMultiplicities(self,in_1_to_n= None ,in_n_to_1= None,in_n_to_m = None):
        self.in_1_to_n = in_1_to_n
        self.in_n_to_1 = in_n_to_1
        self.in_n_to_m = in_n_to_m


class logElement:
    def __init__(self):
        self.activity = ''
        self.resource = ''
        self.itemsSet = []
        self.timestamp = None
        self.caseID = ''
        self.prevActivity = []

