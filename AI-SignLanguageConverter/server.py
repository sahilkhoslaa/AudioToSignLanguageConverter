from flask import Flask, request
from flask_cors import CORS
from nltk.corpus import stopwords
from nltk.parse.stanford import StanfordParser
from nltk.stem import WordNetLemmatizer
from nltk.tree import *
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)
CORS(app, supports_credentials=True)

BASE_DIR = os.path.dirname(os.path.realpath(__file__))
# Download zip file from https://nlp.stanford.edu/software/stanford-parser-full-2015-04-20.zip and extract in stanford-parser-full-2015-04-20 folder in higher directory
os.environ['CLASSPATH'] = os.path.join(BASE_DIR, 'stanford-parser-full-2015-04-20')
os.environ['STANFORD_MODELS'] = os.path.join(BASE_DIR, 'stanford-parser-full-2015-04-20/stanford-parser-3.5.2-models/edu/stanford/nlp/models/lexparser/englishPCFG.ser.gz')
os.environ['NLTK_DATA'] = '/usr/local/share/nltk_data/'


def filter_stop_words(words):
    stopwords_set = set(stopwords.words("english"))
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
    eligible_words = ['0', 'axe', 'colour', 'forgive', 'livewhere', 'tools', '1', 'bad', 'colours', 'form', 'lock', 'read', 'touch',
		 '10', 'badminton', 'come', 'four', 'long', 'ready', 'toward', '100', 'bag', 'comeover', 'fourhundred', 'lorry',
		 'receive', 'town', '11', 'bake', 'cometoyou', 'fouroclock', 'lose', 'reception', 'track', '12', 'communicate',
		 'fourteen', 'loss', 'rectangle', 'trade-equipment', '13', 'ballon', 'communication', 'france', 'loss1', 'red',
		 'train', '1month', 'bandage', 'compare', 'friday', 'lotus', 'regions', 'transport', '2-3fingerbent', 'bangali',
		 'compass', 'loud', 'regular', 'travel', '2', 'basketball', 'complain', 'germany', 'love', 'tree', '2months',
		 'bat', 'complaint', 'get', 'man', 'trophy', '3', 'bath', 'concentrate', 'girl', 'mango', 'remind', 'truck',
		 '4', 'beak', 'confuse', 'give-form', 'manner', 'remove', '5', 'bearwithit', 'congratulations', 'give-me',
		 'many', 'repeat', 'try', '6', 'beat', 'go-with-you', 'march', 'research', 'tub', '7', 'beautiful', 'go',
		 'married', 'responsibility', 'tuesday', '8', 'become', 'continue', 'gold', 'may', 'responsible', 'turn', '9',
		 'before', 'control', 'good', 'maybe', 'resting_position', 'turnip', 'A', 'begin', 'cook', 'greece', 'me',
		 'result', 'turnleft', 'behind', 'coolie', 'green', 'meet', 'roof', 'tv', 'C', 'belgium', 'copy', 'grey',
		 'mind', 'round-hand', 'twelveclock', 'Computer', 'bell', 'correct', 'half-past', 'minicom', 'run', 'twenty',
		 'D', 'below', 'halfpast', 'mistake', 'sad', 'two', 'bench', 'count', 'hang', 'monday', 'same', 'twohundred',
		 'F', 'bend', 'cover', 'hardofhearing', 'money', 'save', 'twooclock', 'G', 'benefit', 'crash', 'havealook',
		 'more', 'say', 'typewriter', 'H', 'bent-hand', 'cream', 'he', 'morning', 'science', 'typist', 'I', 'berth',
		 'cricket', 'mother', 'scotland', 'ugly', 'Iv', 'best', 'criticize', 'hearing', 'my', 'screen', 'umbrella', 'J',
		 'better', 'crow', 'n-n(norfolk)', 'search', 'under', 'K', 'between', 'cry', 'hello', 'nagpur', 'see',
		 'understand', 'L', 'bhagat', 'cucumber', 'help-me', 'nails', 'semi-roundhand', 'uniform', 'M', 'bhangra',
		 'cup', 'help-you', 'name', 'send-me', 'university', 'N', 'bible', 'cut', 'her', 'namewhat', 'send', 'until',
		 'O', 'big', 'cycle', 'hers', 'national', 'seven', 'up', 'bird', 'hill', 'near', 'sevenhundred', 'urdu', 'Q',
		 'black', 'date', 'him', 'need', 'sevenoclock', 'us', 'R', 'blackboard', 'day', 'himself', 'needle',
		 'seventeen', 'vadodara', 'Rain', 'blow', 'deaf', 'hindi', 'never', 'sewingmachine', 'van', 'S', 'blue',
		 'decrease', 'hindu', 'shake', 'T', 'boat', 'delete', 'hire', 'news', 'short', 'vegetable', 'Table.AUS', 'body',
		 'dept', 'his', 'next', 'sign', 'vegetables', 'U', 'bogies', 'desk', 'hockey', 'nextyear', 'silver', 'velvet',
		 'V', 'boil', 'hold', 'nice', 'sitandmeet', 'very', 'W', 'book', 'develop', 'holland', 'night', 'six',
		 'veryverydifficult', 'X', 'borrow', 'differences', 'home', 'nine', 'sixhundred', 'video', 'Y', 'bowl',
		 'different', 'how', 'ninehundred', 'sixoclock', 'visit', 'Z', 'boxing', 'difficult', 'howareyou', 'nineoclock',
		 'sixteen', 'volleyball', 'about', 'boy', 'discuss', 'howmany', 'nineteen', 'slow', 'vomit', 'above',
		 'break-in', 'divide', 'howmuch', 'no', 'soft', 'vote', 'absorb', 'break', 'doctor', 'hun', 'none', 'sorry',
		 'wait', 'accept', 'bridge', 'doctor1', 'hundred', 'north-pole', 'spelling', 'wales', 'access', 'brighton',
		 'donotunderstand', 'hungry', 'note-book', 'stay', 'walkacross', 'accident', 'bring', 'down', 'idea',
		 'note-money', 'stubborn', 'wall-clock', 'accuse', 'britain', 'draw', 'ignore', 'now', 'want', 'achakan',
		 'broom', 'dream', 'number', 'sunday', 'was', 'across', 'brown', 'drinking', 'impossible', 'nurse',
		 'switzerland', 'wash', 'act', 'brush', 'easy', 'improve', 'offer', 'tabla', 'waste', 'acting', 'bsl', 'eat',
		 'in', 'office', 'table-tennis', 'water-bottle', 'active', 'education', 'increase', 'officer', 'tablet',
		 'water', 'actor', 'budhpoornima', 'educationalterms', 'index.html', 'often', 'tailor', 'water1', 'actress',
		 'eid', 'informus', 'old', 'take', 'we', 'add', 'building', 'eight', 'infrontof', 'talk', 'weapon', 'advice',
		 'bulb', 'eighteen', 'injection', 'on', 'tall', 'weaver', 'advise', 'bullockcart', 'eighthundred', 'one',
		 'tamil', 'aeroplane', 'busy', 'eightoclock', 'onehundred', 'tap', 'weigh', 'afraid', 'bye', 'electrician',
		 'internet', 'oneoclock', 'taste', 'weight', 'africa', 'c-x', 'electricity', 'interpreter', 'onerupee', 'taxi',
		 'welcome', 'after', 'cabbage', 'issues', 'onetoone', 'teach', 'well', 'afternoon', 'calculator',
		 'elevenoclock', 'iunderstand', 'onion', 'teacher', 'west', 'age', 'call', 'email', 'ix-down', 'ooty',
		 'teachme', 'what', 'agree', 'calm-down', 'ix-left', 'open', 'teachyou', 'wheat', 'alive', 'can', 'empty',
		 'jain', 'opendoors', 'tear', 'when', 'all', 'cancel', 'encourage', 'january', 'openhand', 'tease', 'where',
		 'allah', 'cannot', 'engine', 'jealous', 'operation', 'teat', 'which', 'allday', 'canyousign', 'jeep',
		 'opraise-clap(deaf)', 'technical', 'whistle', 'allover', 'car', 'england', 'or', 'teeth', 'white', 'allow',
		 'carpenter', 'english', 'join', 'orange', 'who', 'almirah', 'carrom', 'enjoy', 'jug', 'order', 'temperature',
		 'why', 'alone', 'carrot', 'enter', 'jump', 'organise', 'temple', 'wide', 'always', 'carry', 'equal', 'june',
		 'ten', 'will', 'ambulance', 'catch-2', 'justamoment', 'our', 'tennis', 'win', 'america', 'catch', 'eraser',
		 'kannada', 'ourself', 'tenoclock', 'wipe-off', 'among', 'cauliflower', 'escape', 'kanpur', 'out', 'thankyou',
		 'wipe', 'andhrapradesh', 'cement', 'essay', 'karate', 'over', 'that', 'wire', 'angel', 'center', 'evening',
		 'keep', 'own', 'theif', 'wish', 'angry', 'certificate', 'every', 'kerala', 'paranoid', 'their', 'with',
		 'announce', 'chair', 'everyday', 'key', 'parts', 'them', 'without', 'chalk', 'everyyear', 'keyboard', 'past',
		 'themselves', 'woman', 'changeback', 'exam', 'kite', 'pay-me', 'then', 'word', 'answer', 'changemind',
		 'examination', 'know', 'pay', 'there', 'work', 'chase', 'examine', 'knowledge', 'pen', 'thermometer',
		 'worn(warn)', 'any', 'check', 'example', 'knowwell', 'person', 'thermus', 'worry', 'anything', 'chemistry',
		 'expensive', 'koli', 'phone', 'these', 'worse', 'appear', 'cheque', 'experience', 'la', 'phoneme', 'they',
		 'worst', 'apple', 'chess', 'eyelash', 'laboratory', 'phoneyou', 'think', 'wrestling', 'appointment', 'child',
		 'factory', 'ladder', 'pick', 'thirsty', 'write', 'children', 'fail-loser', 'lakhnow', 'pink', 'thirteen',
		 'writedown', 'are', 'chilly', 'fall', 'languages', 'plan', 'this', 'writesend', 'area', 'christian', 'far',
		 'late', 'please', 'thorn', 'wrong', 'argue', 'christmas', 'farmer', 'later', 'pooryou', 'those', 'x-ray',
		 'around', 'church', 'fat', 'laugh', 'possible', 'thread', 'yeah', 'arrange', 'cinema', 'father', 'lead', 'pot',
		 'three', 'yellow', 'arrest', 'circle', 'fear', 'leafy-vegetables', 'pound', 'threehundred', 'yes', 'arrive',
		 'circus', 'leak', 'power', 'threeoclock', 'yesterday', 'art', 'clap', 'feed', 'learn', 'practice', 'throw',
		 'you', 'asia', 'class', 'feel', 'leave', 'prayer', 'thumb-little-finger', 'youfillinwipe-off', 'classroom',
		 'few', 'lecturer', 'pretend', 'thumb', 'youhowold', 'clerk', 'fifteen', 'lend', 'print', 'thumbup', 'your',
		 'assam', 'click', 'fight', 'less', 'problem', 'thursday', 'yourhobbieswhat', 'climb', 'fill-in', 'letmeknow',
		 'profit', 'ticket', 'yournamewhat', 'at', 'climbdown', 'fill', 'letter', 'provide', 'ticketchecker', 'yours',
		 'atlast', 'climbup', 'fingerspell', 'level', 'purple', 'tie', 'yourself', 'attend', 'clinic', 'finish',
		 'library', 'put-on-letter', 'tiffinbox', 'yourselves', 'audiologist', 'close', 'five', 'putonleft', 'tight',
		 'zebra-crossing', 'auditorium', 'closedhand', 'fivehundred', 'light-house', 'quarterpast', 'tighten',
		 'australia', 'cloud', 'fiveoclock', 'quarterto', 'time', 'zoo', 'austria', 'clown', 'flood', 'line',
		 'question', 'tippi', 'autorickshaw', 'cobbler', 'floor', 'quick', 'today', 'available', 'fly', 'list', 'quiet',
		 'together', 'avoid', 'collect', 'food', 'litter', 'quote', 'tomato', 'awful', 'college', 'forever',
		 'little-fingerhand', 'quran', 'tomorrow']

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

    # input_string = input_string.lower()
    isl_parsed_token_list = convert_eng_to_isl(input_string)

    # remove stop words
    filtered_isl_token_list = filter_stop_words(isl_parsed_token_list)

    # lemmatize tokens
    lemmatized_isl_token_list = lemmatize_tokens(filtered_isl_token_list)

    isl_text_string = ""

    for token in lemmatized_isl_token_list:
        isl_text_string += token
        isl_text_string += " "

    return isl_text_string + "$" + pre_process(isl_text_string)


if __name__ == "__main__":
    app.run(host="localhost", debug=True)
