# Imports custom shared code
import sys
sys.path += ["..", "."]
import Function
import string
import re

targetCipherText = "32510ba9babebbbefd001547a810e67149caee11d945cd7fc81a05e9f85aac650e9052ba6a8cd8257bf14d13e6f0a803b54fde9e77472dbff89d71b57bddef121336cb85ccb8f3315f4b52e301d16e9f52f904"

def hexXor(a, b):
        """
        Produces an XOR result of two equal length Hex values
        """

        # Finds the longest length
        # And truncates the longest
        length = 0
        if len(a) > len(b):
            length = len(b)

            a = a[:len(b)]
        else:
            length = len(a)
            b = b[:len(a)]

        xor = int(a, 16) ^ int(b, 16)

        # Format ensures that the hex values are always the same length
        hexOutput = format(xor, f"#0{length + 2}x")[2:]

        # Evens the value
        if len(hexOutput) % 2 != 0:
            hexOutput = "0" + hexOutput

        return hexOutput

def loadData():

    with open("./Week_1/data.txt") as file:
        lines = file.readlines()

    # Removes \n
    return list(map(str.strip, lines))

data = loadData()

# Positions of known key
knownKey = [0] * 500
answer = ""

# First it checks for position of plaintext that are spaces
    # This is because C1 ⊕ C2 = P1 ⊕ P2 and if P1 or P2 is a space the result will be 
    # an upper or lowercase character

    # For example:
    #   V ⊕ ' ' = v

# The fact that we known the plain text is a space allows us the retrieve the key bit. This
# is because:
#   C ⊕ K = P
#       ==
#   P ⊕ C = K
for current_index, ciphertext in enumerate(data):

    # Number of times a space has been found in this position
    knownSpaces = [0] * len(ciphertext)
    knownIndices = [False] * 500

    for index, ciphertext2 in enumerate(data):

        # Stops self comparason
        if index != current_index:
            
            xorBytes = bytes.fromhex(hexXor(ciphertext, ciphertext2))

            for charIndex, char in enumerate(xorBytes):

                # Converts to string
                c = chr(char)

                # If the XOR result contains a alpha char we can
                # predicts that one of the plaintext values is a space 
                if c.isalpha() and c in string.printable:
                        knownSpaces[charIndex] += 1


    # Loops through the positions to check for positions with 
    # a high chance of being a space
    for index, spaceCount in enumerate(knownSpaces):
        
        # Out of a possible 9
        if spaceCount >= 7:
            knownIndices[index] = True

    # Now discover the key bit
    #   - 20 is hex for a space
    xorWithSpaces = bytes.fromhex(hexXor(ciphertext, "20" * len(ciphertext)))
    for index, knownSpacePosition in enumerate(knownIndices):

        if knownSpacePosition:
            k =  xorWithSpaces[index]
            keyHex = hex(k)[2:].zfill(0)
            knownKey[index] = keyHex

# The discovered key bits are then XORed against the target cipher text
cipherTextBytes = re.findall("..", targetCipherText) # Splits hex into bytes
for k, c in zip(knownKey, cipherTextBytes): 

    # Ignores positions key has not been found
    if k != 0:

        # XORs ciphertext with key
        byte = bytes.fromhex(hexXor(k, c))
        answer += byte.decode('utf-8')
    else:
        answer += "*"

# The answer is patchy by you can manually piece together the answer
print(answer)