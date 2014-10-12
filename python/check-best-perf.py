#!/usr/bin/python
import sys
import random


if len(sys.argv) < 2:
    print 'Usage: python check-best-perf.py rtb.result.1458.txt'
    exit(-1)

setting_row = {}
setting_perf = {}

# setting is (proportion, algorithm)

fi = open(sys.argv[1], 'r') # rtb.result.1458.txt
fo = open(sys.argv[1].replace('.tsv', '.best.perf.tsv'), 'w')
first = True
for line in fi:
    line = line.strip()
    s = line.split('\t')
    if first:
        first = False
        fo.write(line + '\n')
        continue
    algo = s[6]
    prop = s[0]
    perf = int(s[1])
    setting = (prop, algo)
    if setting in setting_perf and perf > setting_perf[setting] or setting not in setting_perf:
        setting_perf[setting] = perf
        setting_row[setting] = line
fi.close()
for setting in sorted(setting_perf):
    fo.write(setting_row[setting] + '\n')
fo.close()