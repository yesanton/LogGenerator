import datetime, time

import random



def parse_time(date):
    date = date.strip()
    for fmt in ('%Y-%m-%d %H:%M:%S','%d.%m.%y', '%d-%b-%y', '%Y/%m/%d %H:%M:%S'):
        try:
            return datetime.datetime.strptime(date, fmt)
        except ValueError:
            pass
    raise ValueError('no valid date format found')

def find_clusters(r, traces):
    clusters = list()
    visited = set()
    for i in range(len(r)):
        cluster = set()
        for j in range(int(len(r)/2.)):
            if i != j:
                r1 = Range(start=traces[r[i][0]].trace[r[i][1]][2], end=traces[r[i][0]].trace[r[i][1]][3])
                r2 = Range(start=traces[r[j][0]].trace[r[j][1]][2], end=traces[r[j][0]].trace[r[j][1]][3])

                latest_start = max(r1.start, r2.start)
                earliest_end = min(r1.end, r2.end)

                diff = earliest_end - latest_start

                overlap = diff.days * 24 * 60 + diff.seconds / 60

                if overlap >= 1:
                    cluster.add(r[j])
                    cluster.add(r[i])
        if cluster:
            clusters.append(cluster)
            cluster = None


    return clusters


def calculatePositionsForNodesInAGraph(nodes):
    pos = dict()

    #let's find the boundaries
    timestamps = []
    cases = dict()

    for i in nodes:
        timestamps.append(i.timestamp)
        for q in i.case_ids:
            cases[q] = None

    #make dictionary with each case y axis

    minTime = min(timestamps)
    maxTime = max(timestamps)

    N_cases = len(cases)

    y_div = 1.0 / N_cases

    x_div = 1.0 / \
            (time.mktime(maxTime.timetuple())
             - time.mktime(minTime.timetuple()))

    #define the position on the case level

    y_temp = 0
    for i in cases:
        cases[i] = y_temp
        y_temp += y_div

    pick_case = dict()
    pick_temp = []

    for i in nodes:
        if not (i.activity == "Picking"):
            #calculate y axis
            sum_y = 0

            #TODO better way to plot on y axis
            for j in i.case_ids:
                sum_y += cases[j]

            y = sum_y / len(i.case_ids)

            #y =cases[i.case_ids[0]]

            #calculate x axis

            x = (time.mktime(i.timestamp.timetuple()) \
                - time.mktime(minTime.timetuple())) * x_div

            pos[i.id] = (x,y)
        #TODO process pickings and find right place for them
        else:
            elem_temp = list(i.case_ids)[0]
            if not elem_temp in pick_case:
                newDictTemp = dict()
                newDictTemp[i.resource] = [(i.id, i.timestamp)]
                pick_case[elem_temp] = newDictTemp
            elif not i.resource in pick_case[elem_temp]:
                pick_case[elem_temp][i.resource] = [(i.id, i.timestamp)]
            else:
                pick_case[elem_temp][i.resource].append((i.id, i.timestamp))


    for i in pick_case:
        y1_initial = cases[i]
        l = len(pick_case[i])

        y_suppl = 0
        if l > 1:
            y1_initial -= y_div / 3.0
            y_suppl = y_div * 2.0 / (3.0 * (l-1))

        jj = 0
        for j in pick_case[i]:
            y = y1_initial + y_suppl * jj
            for g in pick_case[i][j]:
                print (g[1])
                x = (time.mktime(g[1].timetuple()) \
                     - time.mktime(minTime.timetuple())) * x_div
                pos[g[0]] = (x, y)
            jj = jj + 1







    print(pick_case)
    return pos

def defineColorMapForGraphDrawing(nodes):
    color_dict = dict()

    cases = dict()

    for i in nodes:
        cases[''.join(i.case_ids)] = None

    r = lambda: random.randint(0, 255)

    for i in cases:
        cases[i] = '#%02X%02X%02X' % (r(), r(), r())

    for i in nodes:
        color_dict[i.id] = cases[''.join(i.case_ids)]

    return color_dict


def annotateNodesWithNames(nodes):
    nodesToNamesOfActivities = dict()
    for i in nodes:
        nodesToNamesOfActivities[i.id] = i.activity + ',' + i.payload



    return nodesToNamesOfActivities

















