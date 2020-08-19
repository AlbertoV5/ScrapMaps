#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Get Maps from osu! website.
Using selenium with chromedriver on script path.
"""
from selenium import webdriver
from pathlib import Path
import pandas as pd
import time

website = "https://osu.ppy.sh/beatmapsets?s=loved"
driver = webdriver.Chrome(Path.cwd() / "chromedriver")
tsvFile = Path.cwd() / "data" / "osuLoved.tsv"

def MainPage():
    time.sleep(2)
    driver.get(website)        
    links = [i.get_attribute("href") for i in driver.find_elements_by_class_name("beatmapset-panel__header") if 'beatmapsets' in i.get_attribute("href")]
    return list(dict.fromkeys(links))
        
def Single(webpage):
    driver.get(webpage)
    time.sleep(2)
    
    songName = driver.find_elements_by_class_name("beatmapset-header__details-text")[0].text 
    artist = driver.find_elements_by_class_name("beatmapset-header__details-text")[1].text
    mapper = driver.find_element_by_class_name("beatmapset-mapping__user").get_attribute("href")
    genre = driver.find_element_by_class_name("beatmapset-info__half-entry").find_element_by_tag_name("a").text
    tags = GetTags()
    song = songName + " " + artist

    return pd.DataFrame({"Song": [song], "Genre": [genre], "Youtube": [GetYoutube(song)], 
                         "Tags": [tags], "Map": [webpage], "Mapper": [mapper]})

def GetTags(webpage):
    for i in driver.find_elements_by_class_name("beatmapset-info__header"):
        if 'Tags' in i.text:
            parent = i.find_element_by_xpath("..")
            tags = [j.text for j in parent.find_elements_by_tag_name("div")[0].find_elements_by_tag_name("a")]
            if len(tags) == 0:
                return "-"
            else:  
                tagsString = ""
                for i in tags:
                    tagsString = tagsString + str(i) + ", "    
                return tagsString[:-2]
    
def GetYoutube(song):
    driver.get("https://www.youtube.com/results?search_query=" + song)    
    return driver.find_element_by_id("video-title").get_attribute("href")
    
# Header TSV
sheet = pd.DataFrame({"Song" : [], "Genre": [], "Youtube": [], "Tags": [], "Map": [], "Mapper": []})
for page in MainPage():
    sheet = sheet.append(Single(page))
    
sheet.to_csv(tsvFile, sep = "\t", index = False)

print("\nDone :)")
