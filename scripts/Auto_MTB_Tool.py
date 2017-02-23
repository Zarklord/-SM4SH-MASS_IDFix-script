import struct
import binascii
import sys
import os
import string
import zlib
import glob
import re
import msvcrt as m
try:
    from colorama import init, Fore, Back, Style
except:
    coloraImported = False
else:
    coloraImported = True

def errorCode(message):
    """prints a message in red"""
    if coloraImported:
        print Fore.RED + message + Fore.RESET
    else:
        print message

def wait():
    m.getch()

def readByte(file):
        return struct.unpack("B", file.read(1))[0]

def readu16be(file):
        return struct.unpack(">H", file.read(2))[0]

def readu16le(file):
        return struct.unpack("<H", file.read(2))[0]

def readu32be(file):
        return struct.unpack(">I", file.read(4))[0]

def readu64be(file):
        return struct.unpack(">q", file.read(8))[0]

def readu32le(file):
        return struct.unpack("<I", file.read(4))[0]

def writeu32le(file,u32):
        file.write(struct.pack("<I",u32))

def readfloatbe(file):
        return struct.unpack(">f", file.read(4))[0]

def readfloatle(file):
        return struct.unpack("<f", file.read(4))[0]

def getString(file):
        result = ""
        tmpChar = file.read(1)
        while ord(tmpChar) != 0:
                result += tmpChar
                tmpChar =file.read(1)
        return result

def getNUS3Type(NUS3Name):
        if "_se" in NUS3Name and "_common" in NUS3Name:
                return 4
        elif "_vc" in NUS3Name and "_ouen" in NUS3Name:
                return 3
        elif "_vc" in NUS3Name and "_se" not in NUS3Name and "_ouen" not in NUS3Name:
                return 2
        elif "_se" in NUS3Name and "_vc" not in NUS3Name and "_common" not in NUS3Name:
                return 1
        else:
                return 5

def getNUS3ID(NUS3Name):
        isCXX = False
        defaultInternalID = 0
        search = re.search("_c([0-9]{2,3})",NUS3Name)
        NUS3NameNoCXX = ""
        if search:
                isCXX = True
                NUS3NameNoCXX = NUS3Name[:search.start()] + NUS3Name[search.end():]
        with open(NUSIDSDBPath + "NUS3-IDs.db",'rb+') as f:
                for line in f:
                        if NUS3Name in line and line[len(NUS3Name)] == ":":
                                return (int(line[len(NUS3Name) + 1:]),int(line[len(NUS3Name) + 1:]))
                        if isCXX and NUS3NameNoCXX in line and line[len(NUS3NameNoCXX)] == ":":
                                defaultInternalID = int(line[len(NUS3NameNoCXX) + 1:])
        if isCXX:
                customInternalID = int(search.group(1))
                return ((customInternalID << 16) + defaultInternalID, defaultInternalID)
        return (None, None)

def getFighterName(filename):
    nameFighter = filename[7:-9]
    fighterSearch = re.search("_c([0-9]{2,3})",nameFighter)
    if fighterSearch:
        nameFighter = nameFighter[:fighterSearch.start()] + nameFighter[fighterSearch.end():]
    fighterSearch = re.search("_common",nameFighter)
    if fighterSearch:
        nameFighter = nameFighter[:fighterSearch.start()] + nameFighter[fighterSearch.end():]
    fighterSearch = re.search("_copy_",nameFighter)
    if fighterSearch:
        nameFighter = nameFighter[fighterSearch.end():]
    return nameFighter
    
class nus3bank(object):
        contents = []
        propOffset = 0
        binfOffset = 0
        grpOffset = 0
        dtonOffset = 0
        toneOffset = 0
        junkOffset = 0
        packOffset = 0
        def __init__(self, size):
                self.size = size


def getNusbankIdInfo(fname):
                nus3 = open(fname, 'rb+')
                if nus3.read(4) != "NUS3":
                                nus3.seek(0)
                                data = nus3.read()
                                nus3_decom = zlib.decompress(data)
                                nus3.close()
                                nus3 = open(fname, 'wb+')
                                nus3.write(nus3_decom)
                                nus3.seek(0)
                                data = None
                                nus3_decom = None
                else:
                                nus3.seek(0)

                assert nus3.read(4) == "NUS3"
                size = readu32le(nus3)

                bank = nus3bank(size)
                assert nus3.read(8) == "BANKTOC ", "Not a bank archive!"
                tocSize = readu32le(nus3)
                contentCount = readu32le(nus3)
                offset = 0x14 + tocSize
                for i in range(contentCount):
                                content = nus3.read(4)
                                contentSize = readu32le(nus3)
                                if content == "PROP":
                                                propOffset = offset
                                                propSize = contentSize
                                elif content == "BINF":
                                                binfOffset = offset
                                                binfSize = contentSize
                                elif content == "GRP ":
                                                grpOffset = offset
                                                grpSize = contentSize
                                elif content == "DTON":
                                                dtonOffset = offset
                                                dtonSize = contentSize
                                elif content == "TONE":
                                                toneOffset = offset
                                                toneSize = contentSize
                                elif content == "JUNK":
                                                junkOffset = offset
                                                junkSize = contentSize
                                elif content == "MARK":
                                                markOffset = offset
                                                markSize = contentSize
                                elif content == "PACK":
                                                packOffset = offset
                                                packSize = contentSize
                                offset += 8 + contentSize

                nus3.seek(binfOffset)
                assert nus3.read(4) == "BINF"
                assert readu32le(nus3) == binfSize
                assert readu32le(nus3) == 0
                assert readu32le(nus3) == 3
                binfStringSize = readByte(nus3)
                binfString = nus3.read(binfStringSize-1)
                nus3.seek(1,1)
                #print binfString
                padding = (binfStringSize + 1) % 4
                #print padding
                if padding == 0:
                                pass
                else:
                                nus3.seek(abs(padding-4), 1)
                nusIdPos = nus3.tell()
                nus3ID = readu32le(nus3)
                #print hex(nus3ID)

                nus3.seek(toneOffset)
                assert nus3.read(4) == "TONE"
                assert readu32le(nus3) == toneSize
                toneCount = readu32le(nus3)
                nus3.close()
                return (nus3ID,nusIdPos)



class Mtb:
        def __init__(self,fname):
                self.filename = fname
                self.header = "\x4D\x54\x42\x00\x01\x00\x00\x00"
                self.entries = []
                entry = []
                entry.append("")
                entry.append(2045)
                entry.append(getNUS3Type("_se"))
                entry.append(1)
                entry.append([2046])
                self.addNewEntry(entry)
                entry = []
                entry.append("")
                entry.append(2052)
                entry.append(getNUS3Type("_se_common"))
                entry.append(1)
                entry.append([2053])
                self.addNewEntry(entry)
                entry = []
                entry.append("")
                entry.append(2133)
                entry.append(getNUS3Type("_se"))
                entry.append(1)
                entry.append([2134])
                self.addNewEntry(entry)
                entry = []
                entry.append("")
                entry.append(2135)
                entry.append(getNUS3Type("_se_common"))
                entry.append(1)
                entry.append([2136])
                self.addNewEntry(entry)
                entry = []
                entry.append("")
                entry.append(2138)
                entry.append(getNUS3Type("_se"))
                entry.append(1)
                entry.append([2139])
                self.addNewEntry(entry)
                entry = []
                entry.append("")
                entry.append(6039)
                entry.append(getNUS3Type("_vc"))
                entry.append(1)
                entry.append([6045])
                self.addNewEntry(entry)
                entry = []
                entry.append("")
                entry.append(6051)
                entry.append(getNUS3Type("_vc"))
                entry.append(1)
                entry.append([6056])
                self.addNewEntry(entry)
                entry = []
                entry.append("")
                entry.append(6059)
                entry.append(getNUS3Type("_vc"))
                entry.append(1)
                entry.append([6060])
                self.addNewEntry(entry)
                entry = []
                entry.append("")
                entry.append(6062)
                entry.append(getNUS3Type("_vc"))
                entry.append(7)
                entry.append([6063,6064,6065,6066,6067,6068,6069])
                self.addNewEntry(entry)
                entry = []
                entry.append("")
                entry.append(6133)
                entry.append(getNUS3Type("_vc_ouen"))
                entry.append(7)
                entry.append([6135,6136,6137,6138,6139,6140,6141])
                self.addNewEntry(entry)
                entry = []
                entry.append("")
                entry.append(6100)
                entry.append(getNUS3Type("_vc_ouen"))
                entry.append(1)
                entry.append([6142])
                self.addNewEntry(entry)
                entry = []
                entry.append("")
                entry.append(6165)
                entry.append(getNUS3Type("_vc"))
                entry.append(1)
                entry.append([6166])
                self.addNewEntry(entry)
                entry = []
                entry.append("")
                entry.append(6170)
                entry.append(getNUS3Type("_vc"))
                entry.append(1)
                entry.append([6171])
                self.addNewEntry(entry)

        def recalcTable(self):
                self.offsetStart = (len(self.entries) * 0x4) + 0x10
                self.offsetTable = []
                currentOffset = 0
                for i in self.entries:
                        self.offsetTable.append(currentOffset)
                        currentOffset += 0x1A + (0x4 * i[3])

        def addNewEntry(self,newEntry):
                self.entries.append(newEntry)
                self.recalcTable()

        def getEntry(self,entryNum):
                if entryNum < len(self.entries):
                        return self.entries[entryNum]
                return None

        def modifiyExistingEntry(self,entryNum,entry):
                if entryNum != -1:
                        self.entries[entryNum] = entry
                        return 0
                return -1

        def removeEntry(self,entryNumber):
                del self.entries[entryNumber]
                self.recalcTable()

        def findByDefaultInternalAndNusType(self,defaultInternal,nusType):
                entryCount = 0;
                for entry in self.entries:
                        if defaultInternal == entry[1] and nusType == entry[2]:
                                return entryCount
                        entryCount += 1
                return -1

        def save(self):
                self.recalcTable()
                self.entryCount = len(self.entries)
                with open(self.filename,'wb') as f:
                        f.write(self.header)
                        f.write(struct.pack('<L',self.entryCount))
                        f.write(struct.pack('<L',self.offsetStart-0x10))
                        for i in self.offsetTable:
                                f.write(struct.pack('<L',i))
                        for i in self.entries:
                                name,defaultInternal,nusType,nusCount,internalIds = i
                                f.write(name)
                                f.write(((0x10-len(name)) * chr(0)))
                                f.write(struct.pack('<L',defaultInternal))
                                f.write(struct.pack('<H',nusType))
                                f.write(struct.pack('<H',nusCount))
                                for j in internalIds:
                                        f.write(struct.pack('<L',int(j)))
                                f.write(chr(0)*2)

def EntryEdit(fighterName,InternalId,nusType,customNusId,entryNum,cXXSlot,mtb):
        if entryNum == -1:
            #entry doesnt exist in the current mtb
            customInternalIds = []
            for soundBankSlot in range(cXXSlot):
                if soundBankSlot == cXXSlot - 1:
                        customInternalIds.append(customNusId)
                else:
                        customInternalIds.append(InternalId)
            entry = [fighterName,InternalId,nusType,cXXSlot,customInternalIds]
            mtb.addNewEntry(entry)
        else:
            #existing entry
            entry = mtb.getEntry(entryNum)
            if entry[3] - 1 < cXXSlot - 1:
                internalIds = entry[4]
                while len(internalIds) < cXXSlot - 1:
                    internalIds.append(InternalId)
                internalIds.append(customNusId)
            else:
                internalIds = entry[4]
                internalIds[cXXSlot - 1] = customNusId
            entry[3] = len(internalIds)
            entry[4] = internalIds
        mtb.modifiyExistingEntry(entryNum, entry)

def autoIDFix(path,workspaceDir,nusIdsPath=os.path.abspath('.\\')):
    global NUSIDSDBPath
    NUSIDSDBPath = nusIdsPath + "\\"
    print "Auto MTB Fixer 1.2 By Zarklord. Original MTB Editor made by soneek and jam1garner"
    #make the directory
    mtbdir = path[:-(len(path.split("\\")[-1])+1)]
    if not os.path.exists(mtbdir):
        os.makedirs(mtbdir)
    mtb = Mtb(path)
    for fighterName in glob.glob(workspaceDir + '\\*'):
            currentFighterDir = fighterName + '\\sound'
            if os.path.exists(currentFighterDir):
                    print "Starting: " + fighterName.split("\\")[-1].title() + " Mtb Id Fixing..."
                    for filename in os.listdir(currentFighterDir):
                            if filename.endswith('.nus3bank'):
                                    nameFighter = getFighterName(filename)
                                    currentSoundFile = currentFighterDir + '\\' + filename
                                    nusId,nusIdPos = getNusbankIdInfo(os.path.abspath(currentSoundFile.strip('"').strip("'")))
                                    correctNusId,defaultNusId = getNUS3ID(filename)
                                    correctNusType = getNUS3Type(filename)
                                    if correctNusId != nusId:
                                            nus = open(os.path.abspath(currentSoundFile.strip('"').strip("'")),'r+b')
                                            nus.seek(nusIdPos)
                                            writeu32le(nus,correctNusId)
                                            nus.close()
                                    entryNum = mtb.findByDefaultInternalAndNusType(defaultNusId,correctNusType)
                                    search = re.search("_c([0-9]{2,3})",filename)
                                    cXXSlot = None
                                    if search:
                                            cXXSlot = int(search.group(1))
                                    if cXXSlot:
                                        if cXXSlot == 0:
                                                errorCode("You cant Have a c00 nus3bank! SKIPPING...")
                                                print "You Might Have Muting Issue's Because of this nus3bank..."
                                        else:       
                                                EntryEdit(nameFighter,defaultNusId,correctNusType,correctNusId,entryNum,cXXSlot,mtb)
                                    cXXSlot = None
                    print "Finished: " + fighterName.split("\\")[-1].title() + " Mtb Id Fixing!"
    mtb.save()


NUSIDSDBPath = ''
if __name__ == "__main__":
    autoIDFix(os.path.abspath(".\\workspace\\content\\patch\\data\\sound\\config\\fightermodelbanktable.mtb"),os.path.abspath(".\\workspace\\content\\patch\\data\\fighter"))
    print "press any key to exit..."
    wait()
