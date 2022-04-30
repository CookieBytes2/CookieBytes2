'''
Script:  File System Walker
Author:  Chet Hosmer
Edited by: Rodney Arnold
Date:    March 2022
Version: .51
Purpose: Extracts information about files useful in forensic examinations.
'''
''' IMPORT STANDARD LIBRARIES '''
import os
import sys
import hashlib
import time
''' IMPORT 3RD PARTY LIBRARIES '''
from prettytable import PrettyTable

''' DEFINE PSEUDO CONSTANTS '''
TBL = PrettyTable(['Path', 'Size', 'Last Access Time', 'Last Modified Time', 'Creation Time', 'HASH'])

''' LOCAL FUNCTIONS '''


def get_directory_size(fullPath):
    """Returns the `directory` size in bytes."""
    total = 0
    try:
        # print("[+] Getting the size of", directory)
        for entry in os.scandir(fullPath):
            if entry.is_file():
                # if it's a file, use stat() function
                total += entry.stat().st_size
            elif entry.is_dir():
                # if it's a directory, recursively call this function
                total += get_directory_size(entry.path)
    except NotADirectoryError:
        # if `directory` isn't a directory, get the file size then
        return os.path.getsize(fullPath)
    except PermissionError:
        # if for whatever reason we can't open the folder, return 0
        return 0
    return total


def metaDatas():
    print("Accessing Metadata...")

    try:

        metaData = os.stat(fullPath)  # Use the stat method to obtain meta data
        # Determine the size of both folders and directories.
        if os.path.isdir(fullPath):
            fileSize = get_directory_size(fullPath)
            '''
            for dirpath, dirnames, filenames in os.walk(fullPath):
                fileSize = 0
                for f in filenames:
                    fp = os.path.join(dirpath, f)
                    # skip if it is symbolic link
                    if not os.path.islink(fp):
                        fileSize += os.path.getsize(fp)
            '''
        else:
            fileSize = metaData.st_size  # Extract fileSize and MAC Times

        timeLastAccess = metaData.st_atime
        timeLastModified = metaData.st_mtime
        timeCreated = metaData.st_ctime

        timeLastAccess2 = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(timeLastAccess))

        timeLastModified2 = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(timeLastModified))

        timeCreated2 = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(timeCreated))

        # This section will perform hashes on each file.

        if os.path.isfile(fullPath):
            try:
                with open(fullPath, 'rb') as target:
                    fileContents = target.read()
                sha256Obj = hashlib.sha256()
                sha256Obj.update(fileContents)
                hexDigest = sha256Obj.hexdigest()
            except Exception as err:
                sys.exit("\nException: " + str(err))
        else:
            hexDigest = "N/A"
        # Now we add all those values into the table
        TBL.add_row([fullPath, fileSize, timeLastAccess2 + " UTC", timeLastModified2 + " UTC", timeCreated2 + " UTC",
                     hexDigest])

        # Store your formatted values in a sorted variable resultString
        TBL.align = "l"
        resultString = TBL.get_string(reversesort=False)

        return resultString

    except Exception as err:
        print("Fail:    ", targetFolder, "Exception = ", str(err))


''' MAIN ENTRY POINT '''
if __name__ == '__main__':
    print("Beginning directory walk...\n")
    targetFolder = input("Enter Folder Path to Process: ")

    if os.path.isfile(targetFolder):
        print("Please enter a directory, not a file.")
        sys.exit()
    elif os.path.isdir(targetFolder):

        for root, dirs, fileList in os.walk(targetFolder):

            for nextDir in dirs:
                fullPath = os.path.join(root, nextDir)
                #tableStuff = metaDatas()
                metaDatas()

                # For each of the files, join the path with the filename to get the complete path
            for nextFile in fileList:
                fullPath = os.path.join(root, nextFile)
                #tableStuff = metaDatas()
                metaDatas()

        tableStuff = metaDatas()
        print(tableStuff)
        print("\nScript End")

    else:
        sys.exit("Something went wrong trying to determine if you entered a folder or file.")
