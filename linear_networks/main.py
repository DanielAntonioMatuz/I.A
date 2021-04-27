import csv

import numpy as npa

data = npa.zeros([5000])
f= open("183380.csv")
reader = csv.reader(f)
split = npa.zeros([5000])
for row in reader:
    split[0] = (npa.array(row[0].split(";")))
split = npa.asfarray(split)
print (split)