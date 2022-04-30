'''
Script:  File Metadata Extractor
Author:  Chet Hosmer
Edited by: Rodney Arnold
Date:    March 2022
Version: .51
Purpose: Extracts information about files useful in forensic examinations.
'''


import os  # File System Methods
import time  # Time Conversion Methods
import sys  # System Methods


''' IMPORT 3RD PARTY LIBRARIES '''
from prettytable import PrettyTable

''' DEFINE PSEUDO CONSTANTS '''
# Create the table with all the columns we need
TBL = PrettyTable(['Path', 'Size', 'Last Access Time', 'Last Modified Time', 'Creation Time', 'st_mode',
                   'st_ino', 'st_dev', 'st_nlink', 'st_uid', 'st_gid', 'st_size', 'st_atime', 'st_mtime',
                   'ST_ctime'])
''' LOCAL FUNCTIONS '''


# This function gets called as the script iterates through the list of files/folders.
def metaDatas(n, fileList):
    print("Accessing Metadata...")
    time.sleep(1)

    try:

        metaData = os.stat(path)  # Use the stat method to obtain meta data
        fileSize = metaData.st_size  # Extract fileSize and MAC Times
        timeLastAccess = metaData.st_atime
        timeLastModified = metaData.st_mtime
        timeCreated = metaData.st_ctime

        print("MetaData:           ", metaData)
        print("File/Folder Size:   ", fileSize)
        print("Last Access Time:   ", time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(timeLastAccess)), "UTC, ",
              timeLastAccess, " MAC Time")
        timeLastAccess2 = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(timeLastAccess))
        print("Last Modified Time: ", time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(timeLastModified)), "UTC, ",
              timeLastModified, " MAC Time")
        timeLastModified2 = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(timeLastModified))
        print("Creation Time:      ", time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(timeCreated)), "UTC, ",
              timeCreated, " MAC Time")
        timeCreated2 = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(timeCreated))

        # Split the metadata into sections so each value can be uploaded to the table
        stMode = metaData.st_mode
        stIno = metaData.st_ino
        stDev = metaData.st_dev
        stnLink = metaData.st_nlink
        stUID = metaData.st_uid
        stGID = metaData.st_gid
        stSize = metaData.st_size
        stATime = metaData.st_atime
        stMTime = metaData.st_mtime
        stCTime = metaData.st_ctime

        # Now we add all those values into the table
        TBL.add_row([path, fileSize, timeLastAccess2 + " UTC", timeLastModified2 + " UTC", timeCreated2 + " UTC",
                     stMode, stIno, stDev, stnLink, stUID, stGID, stSize, stATime, stMTime, stCTime])

        # Store your formatted values in a sorted variable resultString
        resultString = TBL.get_string(sortby="Path", reversesort=True)
        b = n
        b += 1
        if b == len(fileList):
            print(resultString)

    except Exception as err:
        print("Fail:    ", targetFile, "Exception = ", str(err))


''' LOCAL CLASSES '''
# NONE

''' MAIN ENTRY POINT '''


if __name__ == '__main__':

    print("File Info: Obtain File/Folder Meta Data\n")

    targetFile = input("Enter File/Folder Path to Process: ")

    if not os.path.isfile(targetFile):
        # Okay here is the directory portion of code.
        directoryPath = targetFile
        try:
            fileList = os.listdir(directoryPath)  # get directory entries
            # Create a tbl object that also defines the headings

            n = 0
            numberedEntry = fileList[n]  # get the first name from the list

            print("================================================\n")
            print("\nFile/Folder name:   ", numberedEntry)

            for line in fileList:
                # convert the entry into a full path
                path = os.path.join(directoryPath, fileList[n])
                print("Full Path:          ", path)
                metaDatas(n, fileList)
                print("\n================================================")
                n += 1
        except Exception as err:
            print(err)
            sys.exit("Invalid File/Folder: " + targetFile)
    # Now we can handle in individual file.
    elif os.path.isfile(targetFile):
        try:
            print("================================================\n")
            print("\nFile/Folder name:   ", targetFile)
            path = targetFile
            metaDatas()
            print("\n================================================")
        except Exception as err:
            print(err)
            sys.exit("Invalid File/Folder: " + targetFile)
    # Just in case :)
    else:
        sys.exit("Invalid File: ", targetFile)

    print("\nScript End")
