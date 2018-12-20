import urllib3
import urllib
import base64
import sys
import re
import sys

# Imports custom shared code
sys.path += ["..", "."]
import Function

# Global vars
http = urllib3.PoolManager()

TARGET = 'http://crypto-class.appspot.com/po?er='
cipherText =  Function.HexTo.base64(
    "f20bdba6ff29eed7b046d1df9fb7000058b1ffb4210a580f748b4ac714c001bd4a61044426fb515dad3f21f18aa577c0bdf302936266926ff37dbf7035d5eeb4"
)
#--------------------------------------------------------------
# padding oracle
#--------------------------------------------------------------
class PaddingOracle():
    def query(self, q):
        target = TARGET + urllib.parse.quote(q)
        r = http.request("GET", target) 
        
        # Good padding
        if r.status == 404 or r.status == 200:
            return True

        # Bad Padding 
        return False

def findPaddingLength(cipherText, oracle):
    """
    Discovers the padding length of the cipher text.
    It works by affecting the penultimate bytes to therefore affect the byte with padding.
    If a byte containing padding is corrupted we can therefore determine where the padding starts
    and therefore how long it is
    """

    # Discover padding length
    targetBlock = -2

    # Works it way through the entire byte
    for x in range(16):

        blocks = Function.splitBase64IntoBlocks(cipherText)
        blockBytes = Function.splitBase64IntoBlocks(blocks[targetBlock], 1)
        
        # Random change to that byte
        blockBytes[x] = Function.XOR.b64_Xor(blockBytes[x], base64.b64encode(b"x"))

        # Saves any changes made to the blocks
        blocks[targetBlock] = Function.Base64_To.concat(blockBytes)
        cipherTextPrime = Function.Base64_To .concat(blocks)
        cipherTextPrimeHex = Function.Base64_To.hexadecimal(cipherTextPrime)

        if not oracle.query(cipherTextPrimeHex):
            return 16 - x

def removeLastBlock(cipherText):
    """
    Chops off the last block of the ciphertext
    """

    t = Function.splitBase64IntoBlocks(cipherText)[:-1]
    return Function.Base64_To.concat(t)

def generatePad(cipherText, length):
    numberOfBytes = len(Function.splitBase64IntoBlocks(cipherText, blocksize=1))

    base64Null = base64.b64encode(b"\x00")

    # Generates the new pad
    # It has to be the previous block from the target block
    # This is due to how CBC mode is designed
    pad = [base64Null] * (numberOfBytes - length - 16)
    pad += [base64.b64encode(bytes([length]))] * length
    pad += [base64Null] * (16)

    return Function.Base64_To.concat(pad)

def addDiscoveredPadding(cipherTextLen, paddingLength):

    discoveredCipherText = [base64.b64encode(b"\x00")] * (cipherTextLen - paddingLength - 16)
    discoveredCipherText += [base64.b64encode(bytes([paddingLength]))] * paddingLength
    discoveredCipherText += [base64.b64encode(b"\x00")] * (16)

    return discoveredCipherText

def task():
    global cipherText
    po = PaddingOracle()

    answer = ""

    # Determines padding length
    paddingLength = findPaddingLength(cipherText, po)
    if paddingLength == 16:
        cipherText = removeLastBlock(cipherText)
        paddingLength = 1

    numberOfBlocks = len(Function.splitBase64IntoBlocks(cipherText, 16))

    cipherTextLen = len(Function.splitBase64IntoBlocks(cipherText, 1))

    # Generates a discovered ciphertext pad (Including any padding found)
    # The pad has to be on the previous block so an extra block of zeros are added
    discoveredCipherText = addDiscoveredPadding(cipherTextLen, paddingLength)

    targetByte = cipherTextLen - 1 - 16 - paddingLength # Previous block

    # Moves along to the next value
    paddingLength += 1

    # Skips through padding variables of the block
    blockDiscovered = paddingLength - 1

    for _ in range(numberOfBlocks - 1):

        while blockDiscovered < 16:

            # Generates a pad
            pad = generatePad(cipherText, paddingLength)

            # Char choice
            for x in range(0, 256):
                b64Char = base64.b64encode(bytes([x]))

                discoveredCipherText[targetByte] = b64Char
                discoveredCipherTextString = Function.Base64_To.concat(discoveredCipherText)

                # Manipulates the ciphertext
                xor = Function.XOR.b64_Xor(discoveredCipherTextString, pad)
                cipherTextPrime = Function.XOR.b64_Xor(cipherText, xor)

                if po.query(Function.Base64_To.hexadecimal(cipherTextPrime)):
                    answer += chr(x)
                    break
            else:
                raise(Exception("Cannot find correct byte!"))
    
            paddingLength += 1
            targetByte -= 1
            blockDiscovered += 1

            print(answer[::-1], end="\r")

        # Resets the padding and removes a discovered block
        cipherText = removeLastBlock(cipherText)
        cipherTextLen = len(Function.splitBase64IntoBlocks(cipherText, 1))
        paddingLength = 1

        # Rests discovered variables
        discoveredCipherText = [base64.b64encode(b"\x00")] * cipherTextLen
        blockDiscovered = 0

    # Final answer
    print(answer[::-1])


if __name__ == "__main__":
    print()
    po = PaddingOracle()
    task()
