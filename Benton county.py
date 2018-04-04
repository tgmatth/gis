import urllib.request
from re import findall
import urllib.request
from re import search
from string import Template
import re
import urllib
import urllib.parse
import sqlite3
import json
import time

url = "http://www.healthy.arkansas.gov/eng/planreview/PLUMB/Benton.htm"
response = urllib.request.urlopen(url)
html = response.read()
htmlStr = html.decode('windows-1252')

serviceurl = "http://maps.googleapis.com/maps/api/geocode/json?"
conn = sqlite3.connect('geodata.sqlite')
cur = conn.cursor()
cur.execute('''
CREATE TABLE IF NOT EXISTS BC_Locations (permit_num INTEGER, date TEXT, name TEXT, address TEXT, geodata TEXT)''')

ndata = findall("<ul><li><a href=(.+?)<", htmlStr)    #extracts html link and permit entry
ndatar = findall("Received:(.+?)-", htmlStr)    #extracts html link and permit entry
for item in ndata:
	exp = "(\d+,?)"
	##htmdata = search(exp,item)
	htmldata = item[:9]
	first = 'http://www.healthy.arkansas.gov/eng/planreview/PLUMB/'
	permit = htmldata 
	full = (first + permit)
	permitnum = permit[:5]
	print ("permitnum: ", permitnum)

	cur.execute("SELECT geodata FROM BC_Locations WHERE permit_num= ?", (permitnum,))
	try:
		data = cur.fetchone()[0]
		print ("Found in database ",permitnum)
		continue
	except:
		print("permtinum except: ", permitnum)
		url2 = full
		response2 = urllib.request.urlopen(url2)
		html2 = response2.read()
		htmlStr2 = html2.decode()
		ndata2 = findall("PROJECT ADDRESS: (.+?.)<", htmlStr2)    #extracts html link and permit entry
		for address in ndata2:
			print("address:", address)
			address = re.sub('[.]', '', address)
			print ("address2: ", address)
			address = address.replace("CITY:","",1)
			address = address.replace("ZIP:","",1)
			print ("address3: ", address) 
		ndata3 = findall('Summary:</td></tr><tr><td bgcolor=#FFFFCC width="102%" colspan="2">(.+?.)PD#', htmlStr2)
		for name in ndata3: 
			print ("name: ", name)
		for itemr in ndatar:
			r_date = itemr
		print("permitnum:", permitnum, "r_date: ", r_date, "name: ", name, "address: ", address)

		# buffer = ""     ## TGM
		# buffer += address     ##TGM
		# print ("buffer : ", buffer) ##TGM
		# buffer = buffer.strip()  ## TGM 
		# print ("buffer2: ", buffer) ##TGM
		# cur.execute("SELECT geodata FROM BC_Locations WHERE address= ?", (address,))
		# try:
		# 	data = cur.fetchone()[0]
		# 	print ("Found in database ",address)
		# 	continue
		# except:
		# 	pass

		print ('Resolving', address)
		url = serviceurl + urllib.parse.urlencode({"sensor":"false", "address": address})
		print ('Retrieving', url)
		uh = urllib.request.urlopen(url)
		data = uh.read()

		try: js = json.loads(data.decode('utf-8'))
		except: js = None
 
		print ("js.except: ", js['status']) 
		if 'status' not in js or (js['status'] != 'OK' and js['status'] != 'ZERO_RESULTS') : 
			print ('==== Failure To Retrieve ====')
			print (data)
			break
		print ("insert")	
		cur.execute('''INSERT INTO BC_Locations (permit_num, date, name, address, geodata) 
		VALUES ( ?, ?, ?, ?, ? )''', ( permitnum, r_date, name, address,data ) )

		print("address insert: ", address)
		conn.commit() 
		time.sleep(1)
		print ("Run geodump.py to read the data from the database so you can vizualize it on a map.")
