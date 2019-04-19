def decrypt(alphabeth, word, n):
    #run through the each latter in a word by putting them into a list,
    #then looks at the index of that word in the list alphabeth
    #substruct number n, which is specified by the user in the file, and calls the calculatedindex
    #finds the calculated index in the alphabeth and then adds it to a new list, listword1 does this for every
    #letter. Turns that new list, listword1, to string
    listword1 = []
    for i in range(len(word)):
        listword = []
        listword = list(word)
        index = alphabeth.index(listword[i])
        n = n % 26 #avoids huge numbers to give error
        calculatedindex = index - n
        if calculatedindex >= len(alphabeth):
            newindex = index - n - len(alphabeth)
            listword1.append(alphabeth[newindex])
        else:
            listword1.append(alphabeth[calculatedindex])
    print(''.join(listword1))
    return
if __name__ == '__main__':
    alphabeth = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]
    filename = input("Enter the input filename: ")
    encryptedword = open(filename, "r")
    line = encryptedword.readline() #reads every line of the file
    inputlist = line.split() #splits it
    if len(inputlist) == 2:
        n = int(inputlist[0])
        word = inputlist[1]
    if len(inputlist) == 2:
        decrypt(alphabeth, word, n)
    else:
        print("missing text!")
    while line != '':
        line = encryptedword.readline() #reads every line of the file
        inputlist = line.split() #splits it
        if line == '':
            continue
        if len(inputlist) == 2:
            n = int(inputlist[0])
            word = inputlist[1]
        if len(inputlist) == 2:
            decrypt(alphabeth, word, n) #runs the file with the word, alphabeth list number of n
        else:
            print("missing text!")
    encryptedword.close()
