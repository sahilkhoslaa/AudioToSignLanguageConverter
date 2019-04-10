

import sys
import os
import argparse
from nltk.parse.stanford import StanfordParser
from nltk.tag.stanford import StanfordPOSTagger, StanfordNERTagger
from nltk.tokenize.stanford import StanfordTokenizer
from nltk.tree import *
from nltk import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import nltk

os.environ["CLASSPATH"] = "home/SahilKhosla/Desktop/stanford-parser-full-2018-10-17/stanford-parser.jar:home/SahilKhosla/Desktop/stanford-parser-full-2018-10-17/stanford-parser-3.9.2-models.jar"

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--index", required = True,
	help = "Path to where the computed index will be stored")
args = vars(ap.parse_args())
#s=raw_input("Enter string")
s=args["index"]
parser=nltk.parse.stanford.StanfordParser(model_path="/home/SahilKhosla/Desktop/stanford-parser-full-2018-10-17/stanford-parser-3.9.2-models/edu/stanford/nlp/models/lexparser/englishPCFG.ser.gz")
o=parser.parse(s.split())
tree1=[tree for tree in parser.parse(s.split())]
parsetree=tree1[0]
dict={}
#output = '(ROOT (S (PP (IN As) (NP (DT an) (NN accountant))) (NP (PRP I)) (VP (VBP want) (S (VP (TO to) (VP (VB make) (NP (DT a) (NN payment))))))))'
#parsetree=Tree.fromstring(output)
#parsetree=parser.raw_parse(s)
#print parsetree

#print "***********subtrees**********"
 
ptree= ParentedTree.convert(parsetree)
for sub in ptree.subtrees():
    #print sub
    dict[sub.treeposition()]=0
   # print sub.label()

#print "----------------------------------------------"

tree2=Tree('ROOT',[])
i=0
for sub in ptree.subtrees():
    if(sub.label()=="NP" and dict[sub.treeposition()]==0 and dict[sub.parent().treeposition()]==0):
        dict[sub.treeposition()]=1
        tree2.insert(i,sub)
        i=i+1

       
    if(sub.label()=="VP" or sub.label()=="PRP"):
       
        for sub2 in sub.subtrees():
            if((sub2.label()=="NP" or sub2.label()=='PRP')and dict[sub2.treeposition()]==0 and dict[sub2.parent().treeposition()]==0):
                dict[sub2.treeposition()]=1
                tree2.insert(i,sub2)
                i=i+1

for sub in ptree.subtrees():
    for sub2 in sub.subtrees():
          # print sub2
           #print len(sub2.leaves())
           #print dict[sub2.treeposition()]
           if(len(sub2.leaves())==1 and dict[sub2.treeposition()]==0 and dict[sub2.parent().treeposition()]==0):
               dict[sub2.treeposition()]=1
            #   print sub2
             #  print sub2.treeposition()
              # print dict[sub2.treeposition()]
               tree2.insert(i,sub2)
               i=i+1

             
#print tree2

#print tree2.leaves()

parsed_sent=tree2.leaves()
#print parsed_sent

words=parsed_sent
#print type(words)
stop_words=set(stopwords.words("english"))
filter_words=[]
#print'*****************************'

lemmatizer = WordNetLemmatizer()
lemmatized_words=[]

for w in parsed_sent:
    lemmatized_words.append(lemmatizer.lemmatize(w))

#print lemmatized_words


naya = ""
for w in lemmatized_words:
    naya+=w
    naya+=" "

#print naya 

f = open('out.txt','w')
f.write(naya)
f.close()
