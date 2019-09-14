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

    # We assign the directory to the class that was inputted through console
    def __init__(self, path):
        self.directory = path

    # Gets a list of all path in directory
    def ListofFiles(self):
        FilesList = []
        for file in glob.glob(self.directory):
            FilesList.append(file)
        return FilesList

    def ListofStopWords(self):
        file = open("stoplist.txt", "r")
        stopWords = file.read()
        file.close()
        return stopWords

    def GetText(self, path):
        file = open(path, encoding="utf-8", errors="surrogateescape")
        content = file.read()
        content = content[content.index('<'):]
        soup = BeautifulSoup(content, 'html5lib')
        body = soup.find("body")
        for tags in body(['script', 'style']):
            tags.decompose()
        try:
            text = body.get_text()
        except AttributeError as e:  # in case we fail to read the file
            return ':'
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split(" "))
        text = '\n'.join(chunk for chunk in chunks if chunk)
        file.close()
        return text

    def StoreTermId(self):
        file = open("termids.txt", "w+")
        for term in self.termDictionary:
            file.write(str(self.termDictionary[term]) + "\t" + str(term) + "\n")
        file.close()

    def StoreDocId(self):
        file = open("docids.txt", "w+")
        for doc in self.documentDictionary:
            file.write(str(self.documentDictionary[doc]) + "\t" + str(doc) + "\n")
        file.close()

    def Tokenize(self):
        files = self.ListofFiles()
        stopWordList = self.ListofStopWords()
        for file in files:
            self.documentDictionary[os.path.basename(file)] = self.__docId;  # Gives DocId to document
            self.__docId = self.__docId + 1
            text = self.GetText(file)
            if text == ':':
                print("Failed to read DocID: ", self.__docId - 1)
                continue
            tokenv1 = re.split("[^a-zA-Z0-9]", text)
            tokenv2 = [token.lower() for token in tokenv1]
            tokenv1.clear()
            # Removing stopwords
            tokenv3 = []
            for token in tokenv2:
                if token not in stopWordList:
                    tokenv3.append(token)
            tokenv2.clear()
            # porter Stemming the terms
            tokenv4 = []
            porter = PorterStemmer()
            for token in tokenv3:
                tokenv4.append(porter.stem(token))
            tokenv3.clear()
            for term in tokenv4:
                if (not self.termDictionary.__contains__(term)):
                    self.termDictionary[term] = self.__termId;
                    self.__termId = self.__termId + 1;
            tokenv4.clear()
        self.StoreTermId()
        self.StoreDocId()


# Class Token ends here


def main(arg):
    token = Token(arg)
    token.Tokenize()


main("corpus\*")
