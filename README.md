# Domain Classification for Aztec Tools
Requisites:
```
java 8
python 2.7
pip install nltk, numpy, operator, json
```
Procedures:
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
Results:
```
threshold:  0.1
we have  967  documents.
in which  835  are predicted correctly.
the accuracy is  0.863495346432
threshold:  0.2
we have  967  documents.
in which  846  are predicted correctly.
the accuracy is  0.87487073423
threshold:  0.3
we have  967  documents.
in which  858  are predicted correctly.
the accuracy is  0.88728024819
```
