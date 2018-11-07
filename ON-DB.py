import csv ##csv allows me to output into csv (comma seperated value) files
from urllib.request import urlopen ##urllib allows me to open up urls successfully
from bs4 import BeautifulSoup ##this allows me to parse information from the inter
import pickle

fullList=[]
with open("OntarioDB.txt", "rb") as fp:   # Unpickling   
    b = pickle.load(fp)

print(b)