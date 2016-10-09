from __future__ import unicode_literals
import os
import sys
import zlib
import glob

from TexIDfix import *
from MTA_IDFix import mtaFix
import fixpath
from colorama import init, Fore, Back, Style
from pearhash import PearsonHasher,makeValueValid
from util import *

def IDFixFile(path,baseID,groupID,subgroupID,offsetID):
    """identify whether the path is a nud or a nut and call the apprpriate  method"""
    if path.endswith(".nut"):
         return IDFixNut(path,baseID,groupID,subgroupID,offsetID)
    elif path.endswith(".nud"):
         return IDFixNud(path,baseID,groupID,subgroupID,offsetID)
    return None

def checkAndDecompress(path):
    """will check the supplied file if its zLib compressed and decompress it if it is."""
    with open(path,'rb') as f:
        content = f.read()
    try:
        decomped = zlib.decompress(content)
    except:
        pass
    else:
        with open(path,'wb') as f:
            f.write(decomped)
        return True
    return False

def IDFixFull(path,folderPath,baseID,groupID,subgroupID,offsetID,isError):
    """does the full check for idfixing a file"""
    if os.path.isfile(path):
        worked = IDFixFile(path,baseID,groupID,subgroupID,offsetID)
        if not worked:
            isDecomped = checkAndDecompress(path)
            if isDecomped:
                worked = IDFixFile(path,baseID,groupID,subgroupID,offsetID)
                if not worked:
                    errorCode("ERROR: the " + path.split("\\")[-1] + " in: " + folderPath + " could not be idfixed. it may be corrupted...")
                    return True
    return isError

def getCorrectIDs(path):
    """returns the id supplied by nintendo if its a existing model otherwise returns a unique value using hashes"""
    splitPath = path.split("\\")
    checkPath = splitPath[-4] + "\\" + splitPath[-3] + "\\" + splitPath[-2] + "\\" + splitPath[-1]
    with open(configPath + "\\idList.csv",'rb') as f:
        for line in f:
            if checkPath in line:
                ids = line.split(",")
                return (int(ids[1]),int(ids[2]),int(ids[3]),int(ids[4]))
    hasher = PearsonHasher(3)
    hexhash = hasher.hash(checkPath).hexdigest()
    baseID = makeValueValid(82,91,int(hexhash[:-4],16),checkPath,len(checkPath)/7)
    return (baseID,int(hexhash[2:-2],16),int(hexhash[4:],16),0)


def IDFix(path):
    """will id fix the passed folder"""
    global errorCount
    isError = False
    baseID,groupID,subgroupID,offsetID = getCorrectIDs(path)
    nudPath = path + "\\model.nud"
    nutPath = path + "\\model.nut"
    metalPath = path + "\\metal.nud"
    if baseID == 64:
        isError = IDFixFull(nudPath,path,baseID,groupID,subgroupID,offsetID,isError)
        isError = IDFixFull(nutPath,path,baseID,groupID,subgroupID,offsetID,isError)
        isError = IDFixFull(metalPath,path,baseID,groupID,subgroupID,offsetID,isError)
    else:
        if os.path.isfile(nudPath) and os.path.isfile(nutPath): 
            isError = IDFixFull(nudPath,path,baseID,groupID,subgroupID,offsetID,isError)
            isError = IDFixFull(nutPath,path,baseID,groupID,subgroupID,offsetID,isError)
            isError = IDFixFull(metalPath,path,baseID,groupID,subgroupID,offsetID,isError)
    mtaFix(path,baseID,groupID,subgroupID,offsetID)
    if isError:
        errorCount += 1

def getOutputName(fighterFolder):
    """returns the name defined in the fighters.csv"""
    return allFighterNames[allFighterFolders.index(fighterFolder)]

def IDFixFighter(path,fixType):
    outputName = getOutputName(path.split("\\")[-1].rstrip())
    if os.path.isdir(path + "\\model"):
        if fixType == 'all' or fixType == 'extra':
            print "Beginning " + fixType + " folders for " + outputName.rstrip() + "..."
        else:
            print "Beginning " + fixType + " folder for " + outputName.rstrip() + "..."

        for modelType in glob.glob(path + r"\model\*"):
            if fixType == 'all':
                for folderSlot in glob.glob(modelType + r"\*"):
                    IDFix(folderSlot)
            elif fixType == 'extra':
                if modelType.split("\\")[-1] != 'body':
                    for folderSlot in glob.glob(modelType + r"\*"):
                        IDFix(folderSlot)
            else:
                if modelType.split("\\")[-1] == fixType:
                    for folderSlot in glob.glob(modelType + r"\*"):
                        IDFix(folderSlot)

        if fixType == 'all' or fixType == 'extra':
            print fixType + " folders for " + outputName.rstrip() + " complete."
        else:
            print fixType + " folder for " + outputName.rstrip() + " complete."
        print
    else:
        print "No skins for " + outputName.rstrip() + " exist. skipping..."
        print

def IdFixAllFighters(path):
    global errorCount
    for folder in allFighterFolders:
        IDFixFighter(path + "\\" + folder,'all')
    print "MISHUN COMPREE!"
    print
    if errorCount > 0:
        errorCode("SEGTENDO WARNING: " + str(errorCount) + " skins were unable to be ID-Fixed!")
    errorCount = 0

errorCount = 0
allFighterFolders = []
allFighterNames = []
with open(configPath + "\\fighters.csv", 'rb+') as f:
    for line in f:
        if "," in line:
            stringLine = line.split(",")
            allFighterFolders.append(stringLine[0].rstrip())
            allFighterNames.append(stringLine[1].rstrip())
        else:
            allFighterFolders.append(line.rstrip())
            allFighterNames.append(line.rstrip().title())
