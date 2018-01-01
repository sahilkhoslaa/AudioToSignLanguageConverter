import MySQLdb
import codecs

db = MySQLdb.connect(host="localhost",    # your host, usually localhost
                     user="root",         # your username
                     passwd="root",  # your password
                     db="text2sign", charset='utf8')        # name of the data base

cur = db.cursor()

fp = codecs.open("Database2.csv", "r", "utf-8")
fp2 = open("errors.txt", "w")

line = fp.readline()

count = 0
while len(line.strip()) > 0:
	line = line.strip()
	hindi = []
	l = line.split(",")

	#print "Reading english word"
	engword = l[0].strip().encode('utf').lower()
	
	for x in range(1, 7):
		#print "Reading hindi word"
		pos_hindi_word = l[x].strip()
		pos_hindi_word = pos_hindi_word.strip('"')
		pos_hindi_word = pos_hindi_word.strip()
		if len(pos_hindi_word) > 0:
			hindi.append(pos_hindi_word)

	#print "Reading hamnosys"
	hamnosys = l[7].strip()

	#print "Reading author"
	author = l[8].strip()

	print "Processing word : " + str(engword)
	#print "Hindi words : " + str(hindi)
 	#print "Hamnosys : " + str(hamnosys)
 	#print "Author : " + str(author)
 	#print "==========================="

 	try:
 		sql1 = "insert into englishwords(wordname) values('" + str(engword.encode('utf8')) + "')"
 		cur.execute(sql1)
 		db.commit()
 		engword_id = cur.lastrowid
 		#print "Last id " + str(cur.lastrowid)

 		for word in hindi:
 			sql2 = "insert into hindiwords(wordname, parent) values('" + str(word.encode('utf8')) + "', " + str(engword_id) + ")"
 			cur.execute(sql2)
 			db.commit()

 		if len(hamnosys.encode('utf8')) > 0:
 		 		sql3 = "insert into hamnosys(notation, parent, author) values('" + str(hamnosys.encode('utf8')) + "', " + str(engword_id) + ", '" + str(author) + "')"
 		 		cur.execute(sql3)
 		 		db.commit()
 	except Exception,e:
 		db.rollback()
 		errmsg = "ERROR : " + str(e) + "\n"
 		print "Error : " + errmsg
 		fp2.write(errmsg)


	count = count + 1

	line = fp.readline()

fp.close()
fp2.close()
print count

db.close()