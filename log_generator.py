#this file contains main code for the log generator
from additionalFunctions import sampleSubSets
from log_constructs import Activity, logElement
import random
from random import randint
#activities in the process 'Order', 'Picking', 'Delivery', 'Payment'
#resouces in the process 'User1', 'User2', 'User3',

universe_of_items = ["pasta", "pesto", "cheese", "brötchen", "pizza", "borshch"]
time_slot = 15 #min



order = Activity("Order", ['User1','User2','User3','User4'])
picking = Activity('Picking', ['WarehouseEmployee1','WarehouseEmployee2','WarehouseEmployee3'])
delivery = Activity("Delivery", ["DeliveryMan1","DeliveryWoman1", "DeliveryMan2", "DeliveryWoman2"])
payment = Activity("Payment", ['User1','User2','User3','User4']) #same user as order!


order.setMultiplicities([picking])
picking.setMultiplicities(None, [delivery])
delivery.setMultiplicities(None, None, [payment])

#N is
N = 100

log = []




for i in range(0, N):
    caseID = "case-" + str(i)
    #now we do for every trace
    itemsSet = random.sample(universe_of_items,randint(1, 6))

    act = logElement()
    act.itemsSet = itemsSet
    act.activity = order.name
    act.resouce = random.choice(order.resources)
    act.caseID = caseID

    log.append(act)

    #this returns the set of subsets of the elements to be picked!
    subsets = sampleSubSets(itemsSet)
    for j in range(0,len(subsets)):
        act_t = logElement()
        act_t.caseID = caseID
        act_t.itemsSet = subsets[j]
        act_t.resouce = random.choice(picking.resources)
        act_t.activity = picking.name

        log.append(act_t)




    print(log)








