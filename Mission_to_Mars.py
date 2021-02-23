# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
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
# Find the relative image url
img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
img_url_rel


# %%
# Use the base URL to create and absolute URL
img_url = f'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/{img_url_rel}'
img_url


# %%
df = pd.read_html('https://space-facts.com/mars/')[0]
df.columns = ['Description', 'Mars']
df.set_index('Description', inplace=True)
df


# %%
df.to_html()


# %%
browser.quit()


# %%
