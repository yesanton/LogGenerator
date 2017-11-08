import datetime


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