# Import Splinter, BeautifulSoup, and Pandas
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
import datetime as dt


def scrape_all():
    # Initiate headless driver for deployment
    browser = Browser("chrome", executable_path="chromedriver", headless=True)

    news_title, news_paragraph = mars_news(browser)

    # Run all scraping functions and store results in a dictionary
    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
        "last_modified": dt.datetime.now(),
        "hemis_images": hemisphere_images(browser)}

    # Stop webdriver and return data
    browser.quit()
    return data


def mars_news(browser):

    # Scrape Mars News
    # Visit the mars nasa news site
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)

    # Optional delay for loading the page
    browser.is_element_present_by_css("ul.item_list li.slide", wait_time=1)

    # Convert the browser html to a soup object and then quit the browser
    html = browser.html
    news_soup = soup(html, 'html.parser')

    # Add try/except for error handling
    try:
        slide_elem = news_soup.select_one("ul.item_list li.slide")
        # Use the parent element to find the first 'a' tag and save it as 'news_title'
        news_title = slide_elem.find("div", class_="content_title").get_text()
        # Use the parent element to find the paragraph text
        news_p = slide_elem.find(
            "div", class_="article_teaser_body").get_text()

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
        df = pd.read_html('http://space-facts.com/mars/')[0]

    except BaseException:
        return None

    # Assign columns and set index of dataframe
    df.columns = ['Description', 'Mars']
    df.set_index('Description', inplace=True)

    # Convert dataframe into HTML format, add bootstrap
    return df.to_html(classes="table table-striped")


def hemisphere_images(browser):

    # 1. Use browser to visit the URL
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)

    # 2. Create a list to hold the images and titles.
    # List of dictionaries
    hemisphere_image_urls = []

    # 3. Write code to retrieve the image urls and titles for each hemisphere.
    base_url = 'https://astrogeology.usgs.gov'

    html = browser.html
    hemi_image = soup(html, "html.parser")
    # Find all 4 HTML tags that contain hemisphere data
    titles = hemi_image.find_all('div', class_="description")

    # Iterate through each <div class="description" /> tag
    for x in titles:

        # Create dictionary to store data in
        hemisphere = {}

        # Find URL to visit page with full image
        image_address = x.find('a').get('href')
        browser.visit(f'{base_url}{image_address}')

        # Evaluate HTML of newly visited page
        address_soup = soup(browser.html, "html.parser")

        # Get the image URL from the first <a> in the first <li> of an unordered list
        img_url = address_soup.select_one('ul li').find("a").get("href")
        # Add img_url key with f-string address value
        hemisphere['img_url'] = img_url

        # Get title from first <h2 /> and add to dictionary
        title = address_soup.find('h2').get_text()
        hemisphere['title'] = title

        # Append local dictionary to the global image list
        hemisphere_image_urls.append(hemisphere)

    # 4. Print the list that holds the dictionary of each image url and title.
    return hemisphere_image_urls


if __name__ == "__main__":

    # If running as script, print scraped data
    print(scrape_all())

'''
# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
import datetime as dt


def scrape_all():

    # Initiate headless driver for deployment
    browser = Browser('chrome', executable_path="chromderiver", headless=True)

    news_title, news_paragraph = mars_news(browser)

    # Run all scraping functions and store results in dictionary
    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
        "last_modified": dt.datetime.now()
    }

    browser.quit()

    return data

# %%

# Visit the mars NASA news site


def mars_news(browser):

    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)

    # optional delay for laoding the page
    browser.is_element_present_by_css("ul.item_list li.slide", wait_time=1)

    # Convert the browser html to a soup object and then quit the browser
    html = browser.html
    news_soup = soup(html, 'html.parser')

    try:
        slide_elem = news_soup.select_one('ul.item_list li.slide')

        slide_elem.find("div", class_='content_title')

        news_title = slide_elem.find("div", class_='content_title').get_text()

        # Use the parent element to fund the paragraph text
        news_p = slide_elem.find(
            'div', class_="article_teaser_body").get_text()

    except AttributeError:
        return None, None

    return news_title, news_p

# %% [markdown]
# ### Featured Image


def featured_image(browser):

    # Visit URL to get image
    url3 = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html'
    browser.visit(url3)

    # Find and click the full image button
    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()

    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, "html.parser")

    # Find the relative image url
    try:
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
    except:
        AttributeError
        return None

    # Use the base URL to create and absolute URL
    img_url = f'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/{img_url_rel}'
    return img_url


def mars_facts():
    try:
        df = pd.read_html('https://space-facts.com/mars/')[0]
    except:
        BaseException
        return None

    df.columns = ['Description', 'Mars']
    df.set_index('Description', inplace=True)

    return df.to_html()


if __name__ == "__main__":
    # If running as a script, print scraped data
    print(scrape_all())
'''
