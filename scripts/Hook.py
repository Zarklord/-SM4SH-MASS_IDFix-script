import os
import shutil
import msvcrt as m

from util import *
import Mass_Fighter_IDFix as fighterFix
from Addons import AddonHook,AddonInfoPrint
from Auto_MTB_Tool import autoIDFix

def CaptainHook(userInput):
    if userInput == '':
        fighterFix.IdFixAllFighters(fighterpath)
        exempt()
    elif userInput == 'exemptinfo':
        print "The exempt feature allows you to exclude certain skins from the mass idfix."
        print "This means that if idfixing a skin breaks it, you can just exclude it from the idfix to avoid breaking the skin."
        print 'To enable it, place the mod files you want to exclude inside the "exempt" folder.'
        print 'Make sure to include the full file structure, as if the exempt folder were your workspace folder.'
        print 'Also, be aware that it only applies if you choose to idfix all characters at once.'
        print 'But, you can activate it at any time by typing "exempt" and pressing ENTER.'
        wait(2)
    elif userInput == 'mtb':
        autoIDFix(mtbpath,fighterpath,configPath)
        wait(2)
    elif userInput == 'exempt':
        exempt()
    elif userInput in allFighterFolders:
        print "please type the name of the folder you want to IDFix"
        print 'or type "all" to fix all folders for a given fighter'
        print 'or "extra" to fix all folders besides the "body" folder'
        print
        secondInput = raw_input("Your choice: ")
        print
        if userInput == 'kamui':
            print "YOU MADE YOUR CHOICE!"
            print
        fighterFix.IDFixFighter(fighterpath + "\\" + userInput,secondInput)
    else: AddonHook(userInput)


        
def TheWorks():
    '''users typing "theworks" will run all the data in here before running sm4sh explorer and closing the script'''
    fighterFix.IdFixAllFighters(fighterpath)
    autoIDFix(mtbpath,fighterpath,configPath)
    exempt()

def TheWorksInfo():
    """returns the info for the stuff done in TheWorks()"""
    return 'fix all characters, voice banks'

def HookInfoPrint():
    #print the info pertaining to hooks
    print 'To fix all characters, press ENTER.'
    print "To fix a specific character, type the character's internal name and press ENTER."
    print 'To fix all characters voice banks from muting type "mtb" and press ENTER.'
    print 'To view information about the exempt feature, type "exemptinfo" and press ENTER.'
    print
    #print the info pertaining to addons
    AddonInfoPrint()

def exempt():
    exempt = os.path.abspath(".\\exempt")
    workspace = os.path.abspath(".\\workspace")
    infoCode("Copying exempted files over workspace")
    if os.path.exists(exempt + "\\content"):

        for root, dirs, files in os.walk(exempt):
            workspaceRoot = workspace + root[len(exempt):]

            if not os.path.exists(workspaceRoot):
                os.mkdir(workspaceRoot)
                
            for name in files:
                if os.path.exists(os.path.join(workspaceRoot,name)):
                    os.remove(os.path.join(workspaceRoot,name))
                shutil.copy2(os.path.join(root,name),os.path.join(workspaceRoot,name))
        infoCode("Finished copying exempted files over workspace.")

allFighterFolders = []
with open(configPath + "\\fighters.csv") as f:
    for line in f:
        if "," in line:
            stringLine = line.split(",")
            allFighterFolders.append(stringLine[0].rstrip())
        else:
            allFighterFolders.append(line.rstrip())


