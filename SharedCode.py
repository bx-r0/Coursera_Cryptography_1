import re
import base64
import binascii

def splitHexIntoBlocks(hexValue, blocksize):

    pattern = "." + "{" + str(blocksize) + "}"

    hexBytes = re.findall(pattern, hexValue)

    if len(hexValue) % blocksize != 0:
        # Finds the length of the last block
        diff = len(hexValue) - len(hexBytes) * blocksize
        t = hexValue[len(hexValue) - diff:]
        hexBytes.append(t)

    return hexBytes


# Conversions
def hex_to_base64(hexString):
    return base64.b64encode(binascii.unhexlify(hexString))

def base64_to_hex(base64String):
    return base64.b64decode(base64String).hex()
