#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Get Maps from BeastSaber website.
Using selenium with chromedriver on script path.

Unranked BS 7 days

"""
from selenium import webdriver
from pathlib import Path
import pandas as pd
import time

website = "https://bsaber.com/songs/top/?unranked=false&time=7-days"
driver = webdriver.Chrome(Path.cwd() / "chromedriver")
tsvFile = Path.cwd() / "data" / "beatsaberUnranked.tsv"

def MainPage():
    driver.get(website)    
    links = [i.get_attribute("href") for i in driver.find_elements_by_xpath("//a[@title]") if "songs" in i.get_attribute("href")]
    return list(dict.fromkeys(links))
        
def GetTags():
    div = driver.find_element_by_class_name("bsaber-categories")
    tags = [i.text for i in div.find_elements_by_tag_name("a")]
    if len(tags) == 0:
        return "-"
    else:  
        tagsString = ""
        for i in tags:
            tagsString = tagsString + str(i) + ", "
        return tagsString[:-2]

def GetMapper():
    for i in driver.find_elements_by_css_selector("a"):
        try:
            href = i.get_attribute("href")
            if "/tag/" in href:
                return href
        except:
            pass
        
def GetScore(): # returns [num of likes, num of dislikes]
    thumbs = driver.find_elements_by_class_name("post-stat")
    numbers = []
    for i in thumbs:
        try:
            numbers.append(int(i.text))
        except:
            pass
    return numbers 

def GetYoutube(song):
    driver.get("https://www.youtube.com/results?search_query=" + song)    
    return driver.find_element_by_id("video-title").get_attribute("href")
    
def GetDate():
    date = driver.find_element_by_tag_name("time").text
    if "day" in date:
        num = int(date.split(" ")[0]) * 1
    elif "week" in date:
        num = int(date.split(" ")[0]) * 7
    elif "month" in date:
        num = int(date.split(" ")[0]) * 30
    elif "hour" in date:
        num = int(date.split(" ")[0]) / 24
    return num

def Single(webpage):
    driver.get(webpage)
    time.sleep(1)
    
    song = driver.find_element_by_class_name("entry-title").text
    scores = GetScore() 
    scoreRatio = "=(" + str(scores[0]) + "-" + str(scores[1]) + ")/" + str(GetDate()) # excel formula
    tags = GetTags()
    mapper = GetMapper()
    
    # Beast Saber doesnt include song genre info, has to be input manually, listening to the song
    return pd.DataFrame({"Song": [song], "Genre": ["-"], "Youtube": [GetYoutube(song)], 
                         "Tags": [tags], "Map": [webpage], "Mapper": [mapper], "Likes/Days":[scoreRatio]})

# Save 
sheet = pd.DataFrame({"Song" : [], "Genre": [], "Youtube": [], "Tags": [], "Map": [], "Mapper": [], "Likes/Days": []})

for page in MainPage():
    sheet = sheet.append(Single(page))
    
sheet.to_csv(tsvFile, sep = "\t", index = False)
    
print("\nDone :)")


