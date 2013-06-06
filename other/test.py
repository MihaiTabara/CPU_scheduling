from cpu_predictor import Parser

p = Parser("stat_cpu")
data = p.get_results_per_hour()

minutes = []
for tuplu in data:
    minutes.extend(tuplu[0])

with open("output", "w") as fo:
    for minute in minutes:
        fo.write("%d\n" % minute)
