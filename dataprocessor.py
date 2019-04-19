def paymentsdict(payments):
    #gets the payments file and reads line by line while splitting and appending
    #to listes according to correct format and creates a dictionary called
    #paymentsdict which has phone numbers in the string format as key
    #and every date and payment made in that date as value.
    paymentsdict = dict()
    line = payments.readline()
    linelist = line.split(';')
    list1 = []
    list = []
    list1.append(float(linelist[1]))
    list1.append(linelist[0])
    list.append(list1)
    paymentsdict[linelist[2][:10]] = list
    while line != '':
        line = payments.readline()
        linelist = line.split(';')
        list1 = []
        list = []
        if len(linelist) == 3:
            list1.append(float(linelist[1]))
            list1.append(linelist[0])
            list.append(list1)
            if linelist[2][:10] in paymentsdict:
                paymentsdict[linelist[2][:10]].append(list1)
            else:
                paymentsdict[linelist[2][:10]] = list
    #we get all of these payments of each number and add them up to paymentsum
    #list then we get the sum of that list and add it to paymentsumdict
    paymentsumdict = dict()
    for key, values in paymentsdict.items():
        paymentsum = []
        for i in range(len(values)):
            paymentsum.append(values[i][0])
        paymentsumdict[key] = sum(paymentsum)
    #gets the dates and payments made and puts them in proper string format
    #for to put into the table
    paymentstrdict = dict()
    for key, values in paymentsdict.items():
        strlist = []
        for i in range(len(values)):
            strlist.append("%s ($%.2f);"%(values[i][1], values[i][0]))
        strpayment = " ".join(strlist)
        paymentstrdict[key] = strpayment
    return paymentsdict, paymentsumdict, paymentstrdict

def duesdict(dues):
    #it calls dues file which is read line by line and split, and then put into
    #a list. We are adding these list to a dictionary with phone number in string
    #format as a key and the dues as value.
    duesdict = dict()
    line = dues.readline()
    linelist = line.split(';')
    totaldues = []
    list1 = []
    list1.append(float(linelist[1]))
    duesdict[linelist[2][:10]] = list1
    while line != '':
        line = dues.readline()
        linelist = line.split(';')
        list = []
        if len(linelist) == 3:
            list.append(float(linelist[1]))
            if linelist[2][:10] in duesdict:
                duesdict[linelist[2][:10]].append(float(linelist[1]))
            else:
                duesdict[linelist[2][:10]] = list
    #gets the values of the dictionary and sums them up and overrides to the same
    #dictionary again. Also adds the sum of dues in a list called total dues so
    #that later we can just do sum(totaldues) to get the total dues
    for key, value in duesdict.items():
        values = sum(value)
        totaldues.append(values)
        duesdict[key] = values
    return duesdict, totaldues

def numbernamedict(families, duesdict, paymentsumdict):
    #this function looks into families file, which was called later, and
    #reads line by line. After getting each line it splits it and puts into
    #a dictionary, paymentsdict. In this dictionary, key value is the telephone
    #numbers as string and the equavelent names as value.
    numbernamedict = dict()
    namelist = []
    numberlist = []
    numberliststr = []
    line = families.readline()
    linelist = line.split(',')
    numbernamedict[linelist[0]] = linelist[1]
    numberlist.append(linelist[0])
    while line != '':
        line = families.readline()
        linelist = line.split(',')
        if len(linelist) == 3:
            numberlist.append(linelist[0])
            numbernamedict[linelist[0]] = linelist[1]
    #creates a list called numberlist, which just includes the numbers in the
    #string format. So, in order to sort the phone numbers, we turn every phone
    #number into intiger from string format and then we sort the list. After
    #we sort the list we turn it into string again so that we can use together
    #with other dictionaries and also create another list called numberliststr
    #and format that list in the wanted format.
    for i in range(len(numberlist)):
        numberlist[i] = int(numberlist[i])
    numberlist = sorted(numberlist)
    for i in range(len(numberlist)):
        numberlist[i] = str(numberlist[i])
        numberliststr.append("(" + str(numberlist[i][:3]) + ") " + str(numberlist[i][3:6]) + " " + str(numberlist[i][6:]))
    #we are checking if each numberlist elements are in duesdict and paymentsumdict
    #and if each numberlist elements are in duesdict but not in paymentsum
    #then we are checking if due, the addition of dues and interest.
    #If the due is equal or bigger than 500 we add ** to the string.
    for i in range(len(duesdict)):
        if numberlist[i] in duesdict:
            if numberlist[i] in paymentsumdict:
                due = duesdict[numberlist[i]] - paymentsumdict[numberlist[i]]
                interest = float(due / 100)
                due = due + interest
                if due >= 500:
                    numbernamedict[numberlist[i]] = "**" + numbernamedict[numberlist[i]]
    for i in range(len(duesdict)):
        if numberlist[i] in duesdict:
            if numberlist[i] not in paymentsumdict:
                due = duesdict[numberlist[i]]
                interest = float(due / 100)
                due = due + interest
                if due >= 500:
                    numbernamedict[numberlist[i]] = "**" + numbernamedict[numberlist[i]]
    return numbernamedict, numberlist, numberliststr

def table(numbernamedict, duesdict, paymentsdict, paymentsumdict, paymentstrdict, numberliststr, numberlist):
    #printing the table using combination of print functions and write functions
    suminterest = []
    paymentsum = []
    print("+--------------+------------------+--------+-----+")
    summary.write("+--------------+------------------+--------+-----+\n")
    print("| Phone Number | Name             | Due    | Int |")
    summary.write("| Phone Number | Name             | Due    | Int |\n")
    print("+--------------+------------------+--------+-----+")
    summary.write("+--------------+------------------+--------+-----+\n")
    #goes through every number and calls proper dictionaries to print the numbers,
    #names, interest, dues, payments and dates
    #goes through three if cycles in the first one numberlist[i] is both included
    #in duesdict and paymentsdict, in the second one duesdict not included but paymentsdict
    #is included. In the third one, duesdict is included but paymentsdict is not included.
    #The point of doing is to be able to print every phone number and names even though
    #they did not pay anything
    for i in range(len(numbernamedict)):
        if numberlist[i] in duesdict:
            if numberlist[i] in paymentsdict:
                due = duesdict[numberlist[i]] - paymentsumdict[numberlist[i]]
                if due >= 100: #if dues are above hundered it applies interest on it
                    interest = float(due / 100)
                    suminterest.append(interest)
                    print("|%14s|%18s|$ %6.2f|$%4.2f|"%(numberliststr[i], numbernamedict[numberlist[i]][:18].ljust(18), due + interest, interest), "[$%6.2f] %s"%(paymentsumdict[numberlist[i]], paymentstrdict[numberlist[i]]))
                    paymentsum.append(paymentsumdict[numberlist[i]])
                    summary.write("|%14s|" %(numberliststr[i]))
                    summary.write("%18s|" %(numbernamedict[numberlist[i]][:18].ljust(18))) #aligns the names to the left
                    summary.write("$ %6.2f|" %(due + interest))
                    summary.write("$%4.2f| " %(interest))
                    summary.write("[$%6.2f] " %(paymentsumdict[numberlist[i]]))
                    summary.write("%s\n" %(paymentstrdict[numberlist[i]]))
                else:
                    interest = ""
                    print("|%14s|%18s|$ %6.2f|%5.2s|"%(numberliststr[i], numbernamedict[numberlist[i]][:18].ljust(18), due, interest), "[$%6.2f] %s"%(paymentsumdict[numberlist[i]], paymentstrdict[numberlist[i]]))
                    paymentsum.append(paymentsumdict[numberlist[i]])
                    summary.write("|%14s|" %(numberliststr[i]))
                    summary.write("%18s|" %(numbernamedict[numberlist[i]][:18].ljust(18)))
                    summary.write("$ %6.2f|" %(due))
                    summary.write("%5.2s| " %(interest))
                    summary.write("[$%6.2f] " %(paymentsumdict[numberlist[i]]))
                    summary.write("%s\n" %(paymentstrdict[numberlist[i]]))
        if numberlist[i] not in duesdict:
            if numberlist[i] in paymentsdict:
                due = 0
                duesdict[numberlist[i]] = 0
                if due > 100:
                    interest = duesdict[numberlist[i]] / 100
                    suminterest.append(interest)
                    print("|%14s|%18s|$ %6.2f|$%4.2f|"%(numberliststr[i], numbernamedict[numberlist[i]][:18].ljust(18), due + interest, interest), "[$%6.2f] %s"%(paymentsumdict[numberlist[i]], paymentstrdict[numberlist[i]]))
                    paymentsum.append(paymentsumdict[numberlist[i]])
                    summary.write("|%14s|" %(numberliststr[i]))
                    summary.write("%18s|" %(numbernamedict[numberlist[i]][:18].ljust(18)))
                    summary.write("$ %6.2f|" %(due + interest))
                    summary.write("$%4.2f| " %(interest))
                    summary.write("[$%6.2f] " %(paymentsumdict[numberlist[i]]))
                    summary.write("%s\n" %(paymentstrdict[numberlist[i]]))
                else:
                    interest = ""
                    print("|%14s|%18s|$ %6.2f|%5.2s|"%(numberliststr[i], numbernamedict[numberlist[i]][:18].ljust(18), due, interest), "[$%6.2f] %s"%(paymentsumdict[numberlist[i]], paymentstrdict[numberlist[i]]))
                    paymentsum.append(paymentsumdict[numberlist[i]])
                    summary.write("|%14s|" %(numberliststr[i]))
                    summary.write("%18s|" %(numbernamedict[numberlist[i]][:18].ljust(18)))
                    summary.write("$ %6.2f|" %(duesdict[numberlist[i]]))
                    summary.write("%5.2s| " %(interest))
                    summary.write("[$%6.2f] " %(paymentsumdict[numberlist[i]]))
                    summary.write("%s\n" %(paymentstrdict[numberlist[i]]))
        if numberlist[i] in duesdict:
            if numberlist[i] not in paymentsdict:
                due = duesdict[numberlist[i]]
                if due > 100:
                    interest = duesdict[numberlist[i]] / 100
                    suminterest.append(interest)
                    print("|%14s|%18s|$ %6.2f|$%4.2f|"%(numberliststr[i], numbernamedict[numberlist[i]][:18].ljust(18), due + interest, interest))
                    summary.write("|%14s|" %(numberliststr[i]))
                    summary.write("%18s|" %(numbernamedict[numberlist[i]][:18].ljust(18)))
                    summary.write("$ %6.2f|" %(duesdict[numberlist[i]] + interest))
                    summary.write("$%4.2f|\n" %(interest))
                else:
                    interest = ""
                    print("|%14s|%18s|$ %6.2f|%5.2s|"%(numberliststr[i], numbernamedict[numberlist[i]][:18].ljust(18), due, interest))
                    summary.write("|%14s|" %(numberliststr[i]))
                    summary.write("%18s|" %(numbernamedict[numberlist[i]][:18].ljust(18)))
                    summary.write("$ %6.2f|" %(duesdict[numberlist[i]]))
                    summary.write("%5.2s|\n" %(interest))
    print("+--------------+------------------+--------+-----+")
    summary.write("+--------------+------------------+--------+-----+\n")
    netduetotal = sum(totaldues) - sum(paymentsum) + sum(suminterest)
    print("| Total Dues   |%17s%10.2f|"%("$", netduetotal))
    summary.write("| Total Dues   |%17s" %("$"))
    summary.write("%10.2f|\n" %(netduetotal))
    print("+--------------+---------------------------+")
    summary.write("+--------------+---------------------------+\n")
    print("| Total Interes|%20s%7.2f|"%("$", sum(suminterest)))
    summary.write("| Total Interes|%20s" %("$"))
    summary.write("%7.2f|\n" %(sum(suminterest)))
    print("+--------------+---------------------------+")
    summary.write("+--------------+---------------------------+")
    return

if __name__ == '__main__':
    #oepn the files and then close
    families = open("families.txt", "r")
    dues = open("dues.txt","r")
    payments = open("payments.txt", "r")
    summary = open("summary.txt", "w")
    duesdict, totaldues = duesdict(dues)
    paymentsdict, paymentsumdict, paymentstrdict = paymentsdict(payments)
    numbernamedict, numberlist, numberliststr = numbernamedict(families, duesdict, paymentsumdict)
    table(numbernamedict, duesdict, paymentsdict, paymentsumdict, paymentstrdict, numberliststr, numberlist)
    families.close()
    dues.close()
    payments.close()
    summary.close()
