# Domain Classification for Aztec Tools
```
cd dist
# prepare training/test datasets
python ./src/pre_LLDA.py
gzip ./results/newdocs.dat
mv ./results/newdocs.dat.gz ./models/casestudy/
# train the L-LDA model
java -cp jgibblda.jar jgibblda.LDA -est -alpha 0.5 -beta 0.1 -ntopics 6 -model model -niters 2000 -twords 20 -dir models/casestudy -dfile newdocs.dat.gz
# calculate the accuracy
gunzip ./models/casestudy/model.theta.gz
cp ./models/casestudy/model.theta ./results/
python ./src/post_LLDA.py
```
