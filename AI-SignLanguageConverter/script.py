f = open('stopwords.txt','rw+')
out = open('output.txt','w')

words = f.read()
print(words)

stop_words = words.split()
print(stop_words)
