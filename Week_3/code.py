import os
import sys
sys.path.insert(0, ".")
from Crypto.Hash import SHA256
import Function

"""
Task description can be found in description.txt
"""

def loadVideoFile(fileName):

    path = os.path.realpath(__file__)
    pathSections = path.split("/")
    del pathSections[-1] # Deletes the file name

    pathName =  "/".join(pathSections)

    data = None
    with open(f'{pathName}/{fileName}.mp4', "rb") as file:
        data = file.read()
    return data

if __name__ == "__main__":
    data = loadVideoFile("intro").hex()

    # Breaks into kilobytes - 2048 chars due to the data being hex represented 
    blocks = Function.splitHexIntoBlocks(data, 2048)

    # Reverses the list to compute the hash
    blocks = blocks[::-1]

    append = ""
    for b in blocks:
        hexBytes = bytes.fromhex(b + append)

        append = SHA256.new(hexBytes).hexdigest()

    # h0 is the last hash
    h0 = append

    # Prints h0
    print(f"{h0}")