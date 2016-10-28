<<<<<<< HEAD
import sys
import struct
from struct import pack
import os
from util import *


def writeID(nud,baseID,groupID,subgroupID,offsetID):
    nud.seek(0xB,1)
    texCount = readByte(nud)
    nud.seek(0x14,1)
    for i in range(texCount):
        checkID = readByte(nud)
        nud.seek(3,1)
        if checkID != 0x10:
            nud.seek(-4,1)
            writeByte(nud,baseID)
            writeByte(nud,groupID)
            writeByte(nud,subgroupID)
            texID = readByte(nud)
            nud.seek(-1,1)
            writeByte(nud,(texID % 128)+offsetID)
        nud.seek(0x14,1)
def IDFixNud(path,baseID,groupID,subgroupID,offsetID):
    with open(path, "rb+") as nud:
        #setup are arrays
        polyDataStart = []
        totalSubPolys=[]
        texProp1Start=[]
        texProp2Start=[]
        texProp3Start=[]
        texProp4Start=[]
        if(offsetID == 0 or offsetID == 128):
            offsetID = offsetID
        else:
            offsetID = 0

        header = nud.read(4)
        if header != "NDP3":
            return False
        nud.seek(0x6,1)
        totalPolys = readu16be(nud)
        nud.seek(0x30)

        for z in range(totalPolys):
            nud.seek(0x2A,1)
            totalSubPolys.append(readu16be(nud))
            polyDataStart.append(readu32be(nud))
        for p in range(len(polyDataStart)):
            nud.seek(polyDataStart[p])
            for num in range(totalSubPolys[p]):
                nud.seek(0x10,1)
                texProp1Start.append(readu32be(nud))
                texProp2Start.append(readu32be(nud))
                texProp3Start.append(readu32be(nud))
                texProp4Start.append(readu32be(nud))
                nud.seek(0x10,1)

        for z in range(len(texProp1Start)):
            nud.seek(texProp1Start[z])
            writeID(nud,baseID,groupID,subgroupID,offsetID)
            if texProp2Start[z] != 0:
                nud.seek(texProp2Start[z])
                writeID(nud,baseID,groupID,subgroupID,offsetID)
            if texProp3Start[z] != 0:
                nud.seek(texProp3Start[z])
                writeID(nud,baseID,groupID,subgroupID,offsetID)
            if texProp4Start[z] != 0:
                nud.seek(texProp4Start[z])
                writeID(nud,baseID,groupID,subgroupID,offsetID)
    return True

def IDFixNut(path,baseID,groupID,subgroupID,offsetID):
    with open(path,"rb+") as nut:
        NTWU = nut.read(4)
        if NTWU != "NTWU" and NTWU != "NTP3":
            return False
        nut.seek(0x6)
        fileTotal = readu16be(nut)
        nut.seek(0x10)
        for i in range(fileTotal):
            nut.seek(0xC,1)
            nut.seek(readu16be(nut)-0x16,1)
            writeByte(nut,baseID)
            writeByte(nut,groupID)
            writeByte(nut,subgroupID)
            texID = readByte(nut)
            nut.seek(-1,1)
            writeByte(nut,(texID % 128)+offsetID)
            nut.seek(4,1)
    return True
=======
import sys
import struct
from struct import pack
import os
from util import *


def writeID(nud,baseID,groupID,subgroupID,offsetID):
    nud.seek(0xB,1)
    texCount = readByte(nud)
    nud.seek(0x14,1)
    for i in range(texCount):
        checkID = readByte(nud)
        nud.seek(3,1)
        if checkID != 0x10:
            nud.seek(-4,1)
            writeByte(nud,baseID)
            writeByte(nud,groupID)
            writeByte(nud,subgroupID)
            texID = readByte(nud)
            nud.seek(-1,1)
            writeByte(nud,(texID % 128)+offsetID)
        nud.seek(0x14,1)
def IDFixNud(path,baseID,groupID,subgroupID,offsetID):
    with open(path, "rb+") as nud:
        #setup are arrays
        polyDataStart = []
        totalSubPolys=[]
        texProp1Start=[]
        texProp2Start=[]
        texProp3Start=[]
        texProp4Start=[]
        if(offsetID == 0 or offsetID == 128):
            offsetID = offsetID
        else:
            offsetID = 0

        header = nud.read(4)
        if header != "NDP3":
            return False
        nud.seek(0x6,1)
        totalPolys = readu16be(nud)
        nud.seek(0x30)

        for z in range(totalPolys):
            nud.seek(0x2A,1)
            totalSubPolys.append(readu16be(nud))
            polyDataStart.append(readu32be(nud))
        for p in range(len(polyDataStart)):
            nud.seek(polyDataStart[p])
            for num in range(totalSubPolys[p]):
                nud.seek(0x10,1)
                texProp1Start.append(readu32be(nud))
                texProp2Start.append(readu32be(nud))
                texProp3Start.append(readu32be(nud))
                texProp4Start.append(readu32be(nud))
                nud.seek(0x10,1)

        for z in range(len(texProp1Start)):
            nud.seek(texProp1Start[z])
            writeID(nud,baseID,groupID,subgroupID,offsetID)
            if texProp2Start[z] != 0:
                nud.seek(texProp2Start[z])
                writeID(nud,baseID,groupID,subgroupID,offsetID)
            if texProp3Start[z] != 0:
                nud.seek(texProp3Start[z])
                writeID(nud,baseID,groupID,subgroupID,offsetID)
            if texProp4Start[z] != 0:
                nud.seek(texProp4Start[z])
                writeID(nud,baseID,groupID,subgroupID,offsetID)
    return True

def IDFixNut(path,baseID,groupID,subgroupID,offsetID):
    with open(path,"rb+") as nut:
        NTWU = nut.read(4)
        if NTWU != "NTWU" and NTWU != "NTP3":
            return False
        nut.seek(0x6)
        fileTotal = readu16be(nut)
        nut.seek(0x10)
        for i in range(fileTotal):
            nut.seek(0xC,1)
            nut.seek(readu16be(nut)-0x16,1)
            writeByte(nut,baseID)
            writeByte(nut,groupID)
            writeByte(nut,subgroupID)
            texID = readByte(nut)
            nut.seek(-1,1)
            writeByte(nut,(texID % 128)+offsetID)
            nut.seek(4,1)
    return True
>>>>>>> master
