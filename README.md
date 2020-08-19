# ScrapMaps
 
Scripts to go to:

 - https://bsaber.com/songs/top/?unranked=false&time=7-days
 - https://bsaber.com/songs/top/?ranked=false&time=30-days
 - https://osu.ppy.sh/beatmapsets?s=loved
 - https://osu.ppy.sh/beatmapsets?s=ranked

They get the map info of maps in first page. Around 15 for osu!, around 20 for BeastSaber. Also they go to youtube and look for the first result of the song title + artist name.

Output goes to data/ as a .tsv, different names but same column structure. The idea is to add them manually to a google sheet to organize the data.

Using Selenium, chromedriver.
