#! /usr/bin/python
# gpx-poi-loader.py
# Processes CSV POI files from www.poi-factory.com
# Last modified: 28 October 2014

import pyapp.csv_unicode as csv
import sqlite3
import os
import glob
import codecs

db_filename = "pois.sqlite"

if os.path.exists(db_filename):
	os.unlink(db_filename)

conn = sqlite3.connect(db_filename)
cursor = conn.cursor()

cursor.execute("CREATE TABLE pois (id INTERGER PRIMARY KEY, name TEXT, description TEXT, symbol TEXT, latitude FLOAT, longitude FLOAT)")
cursor.execute("CREATE INDEX id on pois (id)")
cursor.execute("CREATE INDEX latitude on pois (latitude)")
cursor.execute("CREATE INDEX longitude on pois (longitude)")

for filename in glob.glob("*.csv"):
	print filename
	basename = os.path.basename(filename)
	base, ext = os.path.splitext(basename)
	data = csv.reader(codecs.open(filename, "rb", "latin1"))
	linenum = 1
	try:
		for row in data:
			longitude, latitude, name, description = row
			cursor.execute(
				"INSERT INTO pois (name, description, symbol, latitude, longitude) values (?, ?, ?, ?, ?)",
				(name, description, base, float(latitude), float(longitude))
				)
			linenum += 1
	except ValueError:
		print "Line %d is bad: %s" % (linenum, str(row))
	except UnicodeDecodeError:
		print "Line %d is bad: %s" % (linenum, str(row))
	
conn.commit()
conn.close()

