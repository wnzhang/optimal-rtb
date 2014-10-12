campaigns="1458" # "1458 2259 2261 2821 2997 3358 3386 3427 3476"
resultsfolder=../results
for campaign in $campaigns; do
    python ../python/check-best-perf.py $resultsfolder/rtb.results.$campaign.tsv
done
