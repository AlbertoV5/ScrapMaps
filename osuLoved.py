#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Get Maps from BeastSaber

Using selenium, make sure to have chromedriver updated.

"""
from selenium import webdriver
import os

website = "https://osu.ppy.sh/beatmapsets?s=ranked"
driver = webdriver.Chrome(os.getcwd() + "/chromedriver")
tsvFile = "data/osuRanked.tsv"

def MainPage():
    driver.get(website)    
    links = [i.get_attribute("href") for i in driver.find_elements_by_xpath("//a[@title]") if "songs" in i.get_attribute("href")]
    links = list(dict.fromkeys(links))
    text = ""
    for i in links:
        text = text + i + "\n"
    with open("links.txt", "w+") as file:
        file.write(text)
    return links
        
def Categories():
    div = driver.find_element_by_class_name("bsaber-categories")
    links = [i.text for i in div.find_elements_by_tag_name("a")]
    if len(links) == 0:
        return "-"
    else:  
        text = ""
        for i in links:
            text = text + str(i) + ", "
        return text[:-2]

def Mapper():
    for i in driver.find_elements_by_css_selector("a"):
        try:
            href = i.get_attribute("href")
            if "/tag/" in href:
                return href
        except:
            pass

def GetScore():
    thumbs = driver.find_elements_by_class_name("post-stat")
    numbers = []
    for i in thumbs:
        try:
            numbers.append(int(i.text))
        except:
            pass
    return numbers

def iFrame():
    try:
        return driver.find_element_by_tag_name("iframe").get_attribute("src")
    except:
        return "No youtube link"
    
def GetYoutube(name):
    driver.get("https://www.youtube.com/results?search_query=" + name)    
    firstResult = driver.find_element_by_id("video-title").get_attribute("href")
    return firstResult
    
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

def Page(page):
    print(page)
    driver.get(page)
    song = driver.find_element_by_class_name("entry-title").text
    mapper = Mapper()
    categories = Categories()
    scores = GetScore() 
    days = GetDate()
    stream = GetYoutube(song)
    
    Row(song, mapper, categories, scores, stream, days, page)
    
    
def Row(song, mapper, categories, scores, stream, days, page):
    #ratio = str(int(scores[0]-scores[1]/days))
    #ratio formula for excel/sheet
    ratio = "=(" + str(scores[0]) + "-" + str(scores[1]) + ")/" + str(days) 
    text = str(song) + "\t - \t" + str(stream) + "\t" + str(categories) + "\t" 
    text = text + ratio + "\t" + str(page) + "\t" + str(mapper) + "\n"
    
    with open(tsvFile, "r") as file:
        base = file.read()
    with open(tsvFile, "w+") as file:
        file.write(base + text)


# Create/rewrites the file
header = "Song \t Genre \t Stream \t Tags \t Likes/Days \t Map \t Mapper \n"
with open(tsvFile, "w+") as file:
    file.write(header)

# Save 
links = MainPage()
for i in links:
    Page(i)
    
print("\nDone :)")



