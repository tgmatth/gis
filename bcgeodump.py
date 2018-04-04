import sqlite3
import json
import codecs

conn = sqlite3.connect('geodata.sqlite')
cur = conn.cursor()

cur.execute('SELECT * FROM BC_Locations')
print("cur: ", cur)
fhand = codecs.open('where.js','w', "utf-8")
fhand.write("myData = [\n")
count = 0
for row in cur :
	data = (row[4])
	print("data ",data)
	# try: js = json.loads(str(data))
	# except: continue
	  
	try: js = json.loads(data.decode('utf-8'))      
	except: js = [None]  
	if not('status' in js and js['status'] == 'OK') : continue
	##if 'status' not in js or (js['status'] != 'OK' and js['status'] != 'ZERO_RESULTS') : continue

	lat = js["results"][0]["geometry"]["location"]["lat"]
	lng = js["results"][0]["geometry"]["location"]["lng"]
	print ("lat: ",lat)
	
	if lat == 0 or lng == 0 : continue
	where = js['results'][0]['formatted_address']
	where = where.replace("'","")
	try :
		print ("where-lat-lng: ",where, lat, lng)

		count = count + 1
		if count > 1 : fhand.write(",\n")
		output = "["+str(lat)+","+str(lng)+", '"+where+"']"
		fhand.write(output)
	except:
		continue

fhand.write("\n];\n")
cur.close()
fhand.close()
		  
print (count, "records written to where.js")
print ("Open where.html to view the data in a browser")

