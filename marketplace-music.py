'''
Script to download all of the songs listed on NPR's Marketplace show, 
 provided at https://www.marketplace.org/latest-music.
'''

from pyquery import PyQuery as pq
from selenium import webdriver
from selenium.webdriver.support.ui import *
import unicodecsv

#**********************************************
# function to wait until one of the possible_ids shows up
def wait_for_page(driver, possible_CSS=[], possible_xpath=[], seconds=20, interval_to_poll=0.5):
	i = 0
	while(True):
		if i >= seconds/interval_to_poll:
			raise NotFoundException(search = '', msg='Page too slow to load or element never loaded')
			
		if len(possible_CSS) > 0:
			for CSS in possible_CSS:
				#if page(CSS).length > 0:
				els = driver.find_elements_by_css_selector(CSS)
				if len(els) > 0:
					if els[0].is_displayed():
						if els[0].is_enabled():
							return

		elif len(possible_xpath) > 0:
			for xpath in possible_xpath:
				els = driver.find_elements_by_xpath(xpath)
				if len(els) > 0:
					if els[0].is_displayed():
						if els[0].is_enabled():
							return

		else:
			raise ValueError('Did not specify CSS or xpath')
		
		time.sleep(interval_to_poll)
		i = i + 1
#**********************************************

driver = webdriver.Firefox()
driver.implicitly_wait(10)

songs = []

for i in range(1,79):
    # note: the marketplace site frequently gives a "there's been a problem" error. You could
    #       improve this by adding an error handler and repeatedly trying to get the page until it loads
    driver.get('https://www.marketplace.org/latest-music?page=' + str(i))
    wait_for_page(driver=driver, possible_CSS=['.episode-music-title'], seconds=20, interval_to_poll=0.5)

    page = pq(driver.page_source)
    songs_html = page("div.episode-music-row")

    titles=[x.text().encode('utf8').decode('utf8') for x in songs_html.find('.episode-music-title').items()]
    artists=[x.text().encode('utf8').decode('utf8') for x in songs_html.find('.episode-music-artist').items()]

    # add the page's songs to the ongoing list of songs we've collected
    songs.extend(zip([i]*len(titles), artists, titles))
    print 'Done with page ' + str(i)

outtxt=open("C:/users/will/desktop/marketplace.txt","wb")
outwriter = unicodecsv.writer(outtxt, quoting=csv.QUOTE_ALL)
outwriter.writerow(["Page", "Artist", "Title"])
outwriter.writerows(songs)