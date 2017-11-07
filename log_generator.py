#this file contains main code for the log generator
from additionalFunctions import sampleSubSets
from log_constructs import Activity, logElement
import random
from random import randint
from random import randrange
import datetime
#activities in the process 'Order', 'Picking', 'Delivery', 'Payment'
#resouces in the process 'User1', 'User2', 'User3',

universe_of_items = ["pasta", "pesto", "cheese", "brötchen", "pizza", "borshch"]
time_slot = 15 #min

startDate = datetime.datetime(2017, 7, 11,6,00)

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

caseI = 0
for k in range(0,10):
    #the window (not fixed)
    # we will increment all the time with random time shift
    startDate +=  datetime.timedelta(minutes=randrange(30))

    logO = []
    logP = []
    logD = []
    logPay = []

    for i in range(0, 10):
        caseID = "case-" + str(caseI)
        caseI += 1
        #now we do for every trace
        itemsSet = random.sample(universe_of_items,randint(1, 6))

        act = logElement()
        act.itemsSet = itemsSet
        act.activity = order.name
        act.resource = random.choice(order.resources)
        act.caseID = caseID

        logO.append(act)

        #this returns the set of subsets of the elements to be picked!
        subsets = sampleSubSets(itemsSet)
        for j in range(0,len(subsets)):
            act_t = logElement()
            act_t.caseID = caseID
            act_t.itemsSet = subsets[j]
            act_t.resource = random.choice(picking.resources)
            act_t.activity = picking.name
            act_t.prevActivity.append(act)
            logP.append(act_t)

            act_d = logElement()
            act_d.caseID = caseID
            act_d.itemsSet = subsets[j]
            act_d.activity = delivery.name
            act_d.prevActivity.append(act_t)

            logD.append(act_d)



        # the deliveries of different items with be defferentiated
        # only by the
         

        #here will be about payments

        act_pay = logElement()
        act_pay.caseID = caseID
        act_pay.itemsSet = itemsSet
        act_pay.activity = payment.name
        act_pay.resource = act.resource

        for j in range(0, len(subsets)):
            act_pay.prevActivity.append(logD[len(logD) - j - 1])

        logPay.append(act_pay)
    #here we add timespamps and resources


    for el in logO:
        el.timestamp = startDate + datetime.timedelta(minutes=randrange(30))

    for el in logP:
        el.timestamp = el.prevActivity[0].timestamp + \
                       datetime.timedelta(minutes=randrange(60))

    subsetsToFormDeliveries = sampleSubSets(range(0,len(logD)), 5)

    for i in range(0,len(subsetsToFormDeliveries)):
        dates = []
        for j in subsetsToFormDeliveries[i]:
            dates.append(logD[j].prevActivity[0].timestamp)

        m = max(dates)

        dates = []

        date_delivery = m + datetime.timedelta(minutes=randrange(120))

        chooseResource = random.choice(delivery.resources)
        for j in subsetsToFormDeliveries[i]:
            logD[j].timestamp = date_delivery
            logD[j].resource = chooseResource


    #now it's time to make a payment


    for pay in logPay:
        caseID_t = pay.caseID
        timeSTPrev = None
        i = 0
        while not timeSTPrev and i < len(logD):
            if caseID_t == logD[i].caseID:
                timeSTPrev = logD[i].timestamp
            i += 1

        if timeSTPrev:
            pay.timestamp = timeSTPrev + datetime.timedelta(minutes=randrange(120))



    log = log + logO + logP + logD + logPay



log = log


#write to the file
# with open('csvfile.csv','w') as file:
#     for elem in log:
#         print(elem.activity)
#         file.write((elem.activity, elem.caseID), delimiter=',')
#         file.write('\n')


f = open('csvfile.csv','w')

for el in log:
    st = el.activity + ", " + \
         el.caseID + ", " + \
         el.timestamp.strftime("%Y-%m-%d %H:%M:%S") + ", " + \
         el.resource + '\n'
    f.write(st)

























































