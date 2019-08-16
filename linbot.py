import argparse, os, time
import urllib.parse, random
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup


def Main():
	browser = webdriver.Chrome()
	browser.get('https://linkedin.com/uas/login')

	parser = argparse.ArgumentParser()
	parser.add_argument("email", help="linkedin email")
	parser.add_argument("password", help="linkedin password")
	args = parser.parse_args()



	emailElement = browser.find_element_by_id("username")
	emailElement.send_keys(args.email)
	passElement = browser.find_element_by_id("password")
	passElement.send_keys(args.password)
	passElement.submit()

	os.system('cls')
	print ("[+] Success! Logged In, Bot Starting!")
	ViewBot(browser)
	browser.close()

def getPeopleLinks(page):
	links = []
	for link in page.find_all('a'):
		url = link.get('href')
		if url:
			if 'in/' in url:
				links.append(url)
	return links

def getJobLinks(page):
	links = []
	for link in page.find_all('a'):
		url = link.get('href')
		if url:
			if '/jobs' in url:
				links.append(url)
	return links

def getID(url):
	pUrl = urllib.parse.urlparse(url)
	return urllib.parse.parse_qs(pUrl.query)['in/'][0]

def ViewBot(browser):
	visited = {}
	pList = []
	count = 0
	browser.get("https://www.linkedin.com/mynetwork/")
	npage = BeautifulSoup(browser.page_source)
	f=open("net.txt","wb")
	f.write(npage.encode("utf-8"))
	f.close
	while True:
		#sleep to make sure everything loads.
		#add random to make us look human.
		time.sleep(random.uniform(6.5,9.9))
		page = BeautifulSoup(browser.page_source)
		people = getPeopleLinks(page)
		if people:
			for person in people:
				#ID = getID(person)
				if person not in visited:
					pList.append(person)
					print(person)
					#visited[ID] = 1
		if pList:
				person = pList.pop()
				print(person)
				browser.get("https://www.linkedin.com/"+person)
				count += 1
		else:
				jobs = getJobLinks(page)
				if jobs:
						job = random.choice(jobs)
						root = 'http://www.linkedin.com'
						roots = 'http://www.linkedin.com'
						if root not in job or roots not in job:
								job = 'https://www.linkedin.com'+job
						browser.get(job)
				else:
						print ("I'm Lost Exiting")
						break
		print ("[+] "+browser.title+" Visited! \n("\
		+str(count)+"/"+str(len(pList))+") Visited/Queue")

if __name__ == '__main__':       
    Main()			


