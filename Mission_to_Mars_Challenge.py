#!/usr/bin/env python
# coding: utf-8

# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd

# Set up Splinter
executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)

# Visit the mars nasa news site
url = 'https://redplanetscience.com/'
browser.visit(url)
# Optional delay for loading the page
browser.is_element_present_by_css('div.list_text', wait_time=1)

# set up html parser
html = browser.html
news_soup = soup(html, 'html.parser')
slide_elem = news_soup.select_one('div.list_text') # <-- parent element

# scrape title and summary text
slide_elem.find('div', class_='content_title')

# Use the parent element to find the first `a` tag and save it as `news_title`
# i.e., assign title to variable
news_title = slide_elem.find('div', class_='content_title').get_text()
news_title

# Use the parent element to find the paragraph text
news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
news_p

# ### 10.3.4 (featured images scraping)

# Visit URL
url = 'https://spaceimages-mars.com'
browser.visit(url)

# Find and click the full image button
full_image_elem = browser.find_by_tag('button')[1]
full_image_elem.click()

# With the new page loaded onto our automated browser, it needs to be parsed
# Parse the resulting html with soup
html = browser.html
img_soup = soup(html, 'html.parser')

# Find the relative image url
img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
img_url_rel

# Use the base URL to create an absolute URL
img_url = f'https://spaceimages-mars.com/{img_url_rel}'
img_url

# ### Scrape Mars Facts (10.3.5)

df = pd.read_html('https://galaxyfacts-mars.com')[0]
df.columns=['description', 'Mars', 'Earth']
df.set_index('description', inplace=True)
df

df.to_html()

# browser.quit()

# # D1: Scrape High-Resolution Mars’ Hemisphere Images and Titles

# 1. Use browser to visit the URL 
url_main = 'https://astrogeology.usgs.gov/'
url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
browser.visit(url)

# Parse html
html = browser.html
img_soup = soup(html, 'html.parser')

# 2. Create a list to hold the images and titles.
hemisphere_image_urls = []

# 3. Write code to retrieve the image urls and titles for each hemisphere.

# return results as list
results = img_soup.find_all('div', class_='item')

# loop through results
for result in results:
    # get title
    title = result.find('h3').text
    
    # get link for full image
    img_url = result.find('a')['href']
    
    # create full_img_url
    full_img_url = url_main + img_url
    
    # use browser to go to full image and parse html
    browser.visit(full_img_url)
    html = browser.html
    img_soup = soup(html, 'html.parser')
    
    # get full image urls
    hemisphere_img = img_soup.find('div', class_='downloads')
    hemisphere_full_image = hemisphere_img.find('a')['href']
    
    # print hemisphere_full_img
    print(hemisphere_full_image)
    
    # create hemisphere dictionary
    hemispheres = dict({'img_url':hemisphere_full_image, 'title':title})
    
    # append hemisphere_image_urls list
    hemisphere_image_urls.append(hemispheres)
    
# 4. Print the list that holds the dictionary of each image url and title.
hemisphere_image_urls

# 5. Quit the browser
browser.quit()