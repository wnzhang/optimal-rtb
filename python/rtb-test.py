#!/usr/bin/python
import sys
import random
import math

random.seed(10)

def bidding_const(bid):
    return bid

def bidding_rand(upper):
    return int(random.random() * upper)

def bidding_mcpc(ecpc, pctr):
    return int(ecpc * pctr)

def bidding_lin(pctr, base_ctr, base_bid):
    return int(pctr * base_bid / base_ctr)

def win_auction(case, bid):
    return bid > case[1]  # bid > winning price

# budgetProportion clk cnv bid imp budget spend para
def simulate_one_bidding_strategy_with_parameter(cases, ctrs, tcost, proportion, algo, para):
    budget = int(tcost / proportion) # intialise the budget
    cost = 0
    clks = 0
    bids = 0
    imps = 0
    for idx in range(0, len(cases)):
        bid = 0
        pctr = ctrs[idx]
        if algo == "const":
            bid = bidding_const(para)
        elif algo == "rand":
            bid = bidding_rand(para)
        elif algo == "mcpc":
            bid = bidding_mcpc(original_ecpc, pctr)
        elif algo == "lin":
            bid = bidding_lin(pctr, original_ctr, para)
        else:
            print 'wrong bidding strategy name'
            sys.exit(-1)
        bids += 1
        case = cases[idx]
        if win_auction(case, bid):
            imps += 1
            clks += case[0]
            cost += case[1]
        if cost > budget:
            break
    return str(proportion) + '\t' + str(clks) + '\t' + str(bids) + '\t' + \
        str(imps) + '\t' + str(budget) + '\t' + str(cost) + '\t' + algo + '\t' + str(para)

def simulate_one_bidding_strategy(cases, ctrs, tcost, proportion, algo, writer):
    paras = algo_paras[algo]
    for para in paras:
        res = simulate_one_bidding_strategy_with_parameter(cases, ctrs, tcost, proportion, algo, para)
        print res
        writer.write(res + '\n')


if len(sys.argv) < 5:
    print 'Usage: python rtb-test.py train.yzx.txt test.yzx.txt test.yzx.txt.lr.pred rtb.result.txt'
    exit(-1)

clicks_prices = []  # clk and price
pctrs = []          # pCTR from logistic regression prediciton
total_cost = 0      # total original cost during the test data
original_ecpc = 0.  # original eCPC from train data
original_ctr = 0.   # original ctr from train data

# read in train data for original_ecpc and original_ctr
fi = open(sys.argv[1], 'r') # train.yzx.txt
first = True
imp_num = 0
for line in fi:
    s = line.split(' ')
    if first:
        first = False
        continue
    click = int(s[0])  # y
    cost = int(s[1])  # z
    imp_num += 1
    original_ctr += click
    original_ecpc += cost
fi.close()
original_ecpc /= original_ctr
original_ctr /= imp_num

# read in test data
fi = open(sys.argv[2], 'r') # test.yzx.txt
for line in fi:
    s = line.split(' ')
    click = int(s[0])
    winning_price = int(s[1])
    clicks_prices.append((click, winning_price))
    total_cost += winning_price
fi.close()

# read in pctr from logistic regression
fi = open(sys.argv[3], 'r')  # test.yzx.txt.lr.pred
for line in fi:
    pctrs.append(float(line.strip()))
fi.close()

# parameters setting for each bidding strategy
budget_proportions = [64, 16] # , 32, 8]
const_paras = range(2, 20, 2) + range(20, 100, 5) + range(100, 301, 10)
rand_paras = range(2, 20, 2) + range(20, 100, 5) + range(100, 501, 10)
mcpc_paras = [1]
lin_paras = range(2, 20, 2) + range(20, 100, 5) + range(100, 400, 10) + range(400, 800, 50)

algo_paras = {"const":const_paras, "rand":rand_paras, "mcpc":mcpc_paras, "lin":lin_paras}

# initalisation finished
# rock!

fo = open(sys.argv[4], 'w')  # rtb.results.txt
#header = "proportion\tclicks\tbids\timpressions\tbudget\tspend\tstrategy\tparameter"
header = "prop\tclks\tbids\timps\tbudget\tspend\talgo\tpara"
fo.write(header + "\n")
print header
for proportion in budget_proportions:
    for algo in algo_paras:
        simulate_one_bidding_strategy(clicks_prices, pctrs, total_cost, proportion, algo, fo)
fo.close()
