from bs4 import BeautifulSoup
import requests
#anime = "bleach"
def anime_desc(anime):
	URL = "https://myanimelist.net/search/all?q="+anime+"&cat=all"
	r = requests.get(URL) 
	#print(r.content) 
	soup = BeautifulSoup(r.content, 'html.parser')
	#print(soup.prettify())
	table = soup.find('article')  
	#print(table)
	urlval = []
	for row in table.findAll('div',attrs = {'class':'picSurround di-tc thumb'}):
		urlval.append(row.a['href'])
		#print(row)
	#print(urlval)
	urlscrape = urlval[0]
	r1 = requests.get(urlscrape)
	soup1 = BeautifulSoup(r1.content,'html.parser')
	#print(soup1.prettify())
	descanime = soup1.find('p',attrs = {'itemprop':'description'})
	#print(descanime.text)
	#print(descanime.prettify())
	if descanime == None:
		descmanga = soup1.find('span',attrs = {'itemprop':'description'})
		return descmanga.text
	return descanime.text
def anime_info(anime):
	URL = "https://myanimelist.net/search/all?q="+anime+"&cat=all"
	r = requests.get(URL) 
	#print(r.content) 
	soup = BeautifulSoup(r.content, 'html.parser')
	#print(soup.prettify())
	table = soup.find('article')  
	#print(table)
	urlval = []
	for row in table.findAll('div',attrs = {'class':'picSurround di-tc thumb'}):
		urlval.append(row.a['href'])
		#print(row)
	#print(urlval)
	urlscrape = urlval[0]
	r1 = requests.get(urlscrape)
	soup1 = BeautifulSoup(r1.content,'html.parser')
	#print(soup1.prettify())
	img = soup1.find('img',attrs = {'itemprop':'image'})
	#print(img['data-src'])
	info = soup1.find('td',attrs = {'class':'borderClass','width':'225','style':'border-width: 0 1px 0 0;','valign':'top'})
	rows = info.findAll('span',attrs = {'class':'dark_text'})
	final_info = ""
	manga = "false"
	for row in rows:
		check1 = row.parent.findAll('span',attrs = {'itemprop':'genre'})
		if check1 != []:
			checkstr = ""
			for check in check1:
				checkstr = checkstr+check.text+" "
			final_info = final_info+" "+row.text+"\n"+checkstr+"\n"
			#print(row.text)
			#print(checkstr)
			continue
		check2 = row.parent.findAll('span',attrs = {'itemprop':'ratingValue'})
		if check2 != []:
			checkt = row.parent.findAll('span',attrs = {'itemprop':'ratingCount'})
			final_info = final_info+" "+row.text+"\n"
			#print(row.text)
			if checkt != []:
				final_info = final_info+" "+check2[0].text+" Scored by "+checkt[0].text+" Users\n"
				#print(check2[0].text+" Scored by "+checkt[0].text+" Users")
				continue
			final_info = final_info + " invalid "
			#print("invalid")
			continue
		check3 = row.parent.findAll('div',attrs={'class':'statistics-info info2'})
		if check3 != []:
			checkt = row.parent.find('sup')
			if checkt != []:
				final_info = final_info+" "+row.text
				final_info = final_info+" "+checkt.previous_sibling+"\n"
				#print(row.text)
				#print(checkt.previous_sibling)
				continue
			final_info = final_info + " invalid "
			#print("invalid")
		checkmanga = row.parent.findAll('a')
		if checkmanga != []:
			if checkmanga[0].text == "Manga":
				manga = "true"
		if manga == "true":
			final_info = final_info+" "+row.parent.text+"\n"
			continue
		final_info = final_info+" "+row.parent.text
		#print(row.parent.text)
	#print(info.prettify())
	return final_info,img['data-src']
#print(anime_info(anime))
#description = anime_desc(anime)
#print(description)