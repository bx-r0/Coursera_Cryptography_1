from Crypto.Cipher import AES
import random
import codecs
import string
import base64
import sys
import re
import os

class Conversion():

    @staticmethod
    def remove_byte_notation(string):
        """
        Forceful way of removing the byte notation
        """
        return str(string)[2:-1]
class HexTo():
    @staticmethod
    def base64(string):
        """
        Hex --> Base64
        """

        # Ensures the hex value has the correct number of digits
        if len(string) % 2 is not 0:
            string = "0" + string

        input_bytes = codecs.decode(string, 'hex')
        return base64.b64encode(input_bytes)

    @staticmethod
    def utf8(string):
        """
        Hex --> UTF-8
        """

        b = codecs.decode(string, 'hex')
        return codecs.decode(b, 'utf-8')

    @staticmethod
    def binary(string):
        """
        Binary --> Hex
        """

        return bin(string)[2:]

    @staticmethod
    def utf8_check(string):
        """
        Checks a hex value produces a valid UTF-8 string
        """
        try:
            _ = codecs.decode(codecs.decode(string, 'hex'), 'utf-8')
            return True
        except Exception:
            return False
class Base64_To():
    @staticmethod
    def hexadecimal(string):
        """
        Base64 --> Hex
        """
        hexBytes = base64.b64decode(string)
        return codecs.encode(hexBytes, 'hex')

    @staticmethod
    def rawBytes(string):
        """
        Decodes a base64 value
        """
        return base64.b64decode(string)

    @staticmethod
    def utf8(string):
        """
        Base64 --> UTF-8
        """
        b = base64.b64decode(string)
        return b.decode('utf-8')

    @staticmethod
    def binary(string):
        """
        Base64 --> Binary
        """

        return bin(int(base64.b64decode(string).hex(), 16))[2:]

    @staticmethod
    def concat(inputList):
        """
        Combines a list of base64 values in a single value
        """

        byteValues = b""
        for x in inputList:
            byteValues += base64.b64decode(x)

        return base64.b64encode(byteValues)
class UTF8_To():
    @staticmethod
    def hexadecimal(string):
        """
        Converts an utf-8 string to a hex string
        """
        b = codecs.encode(string, 'utf-8')
        return codecs.encode(b, 'hex')

    @staticmethod
    def base64(string):
        """
        Converts an utf-8 string to a base64 string
        """
        return base64.b64encode(string.encode('utf-8'))

class XOR():

    @staticmethod
    def b64_Xor(a, b):
        """
        Produces an XOR Result of two equal length Base64 encoded values
        """

        bytesA = base64.b64decode(a)
        bytesB = base64.b64decode(b)

        result = XOR.bytesXor(bytesA, bytesB)

        return base64.b64encode(result)

    @staticmethod
    def hexXor(a, b):
        """
        Produces an XOR result of two equal length Hex values
        """

        # Finds the longest length
        # And pads the shortest
        length = 0
        difference = abs(len(a) - len(b))

        if len(a) > len(b):
            length = len(a)

            b = ("00" * difference) + b
        else:
            length = len(b)
            a = ("00" * difference) + a


        binA = bin(int(a, 16))[2:].zfill(length)
        binB = bin(int(b, 16))[2:].zfill(length)

        xor = int(binA, 2) ^ int(binB, 2)

        # Format ensures that the hex values are always the same length
        hexOutput = format(xor, f"#0{length + 2}x")[2:]

        return hexOutput

    @staticmethod
    def bytesXor(a, b):
        result = []
        for b1, b2 in zip(a, b):
            result.append(bytes([b1 ^ b2]))

        result = b"".join(result)
        return result

def splitBase64IntoBlocks(string, blocksize=16):
    """
    Takes a base64 string and returns a list of certain length blocks
    """

    # Converts to hex
    hexString = Conversion.remove_byte_notation(Base64_To.hexadecimal(string))

    hexBytes = re.findall("..", hexString)

    # Adds padding if the lengths are not equal
    while len(hexBytes) % blocksize != 0:
        hexBytes.append("00")

    chunks = []
    for x in range(0, len(hexBytes), blocksize):
        chunk = ""

        for i in range(x, x + blocksize):
            chunk += hexBytes[i]
        chunks.append(HexTo.base64(chunk))

    return chunks
