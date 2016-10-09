from util import *
from Meme import MemeGate


def AddonHook(userInput):
    if userInput == 'gfd':
        pass
    else: MemeGate(userInput)

def AddonInfoPrint():
    #print 'To replace missing portraits with silhouettes, type "silhouette" and press ENTER. (requires addon SIL)'
    print "To open the integration with GFD's Inject Pack, type " + '"GFD"' + ' and press ENTER. (requires addon GFD)'
    print 'To view a list of addons which will add functionality to the script, type "addons" and press ENTER.'
