#This script will create a networkx graph structure from the n-m log
import csv
from trace import Trace

from drawing.additional_functions import parse_time, find_clusters

CASE_ID = 1
ACTIVITY_ID = 0

# this column used to group together m-n processing

RESOURCE_ID = 3
TIMESTAMP_ID = 2

eventlog = "../data/csvfile_s.csv"

csvfile = open(eventlog, 'r')
spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
#next(spamreader, None)  # skip the headers

case_dict = dict()
activity_dict = dict()

resources = set()


case_count = 0
activity_count = 0


traces = list()
trace = None

#we will process it in adjacency list manner
#first let's define what is a node

class node:
    #this is our node
    __ID = 0
    def __init__(self, resource, activity, case_id,timestamp):
        self.id = self.__ID;
        self.__class__.__ID += 1 #this is just unique id for the node
        self.resource = resource
        self.activity = activity
        self.case_ids = []
        self.case_ids.append(case_id)
        self.timestamp = timestamp

node_list = []

for row in spamreader:
    case_id = row[CASE_ID]
    activity_id = row[ACTIVITY_ID]
    resource_id = row[RESOURCE_ID]
    resources.add(resource_id)
    timestamp = row[TIMESTAMP_ID]
    timestamp = parse_time(timestamp)

    n_temp = node(resource_id, activity_id, case_id, timestamp)
    node_list.append(n_temp)


#now find batching of nodes

list_to_remove = set()

for i in range(0,len(node_list)):
    for j in range(i+1, len(node_list)):
        if node_list[i] != node_list[j]:
            if not node_list[i] in list_to_remove \
                    and not node_list[j] in list_to_remove:
                if node_list[i].timestamp == node_list[j].timestamp \
                        and node_list[i].resource == node_list[j].resource:
                    node_list[i].case_ids = node_list[j].case_ids + node_list[i].case_ids
                    list_to_remove.add(node_list[j])
# for n in node_list:
#     for m in node_list:
#         if n != m:
#             if n.timestamp == m.timestamp and n.resource == m.resource:
#                 n.case_ids.append(m.case_ids)
#                 list_to_remove.append(m)

for i in list_to_remove:
    node_list.remove(i)


node_cases = dict()

for i in node_list:
    for j in i.case_ids:
        if not j in node_cases:
            node_cases[j] = []
        node_cases[j].append(i)

#make list of edges

edge_list = []

for i in node_cases:
    for a in range(0, len(node_cases[i])):
        for b in range(a+1, len(node_cases[i])):
            if node_cases[i][a].activity == "Order" and node_cases[i][b].activity == "Picking" or \
                    node_cases[i][a].activity == "Picking" and node_cases[i][b].activity == "Delivery" or \
                    node_cases[i][a].activity == "Delivery" and node_cases[i][b].activity == "Payment":
                edge_list.append((node_cases[i][a].id, node_cases[i][b].id))


#TODO contunie the fix
edge_list = edge_list
































































