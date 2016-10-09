# coding: utf-8
from __future__ import absolute_import,unicode_literals
import random, binascii



def makeValueValid(lowest,highest,userInput,string,divisible):
        returnInput = userInput
        mathValue = len(string)
        #adjust value if its lower than "lowest"
        while returnInput < lowest and returnInput < highest:
                if returnInput + mathValue > highest:
                        mathValue = mathValue / divisible
                        while returnInput + mathValue > highest:
                                mathValue = mathValue / divisible
                returnInput += mathValue
        
        #adjust value if its higher than "highest"
        while returnInput > highest and returnInput > lowest:
                if returnInput - mathValue < lowest:
                        mathValue = mathValue / divisible
                        while returnInput - mathValue < lowest:
                                mathValue = mathValue / divisible
                returnInput -= mathValue

        return returnInput


class HashOutput(bytearray):
        def hexdigest(self):
                return binascii.hexlify(self).decode(u'ascii')


                        
                        
class PearsonHasher(object):

        def __init__(self, length, seed = u'Î‘Î“Î•Î©ÎœÎ•Î¤Î¡Î—Î¤ÎŸÎ£ ÎœÎ—Î”Î•Î™Î£ Î•Î™Î£Î™Î¤Î©'):
                self.length = length
                generator = random.Random()
                generator.seed(seed)
                self.table = range(256)
                generator.shuffle(self.table)


        def hash(self, data):
                result = HashOutput()
                for byte in xrange(self.length):
                        h = self.table[(ord(data[0]) + byte) % 256]
                        for c in data[1:]:
                                h = self.table[h ^ ord(c)]
                        result.append(h)
                return result
