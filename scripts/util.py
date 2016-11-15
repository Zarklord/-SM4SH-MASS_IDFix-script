import struct
import msvcrt as m
import time
import os

import fixpath
from colorama import init, Fore, Back, Style

branch = ''
fighterpath = os.path.abspath(".\\workspace\\content\\patch\\data\\fighter")
mtbpath = os.path.abspath(".\\workspace\\content\\patch\\data\\sound\\config\\fightermodelbanktable.mtb")

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

def update(file):
    file.seek(0,1)
 
def readByte(file):
    return struct.unpack("B", file.read(1))[0]

def writeByte(file,b):
    file.write(struct.pack("B", b))
    update(file)
 
def readu16be(file):
    return struct.unpack(">H", file.read(2))[0]
 
def readu16le(file):
    return struct.unpack("<H", file.read(2))[0]

def readu32be(file):
    return struct.unpack(">I", file.read(4))[0]
 
def readu32le(file):
    return struct.unpack("<I", file.read(4))[0]

def write32be(file,u32):
    file.write(struct.pack(">I", u32))
    update(file)

def write32le(file,u32):
    file.write(struct.pack("<I", u32))
    update(file)
 
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

init()
configPath = os.path.abspath(".\\config")
readConfig()