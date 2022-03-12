# Import Splinter, BeautifulSoup, and Pandas
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
from pprint import pprint
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
        "last_modified": dt.datetime.now(),
        "hemispheres": hemisphere_images(browser)
    }
    print(data)
    
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

# Add deliverable 1 hemisphere_images
def hemisphere_images(browser):
    
    # Assign url
    url_main = 'https://astrogeology.usgs.gov/'
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)
    
    # Parse html
    html = browser.html
    img_soup = soup(html, 'html.parser')
    
    # Create a list to hold the images and titles.
    hemisphere_image_urls = []
    
    # Write code to retrieve the image urls and titles for each hemisphere.

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
        try:
            hemisphere_full_image = url_main + img_soup.find('img', class_='wide-image')['src']
        except AttributeError as v:
            print(v)
            return None
        print(hemisphere_full_image)

        # create hemisphere dictionary
        hemispheres = dict({'img_url':hemisphere_full_image, 'title':title})
    
        # append hemisphere_image_urls list
        hemisphere_image_urls.append(hemispheres)

    return hemisphere_image_urls

if __name__ == "__main__":

    # If running as script, print scraped data
    pprint(scrape_all())
    
    