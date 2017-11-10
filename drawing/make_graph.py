#This script will create a networkx graph structure from the n-m log
import csv
from trace import Trace

from drawing.additional_functions import parse_time, find_clusters

def getGraphFromLog():
    CASE_ID = 1
    ACTIVITY_ID = 0

    # this column used to group together m-n processing
    RESOURCE_ID = 3
    TIMESTAMP_ID = 2
    PAYLOAD_ID = 4

    eventlog = "../data/csvfile_s.csv"
    csvfile = open(eventlog, 'r')
    spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
    #next(spamreader, None)  # skip the headers

    resources = set()

    #we will process it in adjacency list manner
    #first let's define what is a node

    class node_elem:
        #this is our node
        __ID = 0
        def __init__(self, resource, activity, case_id,timestamp,payload):
            self.id = self.__ID;
            self.__class__.__ID += 1 #this is just unique id for the node
            self.resource = resource
            self.activity = activity
            self.case_ids = case_id
            # self.case_ids.add(case_id)
            self.timestamp = timestamp
            self.payload = payload



    def make_merged_node(ar, mapping):
        payload = dict()
        case_ids = set()
        for i in ar:
            for j in i.payload:
                if j in payload:
                    payload[j] += i.payload[j]
                else:
                    payload[j] = i.payload[j]

            for j in i.case_ids:
                case_ids.add(j)


        n = node_elem(ar[0].resource, ar[0].activity,
                            case_ids, ar[0].timestamp, payload)
        for i in ar:
            mapping[i.id] = n.id
        return n, mapping


    #STEP 1:
    #Initilize edges and nodes

    node_list_temp = dict()




    for row in spamreader:
        case_id = row[CASE_ID]
        activity_id = row[ACTIVITY_ID]
        resource_id = row[RESOURCE_ID]
        resources.add(resource_id)
        timestamp = row[TIMESTAMP_ID]
        timestamp = parse_time(timestamp)

        payload = row[PAYLOAD_ID].split('+')
        dict_payload = dict()
        for i in payload:
            if not i in dict_payload:
                dict_payload[i] = 1
            else:
                dict_payload[i] += 1


        set_temp = set()
        set_temp.add(case_id)
        n_temp = node_elem(resource_id, activity_id, set_temp, timestamp,dict_payload)

        if not case_id in node_list_temp:
            node_list_temp[case_id] = [n_temp]
        else:
            node_list_temp[case_id].append(n_temp)

    for trace in node_list_temp:
        sortedTr = sorted(node_list_temp[trace], key=lambda node: node.timestamp)
        node_list_temp[trace] = sortedTr


    node_list1 = []
    edge_list = []

    dict_case_ids = set()
    for i in node_list_temp:
        for node in node_list_temp[i]:
            node_list1.append(node)
            if not i in dict_case_ids:
                dict_case_ids.add(i)
            else:
                edge_list.append((node_list1[len(node_list1)-2], node_list1[len(node_list1)-1]))
                print (node_list1[len(node_list1)-2].id, node_list1[len(node_list1)-1].id)



    #STEP 2
    # now find BATCHING of nodes



    d_t = dict()
    for i in node_list1:
        if (i.timestamp, i.resource) in d_t:
            d_t[(i.timestamp, i.resource)].append(i)
        else:
            d_t[(i.timestamp, i.resource)] = [i]

    node_list = []
    mapping = dict()

    for i in d_t:
        if len(d_t[i]) == 1:
            node_list.append(d_t[i][0])
        else:
            temp_node, mapping = make_merged_node(d_t[i],mapping)
            node_list.append(temp_node)

    for i in edge_list:
        print (i[0].id, i[1].id)

    def findMapped(id, node_list):
        for i in node_list:
            if id == i.id:
                return i

    #now find batching edges
    for i in edge_list:
        print (i[0].id )
        if i[0].id in mapping:
            fm = findMapped(mapping[i[0].id], node_list)
            i[0].id = fm.id
            i[0].resource = fm.resource
            i[0].activity = fm.activity
            i[0].case_ids = fm.case_ids
            i[0].timestamp = fm.timestamp
            i[0].payload = fm.payload
        if i[1].id in mapping:
            fm = findMapped(mapping[i[1].id], node_list)
            i[1].id = fm.id
            i[1].resource = fm.resource
            i[1].activity = fm.activity
            i[1].case_ids = fm.case_ids
            i[1].timestamp = fm.timestamp
            i[1].payload = fm.payload


    #TODO make the third step of splitting nodes
    #TODO later change drawing todraw properly

    return node_list, edge_list































































