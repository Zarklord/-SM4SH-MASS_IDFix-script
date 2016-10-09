from __future__ import unicode_literals
import os
import sys
import zlib
import msvcrt as m
import glob
import webbrowser as wb
from distutils.dir_util import copy_tree
import shutil

sys.path.insert(0,os.path.abspath(".\\scripts"))
from util import *
from Hook import CaptainHook,TheWorks,HookInfoPrint,TheWorksInfo

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
    for folder in glob.glob(os.path.abspath(".\\workspace\\content\\patch\\data\\fighter") + '\\*'):
        print folder[len(os.path.abspath(".\\workspace\\content\\patch\\data\\fighter")) + 1:]

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
    print "smb123w64gb: wrote the original TexIDfix.py"
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
        sys.exit()
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
    #calls the hooks section which will call the addons section which will call the memes section
    else: CaptainHook(userInput)

    UI()

if not os.path.exists(os.path.abspath(".\\backup")):
    os.mkdir(os.path.abspath(".\\backup"))
if not os.path.exists(os.path.abspath(".\\exempt")):
    os.mkdir(os.path.abspath(".\\exempt"))
    
UI()
