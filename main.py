from bs4 import BeautifulSoup
import html5lib
import glob
import re
import os.path
from nltk.stem import PorterStemmer
import sys

#My terminal ran it as python main.py and givrs error at ./main.py so its designed for that
#Directory name should end with a '\' like 'Corpus\'


class Token:
    directory = ""
    __termId = 0
    __docId = 0
    termDictionary = {}
    documentDictionary = {}

    # We assign the directory to the class that was inputted through console
    def __init__(self, path):
        self.directory = path + "*"

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

    def ReduceToken(self, text, stopWordList):
        tokenv1 = re.split("[^a-zA-Z]", text)
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
        return tokenv4

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
            stemmedtext = self.ReduceToken(text, stopWordList)
            for term in stemmedtext:
                if not self.termDictionary.__contains__(term):
                    self.termDictionary[term] = self.__termId
                    self.__termId = self.__termId + 1
            stemmedtext.clear()
        self.StoreTermId()
        self.StoreDocId()

# Class Token ends here

class InvertedIndexHash:
    Dictionary = {}
    termFrequencyList = {}
    docFrequencyList = {}
    termDict = {}
    docDict = {}
    token = object

    def __init__(self, token):
        self.token = token
        self.termDict = token.termDictionary
        self.docDict = token.documentDictionary
        self.InitializeFrequencyList()

    def InitializeFrequencyList(self):
        for term in self.termDict:
            self.termFrequencyList[term] = 0
            self.docFrequencyList[term] = 0
            self.Dictionary[term] = []

    def MakeList(self):
        FilesList = self.token.ListofFiles()
        Stopwords = self.token.ListofStopWords()
        for file in FilesList:
            text = self.token.GetText(file)
            if text == ':':
                print("Failed to open")
                continue
            stemmedtext = self.token.ReduceToken(text, Stopwords)
            filename = os.path.basename(file)
            docID = self.docDict[filename]
            position = 1
            WordinDoc = []
            for word in stemmedtext:
                self.termFrequencyList[word] += 1
                if word not in WordinDoc:
                    WordinDoc.append(word)
                    self.docFrequencyList[word] += 1
                self.Dictionary[word].append((docID, position))
                position += 1
            WordinDoc.clear()

    def SavetoFile(self):
        file = open("term_index.txt", "w+")
        for term in self.termDict:
            file.write(str(self.termDict[term]) + " " + str(self.termFrequencyList[term]) + " "  + str(self.docFrequencyList[term]))
            previous_doc = 0
            previous_position = 0
            for docId,position in self.Dictionary[term]:
                if docId == previous_doc:
                    file.write(" " + str(docId - previous_doc) + "," + str(position - previous_position))
                    previous_position = position
                else:
                    file.write(" " + str(docId - previous_doc) + "," + str(position))
                    previous_position = position
                    previous_doc = docId
            file.write('\n')
        file.close()


 #End of class InvertedIndexHash
class InvertedIndexNoHash:
    List = []
    termDict = {}
    docDict = {}
    token = object

    def __init__(self, token):
        self.token = token
        self.termDict = token.termDictionary
        self.docDict = token.documentDictionary

    def MakeList(self):
        FilesList = self.token.ListofFiles()
        Stopwords = self.token.ListofStopWords()
        for file in FilesList:
            text = self.token.GetText(file)
            if text == ':':
                print("Failed to open")
                continue
            stemmedtext = self.token.ReduceToken(text, Stopwords)
            filename = os.path.basename(file)
            docID = self.docDict[filename]
            position = 1
            for word in stemmedtext:
                self.List.append((self.termDict[word], docID, position))
                position += 1
        self.List.sort()

        

    def SavetoFile(self):
        file = open("term_index_no_hash.txt", "w+")
        previous_term = -1
        previous_doc = 0
        term_count = 0
        previous_position = 0
        doc_count = 0
        temp_list = []
        for tuple in self.List:
            if previous_term == -1:
                previous_term = tuple[0]
                term_count += 1
                previous_doc = tuple[1]
                doc_count += 1
                previous_position = tuple[2]
                temp_list.append((tuple[1], tuple[2]))
            elif tuple[0] == previous_term:
                term_count +=1
                if previous_doc != tuple[1]:
                    doc_count += 1
                    temp_list.append((tuple[1] - previous_doc, tuple[2]))
                    previous_doc = tuple[1]
                    previous_position = tuple[2]
                else:
                    temp_list.append((tuple[1] - previous_doc, tuple[2] - previous_position))
                    previous_position = tuple[2]
            else:
                file.write(str(previous_term) + " " + str(term_count) + " " + str(doc_count))
                for record in temp_list:
                    file.write(" " + str(record[0]) + "," + str(record[1]))
                file.write("\n")
                temp_list = []
                doc_count = 0
                term_count = 0
                previous_term = tuple[0]
                temp_list.append((tuple[1] - previous_doc, tuple[2]))
                term_count += 1
                previous_doc = tuple[1]
                doc_count += 1
                previous_position = tuple[2]
        file.close()

#end of InvertedIndexNoHash

def main():
    if sys.argv.__len__() < 2:
        print("Insufficient arguments")

    arg = sys.argv[1]
    print("Tokenizing the document")
    token = Token(arg)
    token.Tokenize()

    print("Making term index without hashmap")
    NoHash = InvertedIndexNoHash(token)
    NoHash.MakeList()
    NoHash.SavetoFile()

    print("Making term index hashmap")
    Hash = InvertedIndexHash(token)
    Hash.MakeList()
    Hash.SavetoFile()

main()
