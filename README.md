# ScrapMaps
 
Scripts to go to:

 - https://bsaber.com/songs/top/?unranked=false&time=7-days
 - https://bsaber.com/songs/top/?ranked=false&time=30-days
 - https://osu.ppy.sh/beatmapsets?s=loved
 - https://osu.ppy.sh/beatmapsets?s=ranked

They get the info of maps in first page, then go to youtube and look for the first result of the song title + artist name. Output goes to data folder as a tsv. 

### What is done manually:
- Organize tsv files by dates (when the scrapping was done).
- Add the results to a google sheet in order to organize and review the data.

Using Selenium, chromedriver.
