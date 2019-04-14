from flask import Flask, request
from flask_cors import CORS
# from nltk.corpus import stopwords
from nltk.parse.stanford import StanfordParser
from nltk.stem import WordNetLemmatizer
from nltk.tree import *
import os
import json
# import urllib.request
import zipfile
import sys
import time

app = Flask(__name__)
app.secret_key = os.urandom(24)
CORS(app, supports_credentials=True)

BASE_DIR = os.path.dirname(os.path.realpath(__file__))
# Download zip file from https://nlp.stanford.edu/software/stanford-parser-full-2015-04-20.zip and extract in stanford-parser-full-2015-04-20 folder in higher directory
os.environ['CLASSPATH'] = os.path.join(BASE_DIR, 'stanford-parser-full-2018-10-17')
os.environ['STANFORD_MODELS'] = os.path.join(BASE_DIR,
                                             'stanford-parser-full-2018-10-17/edu/stanford/nlp/models/lexparser/englishPCFG.ser.gz')
os.environ['NLTK_DATA'] = '/usr/local/share/nltk_data/'


def is_parser_jar_file_present():
    stanford_parser_zip_file_path = os.environ.get('CLASSPATH') + ".jar"
    return os.path.exists(stanford_parser_zip_file_path)


def reporthook(count, block_size, total_size):
    global start_time
    if count == 0:
        start_time = time.time()
        return
    duration = time.time() - start_time
    progress_size = int(count * block_size)
    speed = int(progress_size / (1024 * duration))
    percent = min(int(count*block_size*100/total_size),100)
    sys.stdout.write("\r...%d%%, %d MB, %d KB/s, %d seconds passed" %
                    (percent, progress_size / (1024 * 1024), speed, duration))
    sys.stdout.flush()


def download_parser_jar_file():
    stanford_parser_zip_file_path = os.environ.get('CLASSPATH') + ".jar"
    url = "https://nlp.stanford.edu/software/stanford-parser-full-2018-10-17.zip"
    # urllib.request.urlretrieve(url, stanford_parser_zip_file_path, reporthook)

def extract_parser_jar_file():
    stanford_parser_zip_file_path = os.environ.get('CLASSPATH') + ".jar"
    try:
        with zipfile.ZipFile(stanford_parser_zip_file_path) as z:
            z.extractall(path=BASE_DIR)
    except Exception:
        os.remove(stanford_parser_zip_file_path)
        download_parser_jar_file()
        extract_parser_jar_file()


def extract_models_jar_file():
    stanford_models_zip_file_path = os.path.join(os.environ.get('CLASSPATH'), 'stanford-parser-3.9.2-models.jar')
    stanford_models_dir = os.environ.get('CLASSPATH')
    with zipfile.ZipFile(stanford_models_zip_file_path) as z:
        z.extractall(path=stanford_models_dir)


def download_required_packages():
    if not os.path.exists(os.environ.get('CLASSPATH')):
        if is_parser_jar_file_present():
           pass
        else:
            download_parser_jar_file()
        extract_parser_jar_file()

    if not os.path.exists(os.environ.get('STANFORD_MODELS')):
        extract_models_jar_file()


def filter_stop_words(words):
    stopwords_set = set(['a', 'an', 'the', 'is'])
    # stopwords_set = set(stopwords.words("english"))
    words = list(filter(lambda x: x not in stopwords_set, words))
    return words


def lemmatize_tokens(token_list):
    lemmatizer = WordNetLemmatizer()
    lemmatized_words = []
    for token in token_list:
        lemmatized_words.append(lemmatizer.lemmatize(token))

    return lemmatized_words


def label_parse_subtrees(parent_tree):
    tree_traversal_flag = {}

    for sub_tree in parent_tree.subtrees():
        tree_traversal_flag[sub_tree.treeposition()] = 0
    return tree_traversal_flag


def handle_noun_clause(i, tree_traversal_flag, modified_parse_tree, sub_tree):
    # if clause is Noun clause and not traversed then insert them in new tree first
    if tree_traversal_flag[sub_tree.treeposition()] == 0 and tree_traversal_flag[sub_tree.parent().treeposition()] == 0:
        tree_traversal_flag[sub_tree.treeposition()] = 1
        modified_parse_tree.insert(i, sub_tree)
        i = i + 1
    return i, modified_parse_tree


def handle_verb_prop_clause(i, tree_traversal_flag, modified_parse_tree, sub_tree):
    # if clause is Verb clause or Proportion clause recursively check for Noun clause
    for child_sub_tree in sub_tree.subtrees():
        if child_sub_tree.label() == "NP" or child_sub_tree.label() == 'PRP':
            if tree_traversal_flag[child_sub_tree.treeposition()] == 0 and tree_traversal_flag[child_sub_tree.parent().treeposition()] == 0:
                tree_traversal_flag[child_sub_tree.treeposition()] = 1
                modified_parse_tree.insert(i, child_sub_tree)
                i = i + 1
    return i, modified_parse_tree


def modify_tree_structure(parent_tree):
    # Mark all subtrees position as 0
    tree_traversal_flag = label_parse_subtrees(parent_tree)
    # Initialize new parse tree
    modified_parse_tree = Tree('ROOT', [])
    i = 0
    for sub_tree in parent_tree.subtrees():
        if sub_tree.label() == "NP":
            i, modified_parse_tree = handle_noun_clause(i, tree_traversal_flag, modified_parse_tree, sub_tree)
        if sub_tree.label() == "VP" or sub_tree.label() == "PRP":
            i, modified_parse_tree = handle_verb_prop_clause(i, tree_traversal_flag, modified_parse_tree, sub_tree)

    # recursively check for omitted clauses to be inserted in tree
    for sub_tree in parent_tree.subtrees():
        for child_sub_tree in sub_tree.subtrees():
            if len(child_sub_tree.leaves()) == 1:  #check if subtree leads to some word
                if tree_traversal_flag[child_sub_tree.treeposition()] == 0 and tree_traversal_flag[child_sub_tree.parent().treeposition()] == 0:
                    tree_traversal_flag[child_sub_tree.treeposition()] = 1
                    modified_parse_tree.insert(i, child_sub_tree)
                    i = i + 1

    return modified_parse_tree


def convert_eng_to_isl(input_string):
    # get all required packages
    download_required_packages()

    if len(list(input_string.split(' '))) is 1:
        return list(input_string.split(' '))

    # Initializing stanford parser
    parser = StanfordParser()

    # Generates all possible parse trees sort by probability for the sentence
    possible_parse_tree_list = [tree for tree in parser.parse(input_string.split())]

    # Get most probable parse tree
    parse_tree = possible_parse_tree_list[0]
    print(parse_tree)
    # output = '(ROOT
    #               (S
    #                   (PP (IN As) (NP (DT an) (NN accountant)))
    #                   (NP (PRP I))
    #                   (VP (VBP want) (S (VP (TO to) (VP (VB make) (NP (DT a) (NN payment))))))
    #                )
    #             )'

    # Convert into tree data structure
    parent_tree = ParentedTree.convert(parse_tree)

    modified_parse_tree = modify_tree_structure(parent_tree)

    parsed_sent = modified_parse_tree.leaves()
    return parsed_sent


def pre_process(sentence):
    words = list(sentence.split())
    f = open('words.txt', 'r')
    eligible_words = f.read()
    f.close()
    final_string = ""

    for word in words:
        if word not in eligible_words:
            for letter in word:
                final_string += " " + letter
        else:
            final_string += " " + word

    return final_string

@app.route('/parser', methods=['GET', 'POST'])
def parseit():
    if request.method == "POST":
        input_string = request.form['text']
    else:
        input_string = request.args.get('speech')

    # print("input_string: " + input_string)

    # input_string = input_string.lower()
    isl_parsed_token_list = convert_eng_to_isl(input_string)
    # print("isl_parsed_token_list: " + ' '.join(isl_parsed_token_list))

    # lemmatize tokens
    lemmatized_isl_token_list = lemmatize_tokens(isl_parsed_token_list)
    # print("lemmatized_isl_token_list: " + ' '.join(lemmatized_isl_token_list))

    # remove stop words
    filtered_isl_token_list = filter_stop_words(lemmatized_isl_token_list)
    # print("filtered_isl_token_list: " + ' '.join(filtered_isl_token_list))




    isl_text_string = ""

    for token in filtered_isl_token_list:
        isl_text_string += token
        isl_text_string += " "

    data = {
        'isl_text_string': isl_text_string,
        'pre_process_string': pre_process(isl_text_string)
    }
    return json.dumps(data)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)
