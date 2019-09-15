import sys

#My terminal ran it as python read_index.py and givrs error at ./read_index.py so its designed for that

def read_index():
    if sys.argv.__len__() < 2:
        print("Insufficient arguments")

    argv = sys.argv[1]
    file1 = open("termids.txt","r")
    list = file1.read()
    index = -1

    for word in list.split():
        if(word == argv):
            break
        index = word

    id = int(index)

    file2 = open("term_index.txt","r")
    lines = file2.readlines()

    info = []
    for value in lines[id].split(' '):
        info.append(value)

    print("Listing for term: ", argv)
    print("TERMID: ", id)
    print("Number of documents containing term:", info[2] )
    print("Term frequency in corpus: ", info[1])

read_index()
