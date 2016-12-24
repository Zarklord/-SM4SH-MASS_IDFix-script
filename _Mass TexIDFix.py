from __future__ import unicode_literals
import os
import sys
import zlib
import msvcrt as m
import glob
import webbrowser as wb
from distutils.dir_util import copy_tree
import shutil
import urllib
import hashlib

missingScripts = False
try:
    sys.path.insert(0,os.path.abspath(".\\scripts"))
    from util import *
    from Hook import CaptainHook,TheWorks,HookInfoPrint,TheWorksInfo
except ImportError:
    if os.path.exists(os.path.abspath(".\\TexIDfix.py")):
        os.remove(os.path.abspath(".\\TexIDfix.py"))
    if os.path.exists(os.path.abspath(".\\TexIDfix-NUD.py")):
        os.remove(os.path.abspath(".\\TexIDfix-NUD.py"))
    missingScripts = True
    
majorVersion = "3"
minorVersion = "0"
revision = "09"
branch = ''
fighterpath = os.path.abspath(".\\workspace\\content\\patch\\data\\fighter")
mtbpath = os.path.abspath(".\\workspace\\content\\patch\\data\\sound\\config\\fightermodelbanktable.mtb")


def backup():
    if os.path.exists(os.path.abspath(".\\backup\\content")):
        infoCode("Removing old backup...")
        shutil.rmtree(os.path.abspath(".\\backup\\content"))
        infoCode("Done!")
        print
    infoCode("Making backup now.")
    fromDirectory = os.path.abspath(".\\workspace")
    toDirectory = os.path.abspath(".\\backup")
    copy_tree(fromDirectory, toDirectory)
    infoCode("Success! Workspace Folder is now backed up.")
    print

def debug():
    while True:
        print
        print 'Debug mode activated. Type the name of a function with the necessary arguments and then press ENTER to run it.'
        print 'Only use this if you know what you are doing.'
        print 'To exit debug mode, type "exit" press ENTER.'
        print
        userInput = raw_input("Enter a python command:")
        print
        if userInput == 'exit':
            break
        elif userInput == 'UI()':
            break
        try:
            eval(userInput)
        except:
            print
            errorCode("Not Valid Python Code")
            print

def list():
    infoCode("List of all fighter folders with mods installed: ")
    for folder in glob.glob(fighterpath + '\\*'):
        print folder[len(fighterpath) + 1:]

def readConfig():
    global branch
    global fighterpath
    global mtbpath
    with open(configPath + "\\config.txt",'rb+') as f:
        for line in f:
            if not line.startswith("#"):
                if line.startswith("branch="):
                    branch = line.split('=')[-1].rstrip()
                if line.startswith("fighterfolderpath="):
                    fighterpath = os.path.abspath(line.split('=')[-1].rstrip())
                if line.startswith("mtbfilepath="):
                    mtbpath = os.path.abspath(line.split('=')[-1].rstrip())

def configDownload():
    if not os.path.exists(os.path.abspath(".\\config")):
        os.mkdir(os.path.abspath(".\\config"))
    if branch == 'unstable':
        branchPath = 'https://raw.githubusercontent.com/Zarklord1/-SM4SH-MASS_IDFix-script/unstable'
    else:
        branchPath = 'https://raw.githubusercontent.com/Zarklord1/-SM4SH-MASS_IDFix-script/master'
    configsPath = os.path.abspath(".\\config") + "\\configList.txt"
    urllib.urlretrieve(branchPath + "/config/configList.txt", configsPath)
    with open(configsPath,'rb+') as f:
        for line in f:
            if not os.path.exists(os.path.abspath(".\\config") + "\\" + line.rstrip()):
                urllib.urlretrieve(branchPath + "/config/" + line.rstrip(), os.path.abspath(".\\config") + "\\" + line.rstrip())
    os.remove(configsPath)

def restart():
    os.startfile(sys.argv[0])
    sys.exit(0)

def updateVersion():
    if not os.path.exists(os.path.abspath(".\\scripts")):
        os.mkdir(os.path.abspath(".\\scripts"))
    if branch == 'unstable':
        branchPath = 'https://raw.githubusercontent.com/Zarklord1/-SM4SH-MASS_IDFix-script/unstable'
    else:
        branchPath = 'https://raw.githubusercontent.com/Zarklord1/-SM4SH-MASS_IDFix-script/master'

    manifestPath = "scriptlist.txt"
    urllib.urlretrieve(branchPath + "/scriptlist.txt", manifestPath)
    with open(manifestPath, 'rb+') as f:
        for line in f:
            if len(line) > 0:
                splitLines = line.rstrip().split(",")
                hasher = hashlib.sha256()
                Ifile = branchPath + "/" + splitLines[0]
                Hfile = os.path.abspath(".\\") + "\\" + splitLines[0].replace("/","\\")
                direct = Hfile[:-(len(Hfile.split("\\")[-1])+1)]
                if not os.path.exists(direct):
                    os.mkdir(direct)
                if not os.path.exists(Hfile):
                    urllib.urlretrieve(Ifile, Hfile)
                else:
                    with open(Hfile, 'rb+') as check:
                        buf = check.read()
                        hasher.update(buf)
                        fileHash = hasher.hexdigest().upper()
                    if fileHash != splitLines[1].upper():
                        os.remove(Hfile)
                        urllib.urlretrieve(Ifile, Hfile)
    os.remove(manifestPath)
    restart()

def versionCheck():
    versionCheckFile = configPath + "version.txt"
    if branch == 'unstable':
        branchPath = 'https://raw.githubusercontent.com/Zarklord1/-SM4SH-MASS_IDFix-script/unstable'
    else:
        branchPath = 'https://raw.githubusercontent.com/Zarklord1/-SM4SH-MASS_IDFix-script/master'
    try:
        urllib.urlretrieve(branchPath + "/version.txt", versionCheckFile)
    except:
        errorCode("ERROR: not connected to the internet!")
        return None
    with open(versionCheckFile, 'rb+') as f:
        lines = f
        majorVersionCheck = int(f.next().rstrip().split("=")[-1])
        minorVersionCheck = int(f.next().rstrip().split("=")[-1])
        revisionCheck = int(f.next().rstrip().split("=")[-1])

    os.remove(versionCheckFile)

    if int(majorVersion) < majorVersionCheck:
        infoCode("WARNING: you are running a MUCH older version of the script!")
        input = raw_input("do you want to update y/n?")
        while input != 'y' or input != 'n':
            print "INVALID Input!"
            input = raw_input("do you want to update y/n?")
        if input == 'y':
            updateVersion()
    elif int(minorVersion) < minorVersionCheck:
        infoCode("WARNING: you are running an older version of the script!")
        input = raw_input("do you want to update y/n?")
        while input != 'y' or input != 'n':
            print "INVALID Input!"
            input = raw_input("do you want to update y/n?")
        if input == 'y':
            updateVersion()
    elif int(revision) < revisionCheck:
        updateVersion()
            

def credits():
    print
    print 'Munomario: original maker of script, frontend'
    print
    print 'Zarklord: optimiser, backend, Auto_MTB_Tool,'
    print 'all 4 ids changeable in TexIDfix, rewrite to python'
    print
    print 'Bluedan: modified the mta creator script that jam wrote, for mta id fixing'
    print
    print "jam1garner: RE'd mta, also wrote the original mta creator script,"
    print "co-wrote the original mtb editing script with soneek, and"
    print "wrote some of the code in the auto mtb script"
    print
    print "soneek: RE'd mtb, helped write the mtb code"
    print 'used in the original editor and the auto one'
    print
    print 'GFD: better error handling of packed/corrupted nuds/nuts for the TexIDfix.py'
    print
    print 'DSX8(DONT ask for help/ping): helped jam on mta research stuff'
    print
    wait(5)

def UI():
    global errorCount
    errorCount = 0
    print
    print '---------------------------------------'
    print '   Automatic Mass TexIDFix v3.0 Beta'
    print '       by Munomario and Zarklord'
    print '---------------------------------------'
    print

    if not os.path.isdir(os.path.abspath('.\\workspace\\content\\patch\\data\\fighter')):
	    errorCode('WARNING This script is in the wrong place.')
	    errorCode('Place the files from the download into the main sm4shexplorer folder.')
	    errorCode('Alternatively the workspace folder may have the wrong name. It must be called workspace.')
	    print

    print 'This script will automatically fix the IDs of any skins that are in your workspace folder.'
    print "Make sure that this script is placed inside Sm4shExplorer's main folder, along with the other files!"
    print 'Also make sure that all the skins you want to fix have both model.nud and model.nut.'
    print
    print "Also, you can do some other stuff with this too. Here's a list of commands:"
    print
    print 'to list all fighters with mods installed type "list" and press ENTER'
    print 'to back up your workspace type "backup" and press ENTER'
    print "To view the script's page on Gamebanana, type " + '"gamebanana"' + " and press ENTER."
    print 'To launch Sm4shExplorer, type "explorer" and press ENTER. (requires addon S4E)'
    print 'to know who to thank for this to be possible type "credits" and press ENTER'
    print 'to see the current version you are on type "version" and press ENTER'
    print
    print 'to ' + TheWorksInfo() + ', launch Explorer, and then close this script, type "theworks" and press ENTER.'
    print
    HookInfoPrint()
    print
    print "To end the script, type 'exit' and press ENTER."
    print
    userInput = raw_input("your choice: ").lower()
    print


    if userInput == 'theworks':
        infoCode("On it.")
        print
        TheWorks()
        os.startfile(".\\Sm4shFileExplorer.exe")
        exit()
    elif userInput == 'exit':
        sys.exit(0)
    elif userInput == 'list':
        list()
        wait(2)
    elif userInput == 'gamebanana':
        wb.open_new_tab("http://gamebanana.com/gamefiles/4689")
    elif userInput == 'explorer':
        os.startfile(".\\Sm4shFileExplorer.exe")
        print "Didn't work? Make sure the .exe is still called Sm4shFileExplorer.exe!"
    elif userInput == 'debug':
        debug()
    elif userInput == 'backup':
        backup()
    elif userInput == 'credits':
        credits()
    elif userInput == 'version':
        print "Your version is: " + majorVersion + "." + minorVersion + "-R" + revision
        wait(3)
    #calls the hooks section which will call the addons section which will call the memes section
    else: CaptainHook(userInput)

    UI()

if missingScripts == True:
    configDownload()
    updateVersion()

if not os.path.exists(os.path.abspath(".\\backup")):
    os.mkdir(os.path.abspath(".\\backup"))
if not os.path.exists(os.path.abspath(".\\exempt")):
    os.mkdir(os.path.abspath(".\\exempt"))

configDownload()
readConfig()
versionCheck()
UI()

