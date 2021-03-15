# %%
# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
from pprint import pprint
from IPython import get_ipython

# %%
# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd


# %%
executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
browser = Browser('chrome', **executable_path)


# %%
# Visit the mars NASA news site
url = 'https://mars.nasa.gov/news/'
browser.visit(url)
# optional delay for laoding the page
browser.is_element_present_by_css("ul.item_list li.slide", wait_time=1)


# %%
html = browser.html
news_soup = soup(html, 'html.parser')
slide_elem = news_soup.select_one('ul.item_list li.slide')


# %%
slide_elem.find("div", class_='content_title')


# %%
news_title = slide_elem.find("div", class_='content_title').get_text()
news_title


# %%
# Use the parent element to fund the paragraph text
news_p = slide_elem.find('div', class_="article_teaser_body").get_text()
news_p

# %% [markdown]
# ### Featured Image

# %%
# Visit URL to get image
url3 = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html'
browser.visit(url3)


# %%
# Find and click the full image button
full_image_elem = browser.find_by_tag('button')[1]
full_image_elem.click()


# %%
# Parse the resulting html with soup
html = browser.html
img_soup = soup(html, "html.parser")


# %%
print(img_soup)


# %%
# Find the relative image url
img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
print(img_url_rel)


# %%
# Use the base URL to create and absolute URL
img_url = f'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/{img_url_rel}'
img_url


# %%
df = pd.read_html('https://space-facts.com/mars/')[0]
df.columns = ['description', 'value']
df.set_index('description', inplace=True)
df


# %%
df.to_html()


# %%
browser.quit()

# %% [markdown]
# # Beginning of Starter Code:

# %%
# Import Splinter, BeautifulSoup, and Pandas


# %%
# Path to chromedriver
get_ipython().system('which chromedriver')


# %%
# Set the executable path and initialize the chrome browser in splinter
executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
browser = Browser('chrome', **executable_path)

# %% [markdown]
# ### Visit the NASA Mars News Site

# %%
# Visit the mars nasa news site
url = 'https://mars.nasa.gov/news/'
browser.visit(url)

# Optional delay for loading the page
browser.is_element_present_by_css("ul.item_list li.slide", wait_time=1)


# %%
# Convert the browser html to a soup object and then quit the browser
html = browser.html
news_soup = soup(html, 'html.parser')

slide_elem = news_soup.select_one('ul.item_list li.slide')


# %%
slide_elem.find("div", class_='content_title')


# %%
# Use the parent element to find the first a tag and save it as `news_title`
news_title = slide_elem.find("div", class_='content_title').get_text()
news_title


# %%
# Use the parent element to find the paragraph text
news_p = slide_elem.find('div', class_="article_teaser_body").get_text()
news_p

# %% [markdown]
# ### JPL Space Images Featured Image

# %%
# Visit URL
url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
browser.visit(url)


# %%
# Find and click the full image button
full_image_elem = browser.find_by_id('full_image')
full_image_elem.click()


# %%
# Find the more info button and click that
browser.is_element_present_by_text('more info', wait_time=1)
more_info_elem = browser.links.find_by_partial_text('more info')
more_info_elem.click()


# %%
# Parse the resulting html with soup
html = browser.html
img_soup = soup(html, 'html.parser')


# %%
# find the relative image url
img_url_rel = img_soup.select_one('figure.lede a img').get("src")
img_url_rel


# %%
# Use the base url to create an absolute url
img_url = f'https://www.jpl.nasa.gov{img_url_rel}'
img_url

# %% [markdown]
# ### Mars Facts

# %%
df = pd.read_html('http://space-facts.com/mars/')[0]

df.head()


# %%
df.columns = ['Description', 'Mars']
df.set_index('Description', inplace=True)
df


# %%
df.to_html()

# %% [markdown]
# ### Mars Weather

# %%
# Visit the weather website
url = 'https://mars.nasa.gov/insight/weather/'
browser.visit(url)


# %%
# Parse the data
html = browser.html
weather_soup = soup(html, 'html.parser')


# %%
# Scrape the Daily Weather Report table
weather_table = weather_soup.find('table', class_='mb_table')
print(weather_table.prettify())

# %% [markdown]
# # D1: Scrape High-Resolution Mars’ Hemisphere Images and Titles
# %% [markdown]
# ### Hemispheres

# %%
# 1. Use browser to visit the URL
url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
browser.visit(url)


# %%
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


# %%
# 4. Print the list that holds the dictionary of each image url and title.
pprint(hemisphere_image_urls)


# %%
# 5. Quit the browser
browser.quit()


# %%


# %%
