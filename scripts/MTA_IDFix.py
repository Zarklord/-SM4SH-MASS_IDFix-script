# coding: utf-8
import struct
import sys
import os
import string
import zlib
import msvcrt as m

"""
Script to edit texture id's within mta files.
Most mta code "stolen" from jam1garner.
TexIdFixing by BlueDan: Pac Man + Robin now texIdFixable
Thanks to Zarklord for explaining me how offsetIDs work and auto decompressing invalid mta's
"""

def wait():
    """waits for user input before continuing"""
    m.getch()

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

def uint8(file):
    # return struct.unpack('B',file.read(1))[0]
    return ord(file.read(1))

def uint32(file):
    return struct.unpack('>I',file.read(4))[0]

def writeuint8(file,i):
    file.write(struct.pack('B',i))

def writeuint32(file,i):
    file.write(struct.pack('>I',i))

def eof(mta):
    returnTo = mta.tell()
    mta.seek(0,2)
    eof = mta.tell()
    mta.seek(returnTo)
    return eof

class MtaHeader:
    def __init__(self,mta=None):
        if mta:
            self.magic = mta.read(4)
            self.unknown = uint32(mta)
            self.numFrames = uint32(mta)
            mta.seek(4,1)#padding
            self.frameCountMinusOne = uint32(mta)
            self.frameRate = uint32(mta)
            self.matCount = uint32(mta)
            self.matOffset = uint32(mta)
            self.visCount = uint32(mta)
            self.visOffset = uint32(mta)
            mta.seek(self.matOffset)
            self.matOffsets = []
            for i in range(self.matCount):
                self.matOffsets.append(uint32(mta))
            mta.seek(self.visOffset)
            self.visOffsets = []
            for i in range(self.visCount):
                self.visOffsets.append(uint32(mta))

def editTexIdsPataData(file,mainID,fighterID,texID,offsetID):
    fulldefaultframeID = uint32(file)
    file.seek(-4,1)
    writeuint32(file,mainID*0x1000000 + fighterID*0x10000 + texID*0x100 + (fulldefaultframeID % 0x80) + offsetID)
    '''
    writeuint8(file,mainID)
    writeuint8(file,fighterID)
    writeuint8(file,texID)
    # file.seek(1,1)
    file.read(1) # read is writing? wtf?!?
    # defaultFrameID = (uint8(file) % 0x80) + offsetID
    # file.seek(-1,1)
    # writeuint8(file,defaultFrameID)
    '''
    # print file.tell()
    keyframeCount = uint32(file)
    # print hex(keyframeCount)
    # exit()
    keyframesOffset = uint32(file)
    # print hex(keyframesOffset)
    file.seek(8,1)
    if keyframesOffset != eof(file):
        file.seek(keyframesOffset)
        for i in range(keyframeCount):
            fullframeID = uint32(file)
            file.seek(-4,1)
            writeuint32(file,mainID*0x1000000 + fighterID*0x10000 + texID*0x100 + (fullframeID % 0x80) + offsetID)
            '''
            writeuint8(file,mainID)
            writeuint8(file,fighterID)
            writeuint8(file,texID)
            file.seek(1,1)
            # frameID = (uint8(file) % 0x80) + offsetID
            # file.seek(-1,1)
            # writeuint8(file,frameID)
            '''
            file.seek(4,1)
def checkTexIdsPataData(file):
    ids = [{}]
    ids[0]["mainID"] = uint8(file)
    ids[0]["fighterID"] = uint8(file)
    ids[0]["texID"] = uint8(file)
    ids[0]["defaultFrameID"] = uint8(file)
    print "mainID: " + str(ids[0]["mainID"]) + " | fighterID: " + str(ids[0]["fighterID"]) + " | texID: " + str(ids[0]["texID"]) + " | defaultFrameID: " + str(ids[0]["defaultFrameID"])
    keyframeCount = uint32(file)
    keyframesOffset = uint32(file)
    file.seek(8,1)
    if keyframesOffset != eof(file):
        file.seek(keyframesOffset)
        for i in range(keyframeCount):
            idf ={}
            idf["mainID"] = uint8(file)
            idf["fighterID"] = uint8(file)
            idf["texID"] = uint8(file)
            idf["frameID"] = uint8(file)
            ids.append(idf)
            print "mainID: " + str(idf["mainID"]) + " | fighterID: " + str(idf["fighterID"]) + " | texID: " + str(idf["texID"]) + " |        frameID: " + str(idf["frameID"])
            file.seek(4,1)
    print ''
    return ids

def editTexIdsMatEntry(file,mainID,fighterID,texID,offsetID):
    file.seek(16,1)
    hasPat = ord(file.read(1))
    file.seek(3,1)
    patOffset = uint32(file)
    if hasPat:
        file.seek(patOffset)
        patDataPos = uint32(file)
        if patDataPos != 0:
            file.seek(patDataPos)
            editTexIdsPataData(file,mainID,fighterID,texID,offsetID)
            if patDataPos != patOffset+4: # doing this because otherwise parsing Rosa's powerstar doesn't work
                file.seek(patOffset+4)
                patDataPos2  = uint32(file)
                if patDataPos2 != 0:
                    file.seek(patDataPos2)
                    editTexIdsPataData(file,mainID,fighterID,texID,offsetID)
def checkTexIdsMatEntry(file):
    ids=[]
    file.seek(16,1)
    hasPat = ord(file.read(1))
    file.seek(3,1)
    patOffset = uint32(file)
    if hasPat:
        file.seek(patOffset)
        patDataPos = uint32(file)
        if patDataPos != 0:
            file.seek(patDataPos)
            ids=checkTexIdsPataData(file)
            if patDataPos != patOffset+4: # doing this because otherwise parsing Rosa's powerstar doesn't work
                file.seek(patOffset+4)
                patDataPos2  = uint32(file)
                if patDataPos2 != 0:
                    file.seek(patDataPos2)
                    ids.extend(checkTexIdsPataData(file))
    return ids

def editTexIdsMtafile(file,mainID,fighterID,texID,offsetID):
    if file.read(4) != '':
        file.seek(0)
        for off in MtaHeader(file).matOffsets:
            file.seek(off)
            editTexIdsMatEntry(file,mainID,fighterID,texID,offsetID)
def checkTexIdsMtafile(file):
    ids=[]
    if file.read() != '':
        file.seek(0)
        for off in MtaHeader(file).matOffsets:
            file.seek(off)
            ids.extend(checkTexIdsMatEntry(file))

def mtaFix_edit(folder,mainID,fighterID,texID,offsetID):
    doDecompedversion = None
    for (path,dirs,files) in os.walk(folder):
        for file in files:
            if file.endswith(".mta"):
                with open(os.path.join(path,file),"r+b") as f:
                    if f.read(4) == 'MTA4':
                        f.seek(0)
                        editTexIdsMtafile(f,mainID,fighterID,texID,offsetID)
                    else:
                        doDecompedversion = checkAndDecompress(os.path.join(path,file))
                if doDecompedversion:
                    with open(os.path.join(path,file),"r+b") as f:
                        editTexIdsMtafile(f,mainID,fighterID,texID,offsetID)
                    
# def mtaFix_rebuild(folder,mainID,fighterID,texID,offsetID):
    # for (path,dirs,files) in os.walk(folder):
        # for file in files:
            # if file[-4:] == ".mta":
                # with open(os.path.join(path,file),"rb") as mta_in:
                    # m = MtaFile(mta_in)
                # m.setTexIDs(mainID,fighterID,texID,offsetID)
                # with open(os.path.join(path,file),"wb") as mta_out:
                    # m.save(mta_out)

def mtaFix(folder,mainID,fighterID,texID,offsetID):
    mtaFix_edit(folder,mainID,fighterID,texID,offsetID)
    # mtaFix_rebuild(folder,mainID,fighterID,texID,offsetID)

def check(folder):
    d = {}
    for (path,dirs,files) in os.walk(folder):
        print "Looking for MTA files in "+path
        for file in files:
            filepath = os.path.join(path,file)
            if string.lower(file[-4:]) == ".mta":
                print "Checking IDs in "+filepath
                with open(filepath,"rb") as f:
                    d[filepath]=checkTexIdsMtafile(f)
    return d

if __name__ == "__main__":
    if len(sys.argv) == 1:
        print "To check IDs of MTAs in a folder have that folder as only argument"
        print "\t"+os.path.basename(__file__)+" fightername\\model\\body\\cXX"
        print "To edit IDs of MTAs in a folder, provide as well typeID (64 for characters), secondaryID (character specific), textureID (model-slot specific) and an offsetID (either 0 or 128)"
        print "Note that when TexIdFixing characters, for every \"fightername\\model\\modelname\\cXX\" model-slot folder, *.nud, *.nut and *.mta files within this folder and subfolders should use the same quadruplet (typeID,secondaryID,textureID,offsetID) and that no distinct model-slot folders share the same quadruplets (however \"fightername\\model\\body\\cXX\" and \"fightername\\model\\body\\lXX\" folders for the same slot do share the same quadruplet)."
        print "\t"+os.path.basename(__file__)+" fightername\\model\\body\\cXX 64 74 42 0"
        wait()
        exit()
    folder = sys.argv[1]
    if len(sys.argv) < 3:
        check(folder)
    else:
        mainID = int(sys.argv[2])
        fighterID = int(sys.argv[3])
        texID = int(sys.argv[4])
        offsetID = int(sys.argv[5])

        mtaFix(folder,mainID,fighterID,texID,offsetID)
