#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Get Maps from BeastSaber

Using selenium, make sure to have chromedriver updated.

"""
from selenium import webdriver
import os
import time

website = "https://osu.ppy.sh/beatmapsets?s=loved"
driver = webdriver.Chrome(os.getcwd() + "/chromedriver")
tsvFile = "data/osuLoved.tsv"

def MainPage():
    time.sleep(1)
    driver.get(website)    
    #links = [i.get_attribute("href") for i in driver.find_elements_by_xpath("//a[@title]") if "songs" in i.get_attribute("href")]
    
    links = [i.get_attribute("href") for i in driver.find_elements_by_class_name("beatmapset-panel__header") if 'beatmapsets' in i.get_attribute("href")]
    links = list(dict.fromkeys(links))
    return links
        
def Categories():
    time.sleep(1)
    elem = driver.find_elements_by_class_name("beatmapset-info__header")
    
    for i in elem:
        if 'Tags' in i.text:
            parent = i.find_element_by_xpath("..")
            tags = parent.find_elements_by_tag_name("div")[0]
            links = [j.text for j in tags.find_elements_by_tag_name("a")]
            if len(links) == 0:
                return "-"
            else:  
                text = ""
                for i in links:
                    text = text + str(i) + ", "
                return text[:-2]
    
def GetYoutube(name):
    driver.get("https://www.youtube.com/results?search_query=" + name)    
    firstResult = driver.find_element_by_id("video-title").get_attribute("href")
    return firstResult

def Page(page):
    driver.get(page)
    time.sleep(1)
    song = driver.find_elements_by_class_name("beatmapset-header__details-text")[0].text
    artist = driver.find_elements_by_class_name("beatmapset-header__details-text")[1].text
    mapper = driver.find_element_by_class_name("beatmapset-mapping__user").get_attribute("href")
    
    categories = Categories()
    stream = GetYoutube(song)

    Row(song + " " + artist, mapper, categories, stream, page)
    
    
def Row(song, mapper, categories, stream, page):
    text = str(song) + "\t - \t" + str(stream) + "\t" + str(categories) + "\t" 
    text = text + "\t" + str(page) + "\t" + str(mapper) + "\n"
    
    with open(tsvFile, "r") as file:
        base = file.read()
    with open(tsvFile, "w+") as file:
        file.write(base + text)


# Create/rewrites the file
header = "Song \t Genre \t Stream \t Tags \t Score \t Map \t Mapper \n"
with open(tsvFile, "w+") as file:
    file.write(header)

# Save 
links = MainPage()
for i in links:
    Page(i)
    
print("\nDone :)")



