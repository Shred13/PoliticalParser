# -*- coding: utf-8 -*-

from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
import csv

nameCareer = []
lowercaseLetters = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
for c in lowercaseLetters:
    url = "https://www.ola.org/en/members/last-name/" + c
    ##url = "https://www.ola.org/en/members/last-name/e"
    
    uClient = urlopen(url)
    content = uClient.read()
    uClient.close()
    
    soup = BeautifulSoup(content, 'html.parser')
    
    findName = soup.findAll("td", {"class":"views-field views-field-field-full-name-by-last-name is-active"})
    
    urlList = []
    for name in findName:
        nameString = str(name.a["href"])
        urlList.append("https://www.ola.org" + nameString)
    
    for urls in urlList:
        uClient = urlopen(urls)
        MPPContent = uClient.read()
        uClient.close()
        soupMPP = BeautifulSoup(MPPContent, 'html.parser')
    
        try:
            findCareer = soupMPP.findAll("div",{"class":"views-field views-field-nothing"})
        except:
            findCareer = soupMPP.findAll("div",{"class":"views-element-container block block-views block-views-blockmember-block-2"})
        
        CareerList = []
        theName = (soupMPP.find("span", {"class" : "views-field views-field-field-current-riding"}))
        nameFinal = str(theName.h1.text)
        for Career in findCareer:
            try:
                CareerType = str(Career.p.text)
            except:
                CareerType = str(Career.text)
            CareerList.append(CareerType)
            
    
        positions = []
        for aCareer in CareerList:
            checkCareer = aCareer.split(" ")
            for theCareer in checkCareer:
                if "Premier" == theCareer or "Minister" == theCareer and checkCareer[0] != "Parliamentary":
                    word = aCareer.replace("\n", "").replace("–", "").replace("January", "").replace("February", "").replace("March", "").replace("April", "").replace("May", "").replace("June", "").replace("July", "").replace("August", "").replace("September", "").replace("October", "").replace("November", "").replace("December", "")
                    word = re.sub(r'\s\s\d?\d', "", word)
                    positions.append(word)    
        if len(positions) != 0:
            positions.insert(0, nameFinal)
            positions.insert(0, urls)
            nameCareer.append(positions)          

    print(c)
    
 ##use nameCareer and print it out nicely into a textfile for further use, need to delete the \n and only keep the years
##also need to delete dashes   

with open('OntarioDataBase.csv', 'w') as csvfile:
    writer = csv.writer(csvfile, delimiter = ",")
    for theCareers in nameCareer:
        writer.writerow(theCareers)
print("hello")



