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

# setting classpath variable
os.environ['CLASSPATH'] = '/home/SahilKhosla/Desktop/AudioToSignLanguageConverter/AI-SignLanguageConverter/stanford-parser-full-2018-10-17' 
parser = StanfordParser(model_path="/home/SahilKhosla/Desktop/stanford-parser-full-2018-10-17/stanford-parser-3.9.2-models/edu/stanford/nlp/models/lexparser/englishPCFG.ser.gz")

my_str = "i have a dog"

o = parser.parse(my_str.split())
tree1 = [tree for tree in o]
parsetree=tree1[0]

print(parsetree)


