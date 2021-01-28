import MySQLdb

db = MySQLdb.connect("localhost", "root", "", "numhome")

cursor = db.cursor()