import os

configList = open(os.path.abspath(".\\configCheck.txt"),'wb+')

for root, dirs, files in os.walk(os.path.abspath(".\\")):
    for name in files:
        if not name.endswith(".py") and not name.endswith(".swp") and not name.endswith(".un~") and not name.endswith(".py~"):
            configList.write(name + "\r\n")
