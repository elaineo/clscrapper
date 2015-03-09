from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import time
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
    post_urls = [e.get_attribute('href') for e in driver.find_elements_by_xpath("//p[@class='row']/a")]
    return post_urls


def fetch_post(driver, post_url):
    """ Get content of posts """
    driver.get(post_url)
    try:
        email = driver.find_element_by_xpath("//section[@class='dateReplyBar']/a").text
    except NoSuchElementException:
        email = '  '
    try:
        posting_title = driver.find_element_by_xpath("//h2[@class='postingtitle']").text
    except:
        return
    posting_body = driver.find_element_by_xpath("//section[@id='postingbody']").text.replace('\n','\\n')
    timestamp = driver.find_element_by_xpath("//date").get_attribute('title')
    wanted = parse_wanted(posting_title)
    if wanted:
        return False
    start, dest = parse_locs(posting_title, posting_body)
    return email, timestamp, posting_title, post_url, posting_body, start, dest


def main(stop_emails):
    driver = webdriver.Firefox()
    #driver = webdriver.PhantomJS(PHANTOMJS_PATH, desired_capabilities=dcap)
    main_urls = ['http://sfbay.craigslist.org/rid/']
    main_urls = main_urls + ['http://sfbay.craigslist.org/rid/index%i00.html' % i for i in range(1,11)]
    filename = 'rideshare_%i.tsv' % int(time.time())
    stop_fetch = False
    with open(filename, 'w') as f:
        for main_url in main_urls:
            post_urls = fetch_content_page(driver, main_url)
            for post_url in post_urls:
                result = fetch_post(driver, post_url)
                if not result:
                    continue
                if result[0] in stop_emails:
                    stop_fetch = True
                    break
                buf = '\t'.join(result) + '\n'
                f.write(buf.encode('utf-8'))
                time.sleep(FETCH_INTERVAL)
            if stop_fetch:
                break
    driver.close()


def get_last():
    onlyfiles = [ f for f in listdir('.') if isfile(join('.',f)) ]
    valid_files = [f for f in onlyfiles if re.match('rideshare_.+\.tsv', f)]
    valid_files.sort()
    latest_file = valid_files[-1]

    stop_emails = []
    with open(latest_file) as f:
        for line in f:
            last_email = line.split('\t')[0]
            if len(last_email) > 0:
                stop_emails.append(last_email)
                break
    return stop_emails



if __name__ == "__main__":
    main(get_last())
