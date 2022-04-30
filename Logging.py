'''
Script:  File System Walker, logs each step.
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
import logging
from pathlib import Path

''' IMPORT 3RD PARTY LIBRARIES '''
from prettytable import PrettyTable

''' MAIN ENTRY POINT '''
if __name__ == '__main__':

    logging.basicConfig(filename='ScriptLog.log', level=logging.DEBUG,
                        format='%(asctime)s - %(process)d- %(levelname)s- %(message)s')

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

                logging.info('Processing file: ' + absPath)

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
                try:
                    with open(absPath, 'rb') as targetFile:
                        file_buffer = targetFile.read(8192)
                        while len(file_buffer) > 0:
                            hashObj.update(file_buffer)
                            file_buffer = targetFile.read(8192)
                            hexDigest = hashObj.hexdigest()
                except Exception:
                    logging.error('Unable to open file: ' + absPath)

                a = ""
                b = ""
                c = ""

                if nextFile.lower().endswith(fileExt.lower()):
                    a = "x"
                    logging.critical('Extension match found for: ' + absPath)
                if fileName.lower() in Path(nextFile.lower()).stem:
                    b = "x"
                    logging.critical('File name match found for: ' + absPath)
                if hexDigest == fileHash:
                    c = "x"
                    logging.critical('File hash value match found for: ' + absPath)
                if a == "x" or b == "x" or c == "x":
                    tbl.add_row([absPath, b, a, c, fileSize, modTime, accTime, creTime, hexDigest])
print(tbl.get_string())
print("\nScript-End\n")

