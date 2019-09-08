# To add a new cell, type '#%%'
# To add a new markdown cell, type '#%% [markdown]'

from bs4 import BeautifulSoup
import requests
from splinter import Browser
import pandas as pd
import numpy as np
import pymongo

def init_browser(): 
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {'executable_path':'/usr/local/bin/chromedriver'}
    return Browser("chrome", **executable_path, headless=False)

mission_to_mars = {}

# Mars News

def scrape_mars_news():
    browser = init_browser()

    # URL of page to be scraped
    url = "https://mars.nasa.gov/news/"
    browser.visit(url)

# Retrieve page 
    response = requests.get(url)
   
    # Create BeautifulSoup object; parse with 'html.parser'
    soup = BeautifulSoup(response.text, 'html.parser')

    # Determine the elements that contains requested info
    print(soup.prettify())
   
    # Identify and return title of article and first paragraph

    title = soup.find_all('div','content_title')[0].text
    print(title)

    paragraph = soup.find_all('div','rollover_description_inner')[0].text.strip()
    print(paragraph)           
    
    # Dictionary entry from MARS NEWS
    mission_to_mars['news_title'] = title
    mission_to_mars['news_paragraph'] = paragraph

    browser.quit()
    
    return mission_to_mars


# # JPL Mars Space Images - Featured Image (Splinter)
def scrape_mars_image():
    browser = init_browser()
   
    # Visit Mars Space Images 
    image_url= 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(image_url)

    #Use soup to get image URL
    html = browser.html
    isoup = BeautifulSoup(html, 'html.parser')

    #Navigate to mian page
    page_url = 'http://www.jpl.nasa.gov'

    #Scrape image URL (count into array)

    image_url = isoup.find('article',class_="carousel_item")["style"][23:75]

    feature_image_url = page_url + image_url

    print(feature_image_url)
    
    # Dictionary entry from MARS IMAGE
    mission_to_mars['featured_image_url'] = feature_image_url
   
    browser.quit()
    
    return mission_to_mars

# # Mars Tweet (Splinter)
def scrape_mars_weather():
    browser = init_browser()
    
    url = "https://twitter.com/marswxreport?lang=en"
    browser.visit(url)
  
    # Identify the latest weather tweet

    html = browser.html
    soup_tweet = BeautifulSoup(html, 'html.parser')

    #Return all tweets
    weather = soup_tweet.find_all('div', class_="js-tweet-text-container")

    #Search resulst (weather) for tweet that contains weather deets
    for mweather in weather:
        mars_weather = mweather.find('p').text
        if 'Sol' and 'pressure' in mars_weather:
            print(mars_weather)
            break
        else:
            pass 
    
    # Dictionary entry from MARS TWEET
    mission_to_mars['mars_weather'] = mars_weather
   
    browser.quit()
    
    return mission_to_mars


# # Mars Facts (Pandas)
def scrape_mars_facts():
    browser = init_browser()
    
    # Scrape the table of Mars facts
    url = "https://space-facts.com/mars/"
    table = pd.read_html(url)
    facts = table[1]
    facts.columns = ["Title", "Value"]
    print(facts)

    facts.set_index("Title",inplace=True)
    print(facts)

    html_table = facts.to_html()
    html_table

    html_table.replace('\n', '')

    facts.to_html('table.html')

    # Dictionary entry from MARS FACTS TABLE
    mission_to_mars['mars_facts'] = facts
   
    browser.quit()
    
    return mission_to_mars

# # Mars Hemispheres
def scrape_mars_hemisphere():
    browser = init_browser()

    #URL for page
    mars = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(mars)

    html = browser.html
    hsoup = BeautifulSoup(html, 'html.parser')

    #Part 1 - Get a list of links for the hemispheres
    main_url = 'https://astrogeology.usgs.gov'
    Hlist = []
    links = hsoup.find_all('h3')

    for link in links:
        Hlist.append(link.text)
        
    print(Hlist)

    hemisphere_image_urls =[]

    # Loop through each link to retrive image URL and title 
    for link in Hlist:
        hemisphere = {"title":'',
                    "img_url":''} 

        # Click on the Hemisphere link 
        browser.click_link_by_partial_text(link)
        
        hem = browser.find_by_text('Sample')['href']
        
        hemisphere['title'] = link
        
        hemisphere['img_url'] = hem
        
        hemisphere_image_urls.append(hemisphere)
        
        browser.visit(mars)
        print (hemisphere_image_urls)
        
        # Dictionary entry from MARS FACTS TABLE
        mission_to_mars['mars_hemisphere'] =  hemisphere_image_urls
   
        browser.quit()
    
        return mission_to_mars



