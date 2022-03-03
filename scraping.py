# #!/usr/bin/env python
# # coding: utf-8

# # Import Splinter and BeautifulSoup
# from splinter import Browser
# from bs4 import BeautifulSoup as soup
# from webdriver_manager.chrome import ChromeDriverManager
# import datetime as dt
# import pandas as pd

# def scrape_all():
#     # Initiate headless driver for deployment
#     executable_path = {'executable_path': ChromeDriverManager().install()}
#     browser = Browser('chrome', **executable_path, headless=True)
#     # Run all scraping functions and store results in dictionary
#     data = {
#       "news_title": news_title,
#       "news_paragraph": news_paragraph,
#       "featured_image": featured_image(browser),
#       "facts": mars_facts(),
#       "last_modified": dt.datetime.now()
# }
#     # Stop webdriver and return data
#     browser.quit()
#     return data

# # Set up Splinter
# executable_path = {'executable_path': ChromeDriverManager().install()}
# browser = Browser('chrome', **executable_path, headless=False)

# def mars_news(browser):
#     # Scrape Mars News site
#     # Visit the mars nasa news site
#     url = 'https://redplanetscience.com/'
#     browser.visit(url)
#     # Optional delay for loading the page
#     browser.is_element_present_by_css('div.list_text', wait_time=1)

#     # set up html parser
#     html = browser.html
#     news_soup = soup(html, 'html.parser')
#     # Add try/except for error handling
#     try:
#         slide_elem = news_soup.select_one('div.list_text') # <-- parent element
#         # Use the parent element to find the first 'a' tag and save it as 'news_title'
#         # i.e., assign title to variable
#         news_title = slide_elem.find('div', class_='content_title').get_text()
#         # Use the parent element to find the paragraph text
#         news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
#     except AttributeError:
#         return None, None
        
#     return news_title, news_p
    
#     # scrape title and summary text
#     # slide_elem.find('div', class_='content_title')

# # ### 10.3.4 (featured images scraping)

# def featured_image(browser):
#     # Visit URL
#     url = 'https://spaceimages-mars.com'
#     browser.visit(url)

#     # Find and click the full image button
#     full_image_elem = browser.find_by_tag('button')[1]
#     full_image_elem.click()

#     # With the new page loaded onto our automated browser, it needs to be parsed
#     # Parse the resulting html with soup
#     html = browser.html
#     img_soup = soup(html, 'html.parser')
    
#     # Add try/except for error handling
#     try:
#         # Find the relative image url
#         img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
#     except AttributeError:
#         return None
    
#     # Use the base URL to create an absolute URL
#     img_url = f'https://spaceimages-mars.com/{img_url_rel}'
    
#     return img_url
# # Find the relative image url
# #img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
# #img_url_rel

# # ## Mars Facts
# def mars_facts():
#     try:
#         # use 'read_html" to scrape the facts table into a dataframe
#         df = pd.read_html('https://galaxyfacts-mars.com')[0]
#     except BaseException:
#         return None
#     # assign columns and set index of df
#     df.columns=['description', 'Mars', 'Earth']
#     df.set_index('description', inplace=True)
    
#     # convert df into HTML format, add bootstrap
#     return df.to_html()

# # shut down automated browser
# # browser.quit()
# if __name__ == "__main__":

#     # If running as script, print scraped data
#     print(scrape_all())
    
    #############
    
    # Import Splinter, BeautifulSoup, and Pandas
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
import datetime as dt
from webdriver_manager.chrome import ChromeDriverManager


def scrape_all():
    # Initiate headless driver for deployment
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=True)

    news_title, news_paragraph = mars_news(browser)

    # Run all scraping functions and store results in a dictionary
    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
        "last_modified": dt.datetime.now()
    }

    # Stop webdriver and return data
    browser.quit()
    return data


def mars_news(browser):

    # Scrape Mars News
    # Visit the mars nasa news site
    url = 'https://data-class-mars.s3.amazonaws.com/Mars/index.html'
    browser.visit(url)

    # Optional delay for loading the page
    browser.is_element_present_by_css('div.list_text', wait_time=1)

    # Convert the browser html to a soup object and then quit the browser
    html = browser.html
    news_soup = soup(html, 'html.parser')

    # Add try/except for error handling
    try:
        slide_elem = news_soup.select_one('div.list_text')
        # Use the parent element to find the first 'a' tag and save it as 'news_title'
        news_title = slide_elem.find('div', class_='content_title').get_text()
        # Use the parent element to find the paragraph text
        news_p = slide_elem.find('div', class_='article_teaser_body').get_text()

    except AttributeError:
        return None, None

    return news_title, news_p


def featured_image(browser):
    # Visit URL
    url = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html'
    browser.visit(url)

    # Find and click the full image button
    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()

    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')

    # Add try/except for error handling
    try:
        # Find the relative image url
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')

    except AttributeError:
        return None

    # Use the base url to create an absolute url
    img_url = f'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/{img_url_rel}'

    return img_url

def mars_facts():
    # Add try/except for error handling
    try:
        # Use 'read_html' to scrape the facts table into a dataframe
        df = pd.read_html('https://data-class-mars-facts.s3.amazonaws.com/Mars_Facts/index.html')[0]

    except BaseException:
        return None

    # Assign columns and set index of dataframe
    df.columns=['Description', 'Mars', 'Earth']
    df.set_index('Description', inplace=True)

    # Convert dataframe into HTML format, add bootstrap
    return df.to_html(classes="table table-striped")

if __name__ == "__main__":

    # If running as script, print scraped data
    print(scrape_all())
    
    