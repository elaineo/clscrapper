from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import time
import csv
from os import listdir
from os.path import isfile, join
import re
import logging
from scrapeUtils import *

# TODO - only grab new posts
# TODO - get image links too
FETCH_INTERVAL = 1  # seconds between request
USER_AGENT = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:23.0) Gecko/20131011 Firefox/23.0'
PHANTOMJS_PATH = '/usr/local/bin/phantomjs'
dcap = dict(DesiredCapabilities.PHANTOMJS)
dcap["phantomjs.page.settings.userAgent"] = (USER_AGENT)


def fetch_content_page(driver, url):
    """ Get post urls from content page """
    driver.get(url)
    post_urls = [e.get_attribute('href') for e in driver.find_elements_by_xpath("//div[@class='ride_list']/a")]
    return post_urls


def fetch_post(driver, post_url):
    """ Get content of posts """
    driver.get(post_url)
    try:
        status = driver.find_element_by_xpath("//div[@class='info']/h4").text
        if status == 'Passenger':
            return -1
    except:
        return
    try:
        locstart = driver.find_element_by_xpath("//td[@class='start']").text
    except:
        return
    try:
        locend = driver.find_element_by_xpath("//td[@class='end']").text
    except:
        return        
    departs = driver.find_element_by_xpath("//span[@class='depart']").text
    try:
        returns = driver.find_element_by_xpath("//span[@class='return']").text
    except:
        returns = ""
    try:
        posting_body = driver.find_element_by_xpath("//p[@class='notes']").text.replace('\n','\\n')
    except:
        posting_body = " "
    fb_id = ""
    for f in driver.find_elements_by_xpath("//div[@class='mutual_fb_friends']"):
        fb_id= fb_id + f.get_attribute('data-fbuid')
    return post_url, posting_body, locstart, locend, fb_id, departs, returns

def main(startn):
    driver = webdriver.Firefox()
    #driver = webdriver.PhantomJS(PHANTOMJS_PATH, desired_capabilities=dcap)
    #main_urls = ['http://www.zimride.com/search?filterSearch=true&filter_type=offer']
    post_urls = ['http://www.zimride.com/ride/share?ride=%i' % i for i in range(startn,startn+1000)]
    deadcount = 0
    filename = 'zimride_%i.tsv' % int(time.time())
    stop_fetch = False
    with open(filename, 'w') as f:
        for post_url in post_urls:
            result = fetch_post(driver, post_url)
            print result
            # check for string of Nones
            if result == -1:
                continue
            if not result:
                deadcount=deadcount+1
                if deadcount > 9:
                    break
                continue
            else:
                deadcount = 0
            buf = '\t'.join(result) + '\n'
            f.write(buf.encode('utf-8'))
            time.sleep(FETCH_INTERVAL)
    driver.close()


def get_last():
    with open("zimride_new.tsv") as f:
        for line in f:
            pass
        last_ride = line.split('\t')[0]
        q=last_ride.split('=')[1]
        return int(q)+1

if __name__ == "__main__":
    main(812996) #get_last()
