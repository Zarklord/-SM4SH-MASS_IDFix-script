#Slightly edited from the original idfix script, it now handles errors better; credit goes to GFD

import sys
import struct
from struct import pack
import os
from util import *

def IDFixNud(path,baseID,groupID,subgroupID,offsetID):
    with open(path, "rb+") as nud:
        #setup are arrays
        boneCount = []
        vertexStart_array=[]
        vertexAmount_array=[]
        vertexSize_array=[]
        polyStart_array=[]
        polyAmount_array=[]
        polySize_array=[]
        vertexAddStart_array=[]
        UVSize_array=[]
        polyName_array=[]
        singleBind_array=[]
        texturePropertiesL1Start_array=[]
        texturePropertiesL2Start_array=[]
        texturePropertiesL3Start_array=[]
        texturePropertiesL4Start_array=[]
        textureNuml1_array=[]
        textureNuml2_array=[]
        textureNuml3_array=[]
        textureNuml4_array=[]

        nud.seek(0x4)

        fileSize = readu32be(nud)
        if(offsetID == 0 or offsetID == 128):
            offsetID = offsetID
        else:
            offsetID = 0
        #print("File Size is %i bytes" % (fileSize))
        nud.seek(2,1)
        polysets = readu16be(nud)
        nud.seek(4,1)
        polyClumpStart = (readu32be(nud) + 0x30)
        polyClumpSize = readu32be(nud)
        vertexClumpStart = (polyClumpStart + polyClumpSize)
        vertexClumpSize = readu32be(nud)
        vertexAddStart = (vertexClumpSize + vertexClumpStart)
        vertexAddClumpSize = readu32be(nud)
        nameClumpStart = (vertexAddClumpSize + vertexAddStart)
        nud.seek(0x10,1)
        objCount = 0

        for z in range(polysets):
            nud.seek(0x20,1)
            polynamestart = readu32be(nud)
            indentifiera = readu32be(nud)
            singleBind = readu16be(nud)
            polyamount = readu16be(nud)
            positionb = readu32be(nud)
            objCount = (objCount + polyamount)
            if polynamestart > 99999 or polyamount > 999:
                return False
            for s in range(polyamount):
                polyName_array.append(polynamestart)
                singleBind_array.append(singleBind)
        for p in range(objCount):
            polyStart = (readu32be(nud) + polyClumpStart)
            vertexStart = (readu32be(nud) + vertexAddStart)
            vertexAddStart = (readu32be(nud) + vertexAddClumpSize)
            vertexAmount = readu16be(nud)
            #print("There is %i Vertexs" % int(vertexAmount))
            vertexSize = readByte(nud)
            uvSize = readByte(nud)
            textureLayer1Properties = readu32be(nud)
            textureLayer2Properties = readu32be(nud)
            textureLayer3Properties = readu32be(nud)
            textureLayer4Properties = readu32be(nud)
            polyAmount = readu16be(nud)
            #print("There is %i Faces" % int(polyAmount))
            polySize = readByte(nud)
            polyFlag = readByte(nud)
            nud.seek(0xC,1)
            vertexStart_array.append(vertexStart)
            polyStart_array.append(polyStart)
            vertexAddStart_array.append(vertexAddStart)
            vertexAmount_array.append(vertexAmount)
            polyAmount_array.append(polyAmount)
            vertexSize_array.append(vertexSize)
            UVSize_array.append(uvSize)
            polySize_array.append(polySize)
            texturePropertiesL1Start_array.append(textureLayer1Properties)
            texturePropertiesL2Start_array.append(textureLayer2Properties)
            texturePropertiesL3Start_array.append(textureLayer3Properties)
            texturePropertiesL4Start_array.append(textureLayer4Properties)

        for z in range(objCount):
            nud.seek(texturePropertiesL1Start_array[z])
            nud.seek(8,1)
            texSomethingCount = readu16be(nud)
            texPropCount = readu16be(nud)
            nud.seek(20,1)
            for x in range(texPropCount):
                typeNum = readByte(nud)
                fightNum = readByte(nud)
                playNum = readByte(nud)
                texNum = readByte(nud)
                if(texNum > 0 and texNum <= 127):
                    texNum = texNum
                elif(texNum >= 128 and texNum <= 255):
                    texNum = texNum - 128
                if(typeNum != 0x10):
                    nud.seek(-4,1)
                    nud.write(struct.pack("B", baseID))
                    nud.write(struct.pack("B", groupID))
                    nud.write(struct.pack("B", subgroupID))
                    nud.write(struct.pack("B", offsetID + texNum))
                    nud.seek(-4,1)
                    typeNum = readByte(nud)
                    fightNum = readByte(nud)
                    playNum = readByte(nud)
                    texNum = readByte(nud)
                    nud.seek(20,1)
            headerRead = 0x20
            while headerRead == 0x20:
                headerRead = readu32be(nud)
                texPropNameStart = readu32be(nud)
                nud.seek(24,1)
                backUp = nud.tell()
                nud.seek(nameClumpStart + texPropNameStart)
                texPropName = getString(nud)
                nud.seek(backUp)
            if texturePropertiesL2Start_array[z] != 0:
                nud.seek(texturePropertiesL2Start_array[z])
                nud.seek(8,1)
                texSomethingCount = readu16be(nud)
                texPropCount = readu16be(nud)
                nud.seek(20,1)
                for x in range(texPropCount):
                    typeNum = readByte(nud)
                    fightNum = readByte(nud)
                    playNum = readByte(nud)
                    texNum = readByte(nud)
                    if(texNum > 0 and texNum <= 127):
                        texNum = texNum
                    elif(texNum >= 128 and texNum <= 255):
                        texNum = texNum - 128
                    if(typeNum != 0x10):
                        nud.seek(-4,1)
                        nud.write(struct.pack("B", baseID))
                        nud.write(struct.pack("B", groupID))
                        nud.write(struct.pack("B", subgroupID))
                        nud.write(struct.pack("B", offsetID + texNum))
                        nud.seek(-4,1)
                        typeNum = readByte(nud)
                        fightNum = readByte(nud)
                        playNum = readByte(nud)
                        texNum = readByte(nud)
                    nud.seek(20,1)
                headerRead = 0x20
                while headerRead == 0x20:
                    headerRead = readu32be(nud)
                    texPropNameStart = readu32be(nud)
                    nud.seek(24,1)
                    backUp = nud.tell()
                    nud.seek(nameClumpStart + texPropNameStart)
                    texPropName = getString(nud)
                    nud.seek(backUp)
            if texturePropertiesL3Start_array[z] != 0:
                nud.seek(texturePropertiesL2Start_array[z])
                nud.seek(8,1)
                texSomethingCount = readu16be(nud)
                texPropCount = readu16be(nud)
                nud.seek(20,1)
                for x in range(texPropCount):
                    typeNum = readByte(nud)
                    fightNum = readByte(nud)
                    playNum = readByte(nud)
                    texNum = readByte(nud)
                    if(texNum > 0 and texNum <= 127):
                        texNum = texNum
                    elif(texNum >= 128 and texNum <= 255):
                        texNum = texNum - 128
                    if(typeNum != 0x10):
                        nud.seek(-4,1)
                        nud.write(struct.pack("B", baseID))
                        nud.write(struct.pack("B", groupID))
                        nud.write(struct.pack("B", subgroupID))
                        nud.write(struct.pack("B", offsetID + texNum))
                        typeNum = readByte(nud)
                        fightNum = readByte(nud)
                        playNum = readByte(nud)
                        texNum = readByte(nud)
                    nud.seek(20,1)
                headerRead = 0x20
                while headerRead == 0x20:
                    headerRead = readu32be(nud)
                    texPropNameStart = readu32be(nud)
                    nud.seek(24,1)
                    backUp = nud.tell()
                    nud.seek(nameClumpStart + texPropNameStart)
                    texPropName = getString(nud)
                    nud.seek(backUp)
            if texturePropertiesL4Start_array[z] != 0:
                nud.seek(texturePropertiesL2Start_array[z])
                nud.seek(8,1)
                texSomethingCount = readu16be(nud)
                texPropCount = readu16be(nud)
                nud.seek(20,1)
                for x in range(texPropCount):
                    typeNum = readByte(nud)
                    fightNum = readByte(nud)
                    playNum = readByte(nud)
                    texNum = readByte(nud)
                    if(texNum > 0 and texNum <= 127):
                        texNum = texNum
                    elif(texNum >= 128 and texNum <= 255):
                        texNum = texNum - 128
                    if(typeNum != 0x10):
                        nud.seek(-4,1)
                        nud.write(struct.pack("B", baseID))
                        nud.write(struct.pack("B", groupID))
                        nud.write(struct.pack("B", subgroupID))
                        nud.write(struct.pack("B", offsetID + texNum))
                        nud.seek(-4,1)
                        typeNum = readByte(nud)
                        fightNum = readByte(nud)
                        playNum = readByte(nud)
                        texNum = readByte(nud)
                    nud.seek(20,1)
                headerRead = 0x20
                while headerRead == 0x20:
                    headerRead = readu32be(nud)
                    texPropNameStart = readu32be(nud)
                    nud.seek(24,1)
                    backUp = nud.tell()
                    nud.seek(nameClumpStart + texPropNameStart)
                    texPropName = getString(nud)
                    nud.seek(backUp)
    return True

def IDFixNut(path,baseID,groupID,subgroupID,offsetID):
    with open(path,"rb+") as nut:
        NTWU = readu32be(nut)
        Version = readu16be(nut)
        fileTotal = readu16be(nut)
        nut.seek(0x10)
        paddingFix = 0
        for i in range(fileTotal):
            if i > 0:
                paddingFix = paddingFix + headerSize
            fullSize = readu32be(nut)
            nut.seek(4,1)
            size = readu32be(nut)
            headerSize = readu16be(nut)
            nut.seek(2,1)
            mipsFlag = readu16be(nut)
            gfxFormat = readu16be(nut)
            if NTWU == 0x4E545755:
                width = readu16be(nut)
                height = readu16be(nut)
            if NTWU == 0x4E545033:
                width2 = readByte(nut)
                width1 = readByte(nut)
                height2 = readByte(nut)
                height1 = readByte(nut)
            numOfMips = readu32be(nut)
            nut.seek(4,1)
            offset1 = (readu32be(nut) + 16)
            offset2 = (readu32be(nut) + 16)
            offset3 = (readu32be(nut) + 16)
            nut.seek(4,1)
            if headerSize == 0x60:
                size1 = readu32be(nut)
                nut.seek(12,1)
            if headerSize == 0x70:
                size1 = readu32be(nut)
                nut.seek(0x1C,1)
            if headerSize == 0x80:
                size1 = readu32be(nut)
                nut.seek(0x2C,1)
            if headerSize == 0x90:
                size1 = readu32be(nut)
                nut.seek(0x3C,1)
            eXt = readu32be(nut)
            nut.seek(12,1)
            GIDX = readu32be(nut)
            nut.seek(7,1)
            texNum = readByte(nut)
            nut.seek(-4,1)
            nut.write(struct.pack("B", baseID))
            nut.write(struct.pack("B", groupID))
            nut.write(struct.pack("B", subgroupID))
            nut.write(struct.pack("B", (texNum % 128) + offsetID))
            nut.seek(-4,1)
            typeNum = readByte(nut)
            fightNum = readByte(nut)
            skinNum = readByte(nut)
            fileNum = readByte(nut)
            nut.seek(4,1)
    return True
