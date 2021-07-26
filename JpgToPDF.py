import os,glob
import re
from shutil import copytree, rmtree
from PIL import Image
import tkinter.filedialog
from fpdf import FPDF

#Definitions for Human text sorting for serialization
def atoi(text):
    return int(text) if text.isdigit() else text
def natural_keys(text):
    return [ atoi(c) for c in re.split(r'(\d+)', text) ]

#Counters for Serializing Folders and Files
dirCount = 1
fileCount = 1
fileList = []
while True:
    inputFileLocation = input("Input File Location:")
    if os.path.isdir(inputFileLocation):
        break
    else:
        print("Not a proper file directory please include entire directory path \nExample: C:\\User\\Downloads")
splitInput = inputFileLocation.split("\\")
inputRootDir = '\\'.join(splitInput[:-1])
dirOnlyVal = splitInput[-1]
serialDirPath = inputRootDir + '\\' + dirOnlyVal + '_Serialized'
if os.path.exists(serialDirPath):
    rmtree(serialDirPath)
    #copy directory to same root directory
copytree(inputFileLocation,serialDirPath)
#Serializing loop to rename all folders and files in Human Order
for root, dirs, files in os.walk(serialDirPath):
    dirs.sort(key=natural_keys)
    for name in dirs:
        originalPathVal = os.path.join(root,name)
        renamedPathVal = '\\'.join(originalPathVal.split("\\")[:-1]) + "\\" + str(dirCount)
        dirCount += 1
        #print(renamedPathVal)
        os.rename(originalPathVal,renamedPathVal)
for root, dirs, files in os.walk(serialDirPath):
    dirs.sort(key=natural_keys)
    for name in files:
        originalPathVal = os.path.join(root,name)
        extensionVal = originalPathVal.split('\\')[-1].split('.')[0]
        renamedPathVal = '\\'.join(originalPathVal.split("\\")[:-1]) + "\\" + str(fileCount) + '.' + originalPathVal.split('\\')[-1].split('.')[1]
        fileCount += 1
        #print(renamedPathVal)
        os.rename(originalPathVal,renamedPathVal)
# Convert all png to jpeg
for file in glob.glob(os.path.join(serialDirPath + '/**/*.png')):
    filename=file.split(".")
    img = Image.open(file)
    target_name = filename[0] + ".jpg"
    rgb_image = img.convert('RGB')
    rgb_image.save(target_name)
    os.remove(file)
    print("Converted png to jpg as " + target_name)
for root, dirs, files in os.walk(serialDirPath):
    files.sort(key=natural_keys)
    for name in files:
        fileList.append(os.path.join(root,name))
pdf = FPDF(unit='mm')
pdf.set_auto_page_break(0)
#print(fileList)
fileList.sort(key=natural_keys)
for image in fileList:
    print(image)
    pdf.add_page()
    pdf.image(image,0,0,210)
nameOutput = inputFileLocation.split('\\')[-1].replace("~","").replace(" ","").removesuffix('_Serialized') + '.pdf'
pdfOutPath = inputRootDir.replace('\\','/') + '/' + nameOutput
pdf.output(pdfOutPath).encode('latin-1')

