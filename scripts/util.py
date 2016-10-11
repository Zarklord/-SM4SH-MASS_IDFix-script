import struct
import msvcrt as m
import time
import os

import fixpath
from colorama import init, Fore, Back, Style

def wait(wait=-1):
    """waits for user input before continuing"""
    if wait == -1:
        m.getch()
    else:
        time.sleep(wait)

def errorCode(message):
    """prints a message in red"""
    print Fore.RED + message + Fore.RESET

def infoCode(message):
    """prints a message in green"""
    print Fore.GREEN + message + Fore.RESET
 
def readByte(file):
    return struct.unpack("B", file.read(1))[0]
 
def readu16be(file):
    return struct.unpack(">H", file.read(2))[0]
 
def readu16le(file):
    return struct.unpack("<H", file.read(2))[0]

def readu32be(file):
    return struct.unpack(">I", file.read(4))[0]
 
def readu32le(file):
    return struct.unpack("<I", file.read(4))[0]
 
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

init()
configPath = os.path.abspath(".\\config")
configFile = configPath + "\\config.txt"
