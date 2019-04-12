# Python script to generate the list of files available in the SignFiles
# directory so that player.js can use it to test it

import os

os.chdir("../SignFiles")

l = os.listdir(os.getcwd())

text = ""

count = 1
for f in l:
	f2 = f.lower()
	f2 = f2.split(".")
	line = str(count) + "," + str(f2[0]) + "," + str(f) +"\n"
	text = text + line
	count = count + 1


os.chdir("../js")
fp = open("sql.csv", "w")
fp.write(text)
fp.close()

print "Saved sql.csv. Please import it in your database :-)"
