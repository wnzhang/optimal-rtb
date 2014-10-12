campaigns="1458"
folder=../../make-ipinyou-data
resultsfolder=../results

if [ ! -d $resultsfolder ]; then
  mkdir $resultsfolder
fi

for campaign in $campaigns; do
    echo $campaign
    #python ../python/lryzx.py $folder/$campaign/train.yzx.txt $folder/$campaign/test.yzx.txt
    python ../python/rtb-test.py $folder/$campaign/train.yzx.txt $folder/$campaign/test.yzx.txt $folder/$campaign/test.yzx.txt.lr.pred $resultsfolder/rtb.results.$campaign.tsv
    python ../python/check-best-perf.py $resultsfolder/rtb.results.$campaign.tsv
done
