import MySQLdb

db = MySQLdb.connect(host="localhost",    # your host, usually localhost
                     user="root",         # your username
                     passwd="root",  # your password
                     db="text2sign")        # name of the data base

fp = open("k.txt", "r")

line = fp.readline()
line = line.strip()

count = 0
error = 0

fp2 = open("input.csv", "w")

while len(line) > 0:

	try :
		h = []
		l = line.split(" ")

		hamsym = l[0]
		tagname = l[1]

		print "Ham : " + str(hamsym)
		print "Tag : " + str(tagname)
		inputtext = str(hamsym) + "," + str(tagname) + "\n"
		fp2.write(inputtext)

	except:
		print "Error"
		error = error + 1
	
	count = count + 1
	line = fp.readline()
	line = line.strip()

fp.close()
fp2.close()

print "Count : " + str(count)
print "Error : " + str(error)

exit()


# you must create a Cursor object. It will let
#  you execute all the queries you need
cur = db.cursor()

# Use all the SQL you like
cur.execute("SELECT * FROM hindiwords")

# print all the first cell of all the rows
for row in cur.fetchall():
    print row[0]

db.close()