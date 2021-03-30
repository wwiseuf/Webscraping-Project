from bs4 import BeautifulSoup
import requests
import pandas as pd
from splinter import Browser
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo

# Create an instance of Flask
app = Flask(__name__)

# Use PyMongo to establish Mongo connection
mongo = PyMongo(app, uri="mongodb://localhost:27017/???????")



def scrape_mars():
    # set up splitter
    executable_path = {'executable_path' : ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=True)

    url = "https://mars.nasa.gov/news/"

    #retreive page with request
    response = requests.get(url)

    soup = BeautifulSoup(response.text, 'html.parser')

    news_title = soup.find("div",class_="content_title").text.strip()
    news_p = soup.find('div',class_="rollover_description_inner").text.strip()


    url = "https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html"
    browser.visit(url)
    html = browser.html
    img_soup = BeautifulSoup(html, 'html.oarser')
    urlb = img_soup.find('img', class_='headerimage')['src']
    featured_image_url = f'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/{urlb}'

    url = "https://space-facts.com/mars/"
    facts_table = pd.read_html(url)[0].to_html()