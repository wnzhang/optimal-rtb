Optimal Real-Time Bidding for Display Advertising
===========

A benchmarking framework supporting the experiments of real-time bidding optimisation. A description of such problem and benchmarking experiment is [here](http://arxiv.org/abs/1407.7073).

In the current version, we implemented the feature engineering for logistic regression CTR estimator and standard bidding functions as described in the above reference. The state-of-the-art bidding function proposed in KDD'14 paper [Optimal Real-Time Bidding for Display Advertising](http://www0.cs.ucl.ac.uk/staff/w.zhang/papers/ortb-kdd.pdf) is planned to be published here in Dec. 2014.

For any problems, please report the issues here or contact [Weinan Zhang](http://www0.cs.ucl.ac.uk/staff/w.zhang/).

### Feature Engineering Code
Please check our GitHub project [make-ipinyou-data](https://github.com/wnzhang/make-ipinyou-data). After downloading the dataset, by simplying `make all` you can generate the standardised data which will be used in the bid optimisation tasks.

### Run Bid Optimisation
After successfully generating the data, let's suppose `make-ipinyou-data` project is placed in the same folder of `optimal-rtb` project, just like this:
```
weinan@ZHANG:~/Project$ ls
optimal-rtb    make-ipinyou-data
```
Then under `optimal-rtb/scripts/` you can simply run `bash demo.sh` to train a logistic regression CTR estimator for one campaign data generated in `make-ipinyou-data` and then perform several bid optimisation algorithms with different parameters.

After running the demo, you could find a file `results/rtb.results.1458.best.perf.tsv` containing the best performance for each bidding algorithm.
```
prop    clks    bids    imps    budget  spend   algo    para
16      51      227472  97784   2826028 2826032 const   55
16      482     614638  89408   2826028 2804895 lin     130
16      473     614638  38858   2826028 816763  mcpc    1
16      50      199209  77751   2826028 2826041 rand    100
64      16      472727  57030   706507  706508  const   20
64      471     614638  31908   706507  628971  lin     60
64      330     424901  32372   706507  706520  mcpc    1
64      14      614638  52079   706507  689611  rand    30
```

### Misc
The code implementation of generating features has a little difference between that in [our benchmarking paper](http://arxiv.org/abs/1407.7073): in the orginal dataset, there could be multiple click events for one impression event. In the benchmarking paper, the multiple clicks are directly counted as the number is. In the `make-ipinyou-data` project, we only count for 1 click even if there are more than one clicks.
