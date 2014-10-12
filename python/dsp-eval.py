#!/usr/bin/python
import sys
import random

random.seed(10)

def const(bid):
    return bid

def rand(upper):
    return int(random.random() * upper)

def mcpc(ecpc, pctr):
    return int(ecpc * pctr)

def lin(pctr, basectr, basebid):
    return int(pctr *  basebid / basectr)

def win(ccfme, bid):
    return bid >= ccfme[2] and bid > ccfme[3]

if len(sys.argv) < 6:
    print 'Usage: train.log.txt test.log.txt test.lr.txt.pred test.gbrt.txt.pred rtb-result.txt'
    exit(-1)

ccfm = [] # clk cnv floor market
lrpctrs = []
gbrtpctrs = []
totalcost = 0
tecpc = 0.
tctr = 0.

# read in train data for tecpc and tctr
fi = open(sys.argv[1], 'r')
first = True
num = 0
for line in fi:
    s = line.split('\t')
    if first:
        first = False
        continue
    clk = int(s[0])
    cost = int(s[23])
    num += 1
    tctr += clk
    tecpc += cost
fi.close()
tecpc /= tctr
tctr /= num

# read in test data
fi = open(sys.argv[2], 'r')
first = True
for line in fi:
    s = line.split('\t')
    if first:
        first = False
        continue
    clk = int(s[27])
    cnv = int(s[28])
    floorprice = int(s[20])
    marketprice = int(s[23])
    ccfm.append((clk, cnv, floorprice, marketprice))
    totalcost+= marketprice
fi.close()

# read in lr pctr
fi = open(sys.argv[3], 'r')
for line in fi:
    lrpctrs.append(float(line.strip()))
fi.close()

# read in gbrt pctr
fi = open(sys.argv[4], 'r')
for line in fi:
    gbrtpctrs.append(float(line.strip()))
fi.close()

# rock!
budgetProportions = [32, 8, 2]
constParas = range(2, 20, 2) + range(20, 100, 5) + range(100, 301, 10)  #[2, 4, 6, 8, 10, 20, 30, 40, 60, 80, 100, 120, 140, 160, 180, 200, 220, 240, 260, 280, 300]
randParas = range(2, 20, 2) + range(20, 100, 5) + range(100, 501, 10)  #[5, 10, 20, 30, 40, 60, 80, 100, 120, 140, 160, 180, 200, 220, 240, 260, 280, 300, 350, 400, 450, 500]
mcpcParas = [1]
linParas = range(2, 20, 2) + range(20, 200, 5) + range(200, 300, 10) + range(300, 501, 25) # [10, 15, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120, 130, 140, 150, 160, 170, 180, 190, 200, 220, 250, 270, 300, 350, 400, 450, 500]
algoParas = {"const":constParas, "rand":randParas, "mcpc-lr":mcpcParas, "mcpc-gbrt":mcpcParas, "lin-lr":linParas, "lin-gbrt":linParas}

# output format
# budgetProportion clk cnv bid imp budget spend para
def simulateABiddingStategyWithParameter(cases, tcost, proportion, algo, para):
    budget = int(tcost / proportion)
    cost = 0
    clks = 0
    cnvs = 0
    bids = 0
    imps = 0
    for idx in range(0, len(cases)):
        bid = 0
        if algo == "const":
            bid = const(para)
        elif algo == "rand":
            bid = rand(para)
        elif algo == "mcpc-lr":
            lrpctr = lrpctrs[idx]
            bid = mcpc(tecpc, lrpctr)
        elif algo == "mcpc-gbrt":
            gbrtpctr = gbrtpctrs[idx]
            bid = mcpc(tecpc, gbrtpctr)
        elif algo == "lin-lr":
            lrpctr = lrpctrs[idx]
            bid = lin(lrpctr, tctr, para)
        elif algo == "lin-gbrt":
            gbrtpctr = gbrtpctrs[idx]
            bid = lin(gbrtpctr, tctr, para)
        else:
            print 'wrong algo'
            sys.exit(-1)
        bids += 1
        case = cases[idx]
        if win(case, bid):
            imps += 1
            clks += case[0]
            cnvs += case[1]
            cost += case[3]
        if cost > budget:
            break
    return str(proportion) + '\t' + str(clks) + '\t' + str(cnvs) + '\t' + str(bids) + '\t' + \
            str(imps) + '\t' + str(budget) + '\t' + str(cost) + '\t' + algo + '\t'+ str(para)

def simulateABiddingStrategy(cases, tcost, proportion, algo, writer):
    paras = algoParas[algo]
    for para in paras:
        res = simulateABiddingStategyWithParameter(cases, tcost, proportion, algo, para)
        print res
        writer.write(res + '\n')

fo = open(sys.argv[5], 'w')
header = "prop\tclk\tcnv\tbid\timp\tbudget\tspend\talgo\tpara"
fo.write(header + "\n")
print header
for bp in budgetProportions:
    for algo in algoParas:
        simulateABiddingStrategy(ccfm, totalcost, bp, algo, fo)
fo.close()
