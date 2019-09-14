from bs4 import BeautifulSoup
import requests
import html5lib
import glob
import re
import os.path
from nltk.stem import PorterStemmer

class Token:
    directory = ""
    __termId = 0
    __docId = 0
    termDictionary = {}
    documentDictionary = {}

    #We assign the directory to the class that was inputted through console
    def __init__(self, path):
        self.directory = path

    #Gets a list of all path in directory
    def ListofFiles(self):
        FilesList = []
        for file in glob.glob(self.directory):
            FilesList.append(file)
        return FilesList

    def ListofStopWords(self):
        file = open("stoplist.txt", "r")
        stopWords = file.read()
        return stopWords

    def Tokenize(self):
        files = self.ListofFiles()
        stopWordList = self.ListofStopWords()







def main(arg):
    token = Token(arg)
    token.Tokenize()


main("corpus\*")

