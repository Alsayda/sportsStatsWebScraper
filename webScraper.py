import requests
import pandas as pd
from bs4 import BeautifulSoup
import inspect
from abc import ABC, abstractmethod 


"""
statsTableHeaders = statsTable.findAll("th")
headerNames = []
for header in statsTableHeaders:
    headerNames.append(header.text)
#print(headerNames)
"""
class statsScraper(ABC):
    _STR_BASEBALL = "Baseball"
    _STR_BASKETBALL = "Basketball"
    
    def __init__(self, urlStats, teamAbreviations, urlExtension) -> None:
        self._urlStats = urlStats
        self._teamAbreviations = teamAbreviations
        self._urlExtension = urlExtension
                
    def _getSoupTeamStats(self, city, year):
        url = ""
        url = url + self._urlStats
        url = url + "/teams/"
        url = url + self._teamAbreviations[city]
        url = url + f"/{year}"
        url = url + self._urlExtension 
    
        r = requests.get(url)
        #print(r)
        soup = BeautifulSoup(r.text, "html.parser")
        return soup
    
    @classmethod
    def _raiseErrorInvalidArg(nameOfEnclosingFunc):
        raise ValueError(f"argument provided to function '{nameOfEnclosingFunc}'' invalid")

class baseballStatsScraper(statsScraper):
    def __init__(self):
        urlStats = "https://www.baseball-reference.com"
        teamAbreviations = dict([
            ("Baltimore", "BAL"),
            ("Texas", "TEX")
        ])
        urlExtension = ".shtml"
        super().__init__(urlStats, teamAbreviations, urlExtension)

    def getBaseballTeamPitcherStats(self, city, year):
        soup = self._getSoupTeamStats(city, year)
        statsTable = soup.find("table", id="team_batting")
        pitchersRows = []  
        statsTableRows = statsTable.findAll("tr")
        for row in statsTableRows[1:]:
            try:
                pos = row.find("td")
                #print(pos.string)
                if(pos.string == "P"):
                    pitchersRows.append(row)
            except AttributeError:
                pass
        
        pitchersStats = []
        for pitcher in pitchersRows:
            tempPitcher = ()
            name = pitcher.find("td",{'data-stat':'player'})
            tempPitcher = (*tempPitcher, name.text)
            #print(pitcherName.text) 
            age = pitcher.find("td",{'data-stat':'age'})
            tempPitcher = (*tempPitcher, age.text)
            games = pitcher.find("td",{'data-stat':'G'})
            tempPitcher = (*tempPitcher, games.text)
            pitchersStats.append(tempPitcher)
        """
        for pitcher in pitchersStats:
            print(pitcher)
        """
        return pitchersStats

class basketballStatsScraper(statsScraper):
    def __init__(self):
        urlStats = "https://www.basketball-reference.com"
        teamAbreviations = dict(
            ("Boston", "BOS"),
            ("Philadelphia", "PHI")
        )
        urlExtension = ".html"
        super().__init__(urlStats, teamAbreviations, urlExtension)

        