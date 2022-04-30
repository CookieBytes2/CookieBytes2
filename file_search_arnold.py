'''
Script:  File System Walker
Author:  Rodney Arnold
Date:    March 2022
Version: 1.0
Purpose: Extracts information about files useful in forensic examinations.
'''

''' IMPORT STANDARD LIBRARIES '''
import os
import sys
import hashlib
import time
from pathlib import Path

''' IMPORT 3RD PARTY LIBRARIES '''
from prettytable import PrettyTable

''' MAIN ENTRY POINT '''
if __name__ == '__main__':

    tbl = PrettyTable(['Path', 'Name Match', '.ext Match', 'Hash Match', 'FileSize', 'LastModified', 'LastAccess', 'Created', 'HASH'])

    print("Beginning directory walk...\n")
    targetFolder = input("Enter Folder Path to Process: ")
    fileName = input("Enter a file name to search: ")
    fileExt = input("Enter a file extension to look for: ")
    fileHash = input("Enter a SHA-256 hash value to look for: ")

    if not os.path.isdir(targetFolder):
        print("Please enter a valid directory path.")
        sys.exit()
    elif os.path.isdir(targetFolder):
        for currentRoot, dirList, fileList in os.walk(targetFolder):

            for nextFile in fileList:
                fullPath = os.path.join(currentRoot, nextFile)
                absPath = os.path.abspath(fullPath)

                stats = os.stat(absPath)

                fileSize = stats.st_size
                modEPOCH = stats.st_mtime
                accEPOCH = stats.st_atime
                creEPOCH = stats.st_ctime

                modTime = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(modEPOCH))
                accTime = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(accEPOCH))
                creTime = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(creEPOCH))

                hexDigest = ""
                hashObj = hashlib.sha256()
                with open(absPath, 'rb') as targetFile:
                    file_buffer = targetFile.read(8192)
                    while len(file_buffer) > 0:
                        hashObj.update(file_buffer)
                        file_buffer = targetFile.read(8192)
                        hexDigest = hashObj.hexdigest()

                a = ""
                b = ""
                c = ""

                if nextFile.lower().endswith(fileExt.lower()):
                    a = "x"
                if fileName.lower() in Path(nextFile.lower()).stem:
                    b = "x"
                if hexDigest == fileHash:
                    c = "x"
                if a == "x" or b == "x" or c == "x":
                    tbl.add_row([absPath, b, a, c, fileSize, modTime, accTime, creTime, hexDigest])
print(tbl.get_string())
print("\nScript-End\n")

