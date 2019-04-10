import sys
import os
import argparse
from nltk.parse.stanford import StanfordParser
from nltk.tag.stanford import StanfordPOSTagger, StanfordNERTagger
from nltk.tokenize.stanford import StanfordTokenizer
from nltk.tree import *
from nltk import word_tokenize
from nltk.stem import WordNetLemmatizer
import nltk
from nltk.corpus import stopwords
from flask import Flask, session, url_for, render_template,jsonify, request, redirect
from flask_pymongo import PyMongo
from flask_cors import CORS
import hashlib
import os

stop_words = set(["couldn't", 'up', 'have', "didn't", 'me', 'that', 'aren', 'haven', "won't", 'nor', 'not', "you're", 'such', 've', 'the', 'ourselves', 'than', 'this', 'all', "she's", "mustn't", "shan't", 'out', 'during', "you've", 'his', 'yourself', 'but', 'do', 'because', 'd', 'here', 'about', 'at', 'been', 'and', 'once', 'o', 'your', 'over', 'theirs', 'we', "should've", 'few', 'hers', 'weren', 'you', 'her', 'what', 'being', 'through', 'when', 'into', 'just', 'more', 'most', 'won', 'above', 'there', 'did', 'whom', 'doesn', 'further', "aren't", 'again', 'or', 'only', 'both', "mightn't", 'were', 'doing', "wouldn't", 'our', 'having', 'had', 'shan', 'they', 'their', 'now', "hadn't", 'be', "it's", 'an', 'with', 'same', 'if', 'by', 'don', 'then', "hasn't", 'who', "that'll", 't', 'she', 'on', "weren't", 'hadn', 'until', "doesn't", 'too', 'very', 're', 'yours', 'those', 'are', 'against', 'below', 'myself', "shouldn't", 'is', 'own', 'other', 'he', 'so', 'can', 'from', 'mustn', 'does', 'while', 'them', 'which', 'why', 'yourselves', 'didn', 'itself', 'himself', "needn't", 'ours', 'where', "don't", 'between', 'needn', 'my', "isn't", 'ain', 'down', 'am', 's', 'of', 'was', 'has', 'll', 'how', 'i', 'its', "wasn't", 'for', 'off', 'in', 'hasn', 'it', 'under', 'y', 'herself', 'to', 'm', 'a', 'will', "haven't", "couldn't", 'these', 'before', 'should', 'after', 'mightn', 'him', "you'll", 'as', "you'd", 'themselves', 'shouldn', 'any', 'each', 'wasn', 'isn', 'some', 'no', 'ma', "wouldn't"])


app = Flask(__name__)
app.secret_key = os.urandom(24)
CORS(app, supports_credentials = True)

# setting classpath variable
os.environ['CLASSPATH'] = '/home/SahilKhosla/Desktop/AudioToSignLanguageConverter/AI-SignLanguageConverter/stanford-parser-full-2018-10-17' 
parser = StanfordParser(model_path="/home/SahilKhosla/Desktop/stanford-parser-full-2018-10-17/stanford-parser-3.9.2-models/edu/stanford/nlp/models/lexparser/englishPCFG.ser.gz")
os.environ['NLTK_DATA'] = '/usr/local/share/nltk_data/'

def filter_stop_words(words, stopwords):
	print(words)
	words = list(filter(lambda x: x not in stopwords, words))
	print(words)
	return words

@app.route('/purani', methods=['GET','POST'])
def parse():
	# Get input String from Request	
	my_str = "my name is sahil khosla"
	
	# Initializing Stanford Parser
	PARSER = parser.parse(my_str.split())

	# Generating Parse tree
	trees = [tree for tree in PARSER]
	
	parsetree = trees[0]
	
	parent_tree = ParentedTree.convert(parsetree)
	
	dict = {}

	for subtree in parent_tree.subtrees():
		print("SUBTREE : ")    
		print(subtree)

		dict[subtree.treeposition()]=0

		print("LABEL SUBTREE : ")
		print(subtree.label())

	print("----------------------------------------------")

	root_tree = Tree('ROOT',[])
	i=0

	for subtree in parent_tree.subtrees():
	    if(subtree.label()=="NP" and dict[subtree.treeposition()]==0 and dict[subtree.parent().treeposition()]==0):
		dict[subtree.treeposition()]=1
		root_tree.insert(i,subtree)
		i=i+1

	    if(subtree.label()=="VP" or subtree.label()=="PRP"):
			for childtree in subtree.subtrees():
				if((childtree.label()=="NP" or childtree.label()=='PRP')and dict[childtree.treeposition()]==0 and dict[childtree.parent().treeposition()]==0):
					dict[childtree.treeposition()] = 1
		    		root_tree.insert(i,childtree)
		    		i=i+1

	for subtree in parent_tree.subtrees():
	    for childtree in subtree.subtrees():
			print("CHILDTREE : ")
			print(childtree)
			print("CHILDTREE LEAVES : " + str(len(childtree.leaves())))
		   	print("Postion of childtree in maintree : " + str(dict[childtree.treeposition()]))
		   
		   	if(len(childtree.leaves())==1 and dict[childtree.treeposition()]==0 and dict[childtree.parent().treeposition()]==0):
				dict[childtree.treeposition()]=1
				print("CHILDTREE : ")
				print(childtree)
				print("CHILDTREE LEAVES : " + str(len(childtree.leaves())))
				print("Postion of childtree in maintree : " + str(dict[childtree.treeposition()]))
				root_tree.insert(i,childtree)
				i=i+1

		     
	print("ROOT TREE : ")
	print(root_tree)

	print("ROOT TREE Leaves : ")
	print(root_tree.leaves())

	words = root_tree.leaves()
	
	# setting stop words
	# stop_words = set(stopwords.words("english"))
	
	# filter words list
	filter_word_list = filter_stop_words(words, stop_words)

	print('*****************************')

	# Initializing Lemmatizer
	lemmatizer = WordNetLemmatizer()
	lemmatized_words = set([])

	for w in words:
		lemmatized_words.add(lemmatizer.lemmatize(w))

	print("Lemmatized words : ")
	print(lemmatized_words)


	lemmatized_string = ""
	for w in lemmatized_words:
		lemmatized_string += w
		lemmatized_string += " "

	return lemmatized_string

@app.route('/parser', methods=['GET','POST'])
def parseit():
	my_str = "my name is sahil khosla"
	
	# PARSER = parser.parse(my_str.split())
	possible_parse_tree_list = [tree for tree in parser.parse(my_str.split())] #generates all possible parse trees sort by probability for the sentence.
	parsetree = possible_parse_tree_list[0] #most probable parse tree
	dict={}
	#output = '(ROOT (S (PP (IN As) (NP (DT an) (NN accountant))) (NP (PRP I)) (VP (VBP want) (S (VP (TO to) (VP (VB make) (NP (DT a) (NN payment))))))))'
	#parsetree=Tree.fromstring(output)
	#parsetree=parser.raw_parse(s)
	#print parsetree

	#print "***********subtrees**********"
	 
	parent_tree= ParentedTree.convert(parsetree)
	for sub_tree in parent_tree.subtrees():
	    #print sub
	    dict[sub_tree.treeposition()]=0
	   # print sub.label()

	#print "----------------------------------------------"

	root_tree = Tree('ROOT', [])
	i=0
	for sub_tree in parent_tree.subtrees():
	    if sub_tree.label()== "NP" and dict[sub_tree.treeposition()]==0 and dict[sub_tree.parent().treeposition()]==0:
	        dict[sub_tree.treeposition()]=1
	        root_tree.insert(i, sub_tree)
	        i = i+1

	    if sub_tree.label()== "VP" or sub_tree.label()== "PRP":
	        for child_sub_tree in sub_tree.subtrees():
	            if (child_sub_tree.label() == "NP" or child_sub_tree.label() == 'PRP')and dict[child_sub_tree.treeposition()]==0 and dict[child_sub_tree.parent().treeposition()]==0:
	                dict[child_sub_tree.treeposition()]=1
	                root_tree.insert(i, child_sub_tree)
	                i=i+1

	for sub_tree in parent_tree.subtrees():
	    for child_sub_tree in sub_tree.subtrees():
	          # print sub2
	           #print len(sub2.leaves())
	           #print dict[sub2.treeposition()]
	           if(len(child_sub_tree.leaves())==1 and dict[child_sub_tree.treeposition()]==0 and dict[child_sub_tree.parent().treeposition()]==0):
	               dict[child_sub_tree.treeposition()]=1
	            #   print sub2
	             #  print sub2.treeposition()
	              # print dict[sub2.treeposition()]
	               root_tree.insert(i, child_sub_tree)
	               i=i+1

	             
	#print tree2

	#print tree2.leaves()

	parsed_sent=root_tree.leaves()
	#print parsed_sent

	words = parsed_sent
	print(type(words))
	stop_words=set(stopwords.words("english"))
	
	filter_words = []
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

	print(naya)
	return naya

if __name__ == "__main__":
	app.run(host="localhost", debug=True)
