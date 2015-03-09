import csv

m=[]

with open("rideshare_new.tsv") as tsv:
    for line in csv.reader(tsv, dialect="excel-tab", quoting=csv.QUOTE_NONE):
        m.append(line)
f = open('./cldata.js', 'w+')
print >> f, 'cldata = '
print >> f, m
print >> f, ';'
        
m=[]        
with open("zimride_new.tsv") as tsv:
    last = ""
    for line in csv.reader(tsv, dialect="excel-tab", quoting=csv.QUOTE_NONE):        
        if line[-2]+line[-1] == last:
            last = ""
            continue
        else:
            last = line[-2]+line[-1]
            m.append(line)
f = open('./zdata.js', 'w+')
print >> f, 'zdata = '
print >> f, m
print >> f, ';'        