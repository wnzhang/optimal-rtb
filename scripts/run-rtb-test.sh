campaigns="1458 2259 2261 2821 2997 3358 3386 3427 3476"
folder=../../make-ipinyou-data
resultsfolder=../results

if [ ! -d $resultsfolder ]; then
  mkdir $resultsfolder
fi

for campaign in $campaigns; do
    echo $campaign
    python ../python/rtb-test.py $folder/$campaign/train.yzx.txt $folder/$campaign/test.yzx.txt $folder/$campaign/test.yzx.txt.lr.pred $resultsfolder/rtb.results.$campaign.tsv
    python ../python/check-best-perf.py $resultsfolder/rtb.results.$campaign.tsv
done
