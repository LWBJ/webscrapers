from calendar import isleap
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from time import sleep
import pandas as pd

class BandLeader():
    def __init__(self):
        options = Options()
        options.headless = True
        self.driver = webdriver.Firefox(options=options)
        self.driver.implicitly_wait(10)
        self.driver.get('https://bandcamp.com')
        sleep(1)

        self.trackList = []
        self.currentTrackNo = 1
        self.database = self.loadDB()
        #self.database = pd.DataFrame()

        self.getTracks()
    
    def getTracks(self):
        sleep(1)
        currentTracks = self.driver.find_element(By.CSS_SELECTOR, '.row.discover-result.result-current')
        self.trackList = currentTracks.find_elements(By.CSS_SELECTOR, '.col.col-3-12.discover-item')
        #print tracks to screen
        for (i,track) in enumerate(self.trackList):
            print('[{}]'.format(i+1))
            lines = track.text.split('\n')
            print('Album  : {}'.format(lines[0]))
            print('Artist : {}'.format(lines[1]))
            if len(lines) > 2:
                print('Genre  : {}'.format(lines[2]))

    def getPages(self):
        navButtons = self.driver.find_elements(By.CLASS_NAME, 'item-page')
        print('PAGES')
        for button in navButtons:
            print(button.text)
        print()

    def nextPage(self):
        navButtons = self.driver.find_elements(By.CLASS_NAME, 'item-page')
        for button in navButtons:
            if button.text == 'next':
                nextButton = button
        if (nextButton):
            nextButton.click()
            self.getTracks() 

    def play(self, track=None):
        if track is None:
            playButton = self.driver.find_element(By.CLASS_NAME, 'playbutton')
            playButton.click()
        elif type(track) is int and track <= len(self.trackList) and track >=1:
            self.currentTrackNo = track
            self.trackList[track-1].click()

        sleep(0.5)
        if self.isPlaying():
            self.currentlyPlayingTrack = self.getCurrentlyPlayingTrack()
            print('Now playing: {}'.format(self.currentlyPlayingTrack))
            print()
            self.updateDB()

    def playNext(self):
        if self.currentTrackNo < len(self.trackList):
            self.play(self.currentTrackNo + 1)
        else:
            self.nextPage()
            self.play(1)

    def pause(self):
        self.play()

    def isPlaying(self):
        playButton = self.driver.find_element(By.CLASS_NAME, 'playbutton')
        return playButton.get_attribute('class').find('playing') > -1

    def getCurrentlyPlayingTrack(self):
        try:
            if self.isPlaying():
                title = self.driver.find_element(By.CSS_SELECTOR, 'span.title').text
                albumDetail = self.driver.find_element(By.CLASS_NAME, 'detail-album').find_element(By.TAG_NAME, 'a')
                albumTitle = albumDetail.text
                albumURL = albumDetail.get_attribute('href').split('?')[0]
                artistDetail = self.driver.find_element(By.CLASS_NAME, 'detail-artist').find_element(By.TAG_NAME, 'a')
                artist = artistDetail.text
                artistURL = artistDetail.get_attribute('href').split('?')[0]
                return (title, albumTitle, albumURL, artist, artistURL)
        except Exception as e:
            print('Error: {}'.format(e))

        return None

    def loadDB(self):
        try:
            df = pd.read_csv('database.csv')
            return list(df.itertuples(index=False, name=None))
        except:
            return [] 

    def updateDB(self):
        check = self.currentlyPlayingTrack is not None and (len(self.database)==0 or self.currentlyPlayingTrack is not self.database[len(self.database)-1])
        if check:
            self.database.append(self.currentlyPlayingTrack)

    def saveDB(self):
        data = pd.DataFrame(self.database, columns=['Title','Album','Album URL','Artist','Artist URL'])
        data.to_csv('database.csv', index=False)
    

bl = BandLeader()
playOrder = [7,8]
for i in playOrder:
    bl.play(i)
    sleep(1)
bl.saveDB() 