
def read_index(argv):
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

read_index("age")
