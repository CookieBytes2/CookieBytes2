'''
Rodney Arnold
Final Script
April 2022
'''
import os
import re
import hashlib
import time
import multiprocessing
from prettytable import PrettyTable


NAME = "Rodney Arnold"  # Add your Name to this constant

tbl = PrettyTable(['String', 'Occurs'])  # Output Table top 10 strings and the number of occurrences of each

'''Local Functions'''


def func1(chunkdLst, queue):        # Creates a unique list based on a segment of txtList
    uniqList = []
    for i in chunkdLst:
        if i not in uniqList:
            uniqList.append(i)
    queue.put(uniqList)


def func2(chunkdLst, queue):        # Returns a list containing all strings of length 10-15
    weedOutList = []
    for i in chunkdLst:
        if 10 <= len(i) <= 15:      # Find all strings 10-15 chars in length
            weedOutList.append(i)
    queue.put(weedOutList)


''' MAIN ENTRY POINT '''

if __name__ == '__main__':

    print("Final Script")
    print("Please be patient, as large files may take some time to process...\n")
    time.sleep(.5)
    print("WARNING: THIS PROGRAM IS VERY CPU INTENSIVE\n")
    time.sleep(.5)

    print("Beginning sequence...")
    with open("mem.raw", 'rb') as target:  # assumes that mem.raw is in the same folder as script

        contents = target.read()  # read the entire contents of the file

    txt = re.sub(b"[^A-Za-z']", b' ', contents)  # strip all non alpha characters
    txt = txt.lower()  # convert all to lower case
    txt = txt.decode("utf-8")  # convert to simple ASCII
    target.close()

    '''
    you will add your code here, to extract specific metrics
    associated with mem.raw:
    '''
    # Find the size of mem.raw
    absPath = os.path.abspath('mem.raw')

    # Extract file size of mem.raw
    stats = os.stat(absPath)
    fileSize = stats.st_size
    print(fileSize, "Bytes")

    # Create a SHA-256 hash of mem.raw
    hexDigest = ""
    hashObj = hashlib.sha256()
    with open(absPath, 'rb') as targetFile:
        file_buffer = targetFile.read(8192)
        while len(file_buffer) > 0:
            hashObj.update(file_buffer)
            file_buffer = targetFile.read(8192)
            sha256 = hashObj.hexdigest()
    print("sha-256: ", sha256)
    targetFile.close()

    # Create list of each string in the file
    txtList = txt.split()
    print("Created txtList. Length: ", len(txtList))

    # Total number of strings
    totStrings = len(txtList)

    #  Divide txtList into pieces up to 1,000,000 items in length.
    chunkedList = []
    for i in range(0, totStrings, 1000000):
        chunkedList.append(txtList[i:i+1000000])

    # Multi-process the creation of a unique list
    queue = multiprocessing.Queue()
    processes = []
    rets = []
    a = 0
    for i in range(len(chunkedList)):
        p = multiprocessing.Process(target=func1, args=(chunkedList[a],  queue))
        processes.append(p)
        p.start()
        a += 1  # just added this

    for p in processes:
        ret = queue.get()
        rets.append(ret)

    for p in processes:
        p.join()

    # Combine all the lists used by the cores.
    uniqList = []
    for i in rets:
        for j in rets[rets.index(i)]:
            uniqList.append(j)

    # Continue breaking down the 18 lists looking for unique strings.
    uniqList2 = []
    for i in uniqList:
        if i not in uniqList2:
            uniqList2.append(i)
    print("Total unique word count: ", len(uniqList2))

    # Multi-process finding all the 10-15 length strings
    queue = multiprocessing.Queue()
    processes = []
    rets = []
    a = 0
    for i in range(len(chunkedList)):
        p = multiprocessing.Process(target=func2, args=(chunkedList[a], queue))
        processes.append(p)
        p.start()
        a += 1

    for p in processes:
        ret = queue.get()
        rets.append(ret)

    for p in processes:
        p.join()

    # Combine all the lists used by the cores.
    weedOutList = []
    for i in rets:
        for j in rets[rets.index(i)]:
            weedOutList.append(j)
    print("weedOutList length is: ", len(weedOutList))

    totUnique = len(uniqList2)

    # Sort all strings and store a count for each one
    finalList = []
    for i in weedOutList:
        if i not in finalList:
            finalList.append(i)
            finalList.append(1)
        elif i in finalList:
            index = finalList.index(i)
            index += 1
            finalList[index] += 1
    print("final list completed.")
    print("length: ", len(finalList), "\n")

    # Create a list of the ten most popular strings
    topTenList = sorted([finalList[i-1:i+1] for i in range(1, len(finalList), 2)], key=lambda x: x[1], reverse=True)

    cnt = 0
    while cnt < 10:
        tbl.add_row([topTenList[cnt][0], topTenList[cnt][1]])
        cnt += 1

    # Format the prettytable
    tbl.align = "l"
    resultString = tbl.get_string(sortby="Occurs", reversesort=True)

    # Convert the variables from ints to strings
    fileSize = str(fileSize)
    totStrings = str(totStrings)
    totUnique = str(totUnique)

    print("Your Name:        " + NAME + "\n")
    print("mem.raw Filesize: " + fileSize + "\n")
    print("mem.raw SHA-256:  " + sha256 + "\n")
    print("total Strings:    " + totStrings + "\n")
    print("Total Unique:     " + totUnique + "\n")
    print(resultString)



    # fileSize     mem.raw file size
    # sha256       SHA256 Hex Digest of mem.raw
    # totStrings   Total number of strings found (all lengths)
    # totUnique    Total unique strings found
    # tbl          Fill in the table as defined here
    # minimum string length = 10 maximum string length = 15

    '''
    DO NOT CHANGE ANY CODE BELOW HERE
    I had to change line 208, because it had an inappropriate argument.
    '''

    with open(NAME + "-FinalProject.txt", 'w') as final:
        final.write("Your Name:        " + NAME + "\n")
        final.write("mem.raw Filesize :" + fileSize + "\n")
        final.write("mem.raw SHA-256:  " + sha256 + "\n")
        final.write("total Strings:    " + totStrings + "\n")
        final.write("Total Unique:     " + totUnique + "\n")
        csv = tbl.get_csv_string(sortby="Occurs", reversesort=True)  # Changed this line.
        final.write(csv)
        final.close()

    print("Script End")
