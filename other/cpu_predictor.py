# Mihai Tabara @ UPB
# in the input file, there has been recorded data for more than 12 days
# the data is recorded once in 5 seconds -> that means 720 consecutive
# recordings for the same hour, meaning 12 days of full activity logged

import math

class Parser:

    def __init__(self, filename):
        self.filename = filename

    def parse_values_by_minute(self):
        """
        Returns a list of touples each of which contains
        two consecutive CPU 5 second loggings
        """
        with open(self.filename, "r") as f:
            content = f.readlines()
            pairs = []
            for idx, line in enumerate(content):
                if idx % 12 == 0:
                    pairs.append((line, content[idx+1]))

            return pairs

    def parse_diffs_by_minute(self):
        """
        Returns a list of difference load balancing measured
        each minute
        """

        differences = []
        minute_content = self.parse_values_by_minute()

        for minute in minute_content:
            # two measurements made at 5 second time difference
            x1 = minute[0]
            x2 = minute[1]
            l1 = x1.split()
            l2 = x2.split()
            cpu_balance1 = sum(int(x) for x in l1[1:4])
            cpu_balance2 = sum(int(x) for x in l2[1:4])

            differences.append(math.fabs(cpu_balance1 - cpu_balance2))

        return differences

    def get_results_per_hour(self):
        """
        Returns a 60-minutes list each of which containg a touple (x, y) where
        x -> 60-values list containing balance measured each minute
        y -> average value in the x list
        """
        minutes = self.parse_diffs_by_minute()
        hours = []
        cnt = int(0)
        prov = []
        for minute in minutes:
            if cnt == 60:
                hours.append(prov)
                cnt = 0
                prov = []
                continue
            prov.append(minute)
            cnt += 1

        # 12 days ~= 300 of hours
        return [(hour, math.trunc(sum(hour)/60)) for hour in hours]

if __name__=="__main__":
    p = Parser("stat_cpu")
    data = p.get_results_per_hour()

    import numpy
    import Orange
    d = Orange.data.Domain([Orange.feature.Continuous('a%i' % x) for x in range(61)])
    thelist = []
    for dd in data:
        l = dd[0]
        l.append(dd[1])
        thelist.append(l)

    a = numpy.array(thelist)
    t = Orange.data.Table(d)
    for dd in thelist:
        t.append(dd)

    """
    with open("data.tab", "w") as fw:
        # headers
        s = "\t".join(["c%s" % str(i) for i in range(1, 61)])
        s += "\tresult\n"

        ss = "\t".join(["continuous" for i in range(1,61)])
        ss += "\tcontinuous\n\n"

        s += ss

        # data now

        for d in data:
            ds = "\t".join([str(x) for x in d[0]])
            ds += "\t%s\n" % str(d[1])
            s += ds

        fw.write(s)
    """
    # orange stuff
    #mport Orange
    #data = Orange.data.Table("/home/mihait/work/upb/CPU_scheduling/log/192.168.6.40/data")
    learner = Orange.classification.bayes.NaiveLearner()
    classifier = learner(t)
    import pdb; pdb.set_trace()
