'''
Searching for Images with PIL
Compare all files in a path to determine images, regardless of file extension.
Rodney Arnold
April 2022
'''

import sys
import os
import json
import csv
from PIL import Image
from prettytable import PrettyTable


''' MAIN ENTRY POINT '''
if __name__ == '__main__':

    # Create the JSON file
    jsonFile = open("photo.json", "w")
    photoDict = {}

    # Create the csv file, and add titles
    csvFile = open("results.csv", "w", newline='')
    reportWriter = csv.writer(csvFile, delimiter=',', quotechar='"')
    heading = ['File', 'Ext', 'Format', 'Width', 'Height', 'Mode', 'ERR']
    reportWriter.writerow([fld for fld in heading])   # Write Heading

    imType = ["APNG", "AVIF", "GIF", "JPEG", "PNG", "SVG", "WEBP", "BMP", "ICO", "TIFF"]
    imExt = [[".apng"], [".avif"], [".gif"], [".jpg", ".jpeg", ".jfif", ".pjpeg", ".pjp"], [".png"], [".svg"], [".webp"],
            [".bmp"], [".ico", ".cur"], [".tif", ".tiff"]]

    tbl = PrettyTable(['File', 'Ext', 'Format', 'Width', 'Height', 'Mode', 'ERR'])
    targetFolder = input("Enter a directory to search: ")
    fileList = os.walk(targetFolder)
    if not os.path.isdir(targetFolder):
        print("Please enter a valid directory path.")
        sys.exit()
    elif os.path.isdir(targetFolder):
        for currentRoot, dirList, fileList in os.walk(targetFolder):

            for nextFile in fileList:
                fullPath = os.path.join(currentRoot, nextFile)
                absPath = os.path.abspath(fullPath)
                csvPath = absPath.replace('\\', '/')
                if os.path.isfile(absPath):
                    ext = os.path.splitext(absPath)[1]
                    ext2 = os.path.splitext(absPath)[1].lower()
                    try:
                        with Image.open(absPath) as im:

                            index = imType.index(im.format)
                            list2 = imExt[index]
                            a = 0
                            list3 = []
                            for i in list2:
                                strImg = list2[a].lower()
                                list3.append(strImg)
                                a += 1
                            if ext2.lower() in list3:
                                Err = ""
                            else:
                                Err = "*"

                            tbl.add_row([absPath, ext, im.format, im.size[0], im.size[1], im.mode, Err])
                            photoDict[fullPath] = [ext, im.format, im.size[0], im.size[1], im.mode, Err]
                            reportWriter.writerow([csvPath, ext, im.format, im.size[0], im.size[1], im.mode, Err])
                    except Exception as err:
                        tbl.add_row([absPath, ext, "[NA]", "[NA]", "[NA]", "[NA]", ""])
                        photoDict[absPath] = [ext, "[NA]", "[NA]", "[NA]", "[NA]", ""]
                        reportWriter.writerow([csvPath, ext, "[NA]", "[NA]", "[NA]", "[NA]", ""])
                        pass
                else:
                    continue
            json.dump(photoDict, jsonFile, indent=4)

    tbl.align = 'l'
    print(tbl.get_string(sortby="ERR", reversesort=True))
