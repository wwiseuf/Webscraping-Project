from bs4 import BeautifulSoup
import requests
import pandas as pandas

from splinter import Browser
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

def scrape_mars():
    # Set up Splinter
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=True)

    url = "https://mars.nasa.gov/news/"
    # Retrieve page with the requests module
    response = requests.get(url)
    # Create BeautifulSoup object; parse with 'html.parser'
    soup = BeautifulSoup(response.text, 'html.parser')

    news_title = soup.find("div",class_="content_title").text.strip()
    news_p = soup.find("div",class_="rollover_description_inner").text.strip()

    url = "https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html"
    browser.visit(url)
    html = browser.html
    img_soup = BeautifulSoup(html, 'html.parser')
    urlb = img_soup.find('img', class_="headerimage")['src']
    featured_img_url = f"https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/{urlb}"

    url = "https://space-facts.com/mars/"
    facts_table = pd.read_html(url)[0].to_html()

    url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&vs=Mars"
    browser.visit(url)
    html = browser.html
    hemi_soup = BeautifulSoup(html, 'html.parser')
    banners_tag = hemi_soup.find_all('h3')
    banners = [x.text for x in banners_tag]
    url = url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&vs=Mars"

    hemispheres = []
    for i in range(len(banners)):
        hemisphere = {}
        browser.visit(url)
        browser.find_by_css('h3')[i].click()

        hemisphere["title"] = [banners[i]]
        hemisphere["img_url"] = browser.find_by_text('Sample')['href']

        hemispheres.append(hemisphere)
        browser.back()

    # Store data in a dictionary
    mars_data = {
        "news_title": news_title,
        "news_p": news_p,
        "featured_image_url": featured_image_url,
        "facts_table":facts_table,
        "hemispheres":hemispheres
    }

    # Quit the browser after scraping
    browser.quit()