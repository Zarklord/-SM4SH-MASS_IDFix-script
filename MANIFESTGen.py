import os
import hashlib

def hashFile(manifest,filepath,outputName):
    with open(filepath,'rb+') as f:
        buf = f.read()
        hasher = hashlib.sha256()
        hasher.update(buf)
        fileHash = hasher.hexdigest().upper()
        manifest.write(outputName + ',' + fileHash + '\r\n')

manifest = open(os.path.abspath(".\\MANIFEST.mf"),'wb+')
hashFile(manifest,os.path.abspath('.\\_Mass TexIDFix.py'),'_Mass TexIDFix.py')
for root, dirs, files in os.walk(os.path.abspath(".\\scripts")):
    for name in files:
        if name.endswith(".py"):
            hashFile(manifest,os.path.join(root, name),os.path.join(root, name)[len(os.path.abspath(".\\"))+1:].replace("\\","/"))
