from bs4 import BeautifulSoup
import requests
import html5lib
import glob
import re
import os.path
from nltk.stem import PorterStemmer
from lxml import html

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

    def GetText(self, path):
        soup = BeautifulSoup(open(path, encoding="utf-8", errors="surrogateescape"), 'html5lib')
        for tags in soup(['script', 'style']):
            tags.decompose()
        try:
            text = soup.html.body.get_text()
        except AttributeError as e:          #in case we fail to read the file
            return ':'
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split(" "))
        text = '\n'.join(chunk for chunk in chunks if chunk)
        return text

    def Tokenize(self):
        files = self.ListofFiles()
        stopWordList = self.ListofStopWords()
        for file in files:
            self.documentDictionary[os.path.basename(file)] = self.__docId; #Gives DocId to document
            self.__docId = self.__docId+1
            text = self.GetText(file)
            if text == ':':
                print("Failed to read DocID: ", self.__docId-1)
                continue
            tokenV1 = re.split("[^a-zA-Z0-9]", text)
            tokenV2 = [token.lower() for token in tokenV1]
            tokenV1.clear()
            #Removing stopwords
            tokenV3 = []
            for token in tokenV2:
                if token not in stopWordList:
                    tokenV3.append(token)
            tokenV2.clear()
            #porter Stemming the terms
            tokenV4 = []
            porter = PorterStemmer()
            for token in tokenV3:
                tokenV4.append(porter.stem(token))
            tokenV3.clear()









def main(arg):
    token = Token(arg)
    token.Tokenize()


main("corpus\*")

