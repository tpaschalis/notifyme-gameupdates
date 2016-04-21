import mechanize
import cookielib
import csv
import time
import httplib
import urllib


# Browser
br = mechanize.Browser()

# Cookie Jar
cj = cookielib.LWPCookieJar()
br.set_cookiejar(cj)

# Browser options
br.set_handle_equiv(True)
br.set_handle_gzip(True)
br.set_handle_redirect(True)
br.set_handle_referer(True)
br.set_handle_robots(False)

# Follows refresh 0 but not hangs on refresh > 0
br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)

# Want debugging messages?
#br.set_debug_http(True)
#br.set_debug_redirects(True)
#br.set_debug_responses(True)

# User-Agent (this is cheating, ok?)
br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]

# function to grab the 'timeago' value from a steamdb.info website or a corresponding dev blog/wiki
# right now it's dependent on site layout, subject to change, should make it more independent
def grabdate(link):
	r=br.open(link)
	html=r.read()
	if 'steamdb' in link:
		f=html.find("Last Record Update")
		g=html[f:].find("timeago")
		result=html[f+g+16:f+g+41]
	elif 'hearthstone' in link:
		# hs grabs rdy
		# http://hearthstone.gamepedia.com/Patches
		f=html.find('<a href="/Patch_')
		f=f+10
		g=html[f:].find('"')
		result=html[f:f+g]
	elif 'warships' in link:
		# warships grabs rdy
		# http://worldofwarships.eu/en/news/cbt/
		f=html.find("patch")
		g=html[f+1:].find('">')
		result = html[f:f+g]
	elif 'warplanes' in link:
		# world of warplanes grabs rdy
		# print http://worldofwarplanes.eu/game/version/current/
		f=html.find("Game Version")
		g=html[f+1:].find("|")
		result = html[f:f+g]
	elif 'tanks' in link:
		# wot grabs rdy
		# print 'http://worldoftanks.eu/en/content/docs/release_notes/'
		f=html.find("Release Notes")
		g=html[f+1:].find("|")
		result = html[f:f+g]
	elif 'leagueoflegends' in link:
		#lol eune/euw grabs rdy
		# http://eune.leagueoflegends.com/en/news/game-updates/patch
		f=html.find("Most Recent Patch News")
		html=html[f+100:]
		f=html.find("/en/news/game-updates")
		g=html[f+22:].find('"')
		result=html[f:f+22+g]
	else:
		"BAD"
	return result

	
	
def main():
	#reading the (games,links) that will be checked from inputlinks.csv
	inputlinks={}
	for key, val in csv.reader(open("inputlinks_experimental.csv")):
		inputlinks[key]=val
	
	#reading the (game,date) value for all entries from last run
	olddates={}
	for key, val in csv.reader(open("dates_experimental.csv")):
		if val=="BAD":
			print key
			conn = httplib.HTTPSConnection("api.pushover.net:443")
			conn.request("POST", "/1/messages.json",
			urllib.urlencode({
			"token": "PUSHOVER_APP_TOKEN",
			"user": "USER_KEY",
			"message": key+" something's wrong, might be false alarm",
			}), { "Content-type": "application/x-www-form-urlencoded" })
			conn.getresponse()
		olddates[key]=val
		
	#writing the new (game,date) values using grabdate function  	
	newdates={}	
	for key in olddates:
		# print key
		newdates.update({key:grabdate(inputlinks[key])})
	
	#comparing the old and new dates from above
	#if something is different or an error is encountered, a notification is sent
	for key in olddates:
		if olddates[key]!=newdates[key]:
			print "sth is different do sth"
			print "---"
			print key
			conn = httplib.HTTPSConnection("api.pushover.net:443")
			conn.request("POST", "/1/messages.json",
			urllib.urlencode({
			"token": "PUSHOVER_APP_TOKEN",,
			"user": "USER_KEY",
			"message": key+" patch...",
			}), { "Content-type": "application/x-www-form-urlencoded" })
			conn.getresponse()
			print "sth is different do sth"
			
	#the newly computed values from this run overwrite the previous ones	
	w = csv.writer(open("dates_experimental.csv", "w"))
	for key, val in newdates.items():
		w.writerow([key, val])

i=0
#this puts an interval between end-of-run and start of another, rather than really scheduling the run
while True:
	main()
	i+=1
	print "Done ",i
	time.sleep(300)
	
# stuff to implement :: 
# initialization of database (if open(db.csv)==False)
# better exception raising.

# we also need to include example input and output csv files.
