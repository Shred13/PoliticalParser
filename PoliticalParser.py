# -*- coding: utf-8 -*-
##Comments for clarity

##the below code is for importing necessary libraries and tools
from urllib.request import urlopen ##urllib allows me to open up urls successfully
from bs4 import BeautifulSoup ##this allows me to parse information from the internet
## import re ##re allows me to use regex on the output
##import csv ##csv allows me to output into csv (comma seperated value) files 
import pickle


x=5

nameCareer = [] ##this is going to be the final list that I work with which should have all my infromation


parliamentaryList = []
for lister in range (42):
    parliamentaryList.append([])
    parliamentaryList[lister].insert(0, str(lister+1))
##lowercaseLetters = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
##^^ the above array is used to quickly traverse the ontario website and see all the MPPs in history
##for c in lowercaseLetters:
    url = "https://www.ola.org/en/members/parliament-"+str(lister+1)
    ##^^as you can see, the ola website is sectioned off by last names, and so I can use this for loop to quickly go through it
    
    uClient = urlopen(url)
    ##open up the urls
    content = uClient.read()
    ##read the urls
    uClient.close()
    ##close the urls
    
    soup = BeautifulSoup(content, 'html.parser')
    ##create an obeject that sees the link that is to be read and then parses its html
    
    findName = soup.findAll("td", {"class":"views-field views-field-field-full-name-by-last-name"})
    ##this is to find the names and links of all the MPPs and their profiles. td is a part of the table and the class is where the names are
    
    urlList = []
    ##this list is to traverse every single link to every MPP's profile
    for name in findName:
        nameString = str(name.a["href"])
        ##make the href link a string value which can then be used  
        urlList.append("https://www.ola.org" + nameString)
    
    for urls in urlList:
        uClient = urlopen(urls)
        MPPContent = uClient.read()
        uClient.close()
        soupMPP = BeautifulSoup(MPPContent, 'html.parser')
    ##do the similar thing except with all the links now
        try:
            findCareer = soupMPP.findAll("div",{"class":"views-field views-field-nothing"})
            ##for the current Ministers, the structure is different so the above try is to do it for former Ministers
        except:
            findCareer = soupMPP.findAll("div",{"class":"views-element-container block block-views block-views-blockmember-block-2"})
        ##this one is for the current ones
        
        ##these are also used to find all the Careers that the different MPPs had.
        CareerList = []
        ##list of all the careers people had
        theName = (soupMPP.find("span", {"class" : "views-field views-field-field-current-riding"}))
        ##this is to get the names of all the MPPs
        nameFinal = str(theName.h1.text)
        for Career in findCareer:
            try:
                CareerType = str(Career.p.text)
            except:
                CareerType = str(Career.text)
            ##above try and catch just to make the positions into strings because it is slightly different
            CareerList.append(CareerType)
            
    
        positions = []
        ##the array i am going to use to store all of the positions people hold
        for aCareer in CareerList:
            checkCareer = aCareer.split(" ")
            ##split the careers by the space in order to filter out everything that is not a Premier or Minister.
            for theCareer in checkCareer:
                if ("Premier" == theCareer or "Minister" == theCareer or "Treasurer" == theCareer) and checkCareer[0] != "Parliamentary":
                    ##filters out for parliamentary assisstants this way as well, though a few did get in eventually
                    word = aCareer.replace("\n", "").replace("–", "").replace("January", "").replace("February", "").replace("March", "").replace("April", "").replace("May", "").replace("June", "").replace("July", "").replace("August", "").replace("September", "").replace("October", "").replace("November", "").replace("December", "")
                    ##only wanted the years for the beginning and ending of their terms, not the months
                  ##  word = re.sub(r'\s\s\d?\d', "", word)
                    ##nor for the dates as well (regex looking for space, space and two digits)
                    positions.append(word)    
        if len(positions) != 0:
            ##if the length of positions is not zero, meaning they had a position at one point
           ## positions.insert(0, nameFinal)
            ##add the names to the beginning of the list
           ## positions.insert(0, urls)
            ##add the url to the beginning of the list for further parsing
            parliamentaryList[lister].insert(0, urls)          
            ##new list with the lists that made it

    print(lister+1)
    ##print the char we just finished for this entire process as a mini loading bar type deal
 ##use nameCareer and print it out nicely into a textfile for further use, need to delete the \n and only keep the years
##also need to delete dashes   



with open("OntarioDB.txt", "wb") as fp:   #Pickling
    pickle.dump(parliamentaryList, fp)


# =============================================================================
# 
# with open('OntarioDataBase.csv', 'w') as csvfile:
#     ##write a csv file
#     writer = csv.writer(csvfile, delimiter = ",")
#     ##with ',' in between the elements
#     for theCareers in parliamentaryList:
#         writer.writerow(theCareers)
#         ##write a row in the document of just the lists
# =============================================================================
print("hello")
##print hello to signify ending of the program



