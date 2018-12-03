from Crypto.Cipher import AES
import base64
import re
import binascii

# Conversions
def hex_to_base64(hexString):
    return base64.b64encode(binascii.unhexlify(hexString))
def base64_to_hex(base64String):
    return base64.b64decode(base64String).hex()

# Encryption function
def split_base64_into_blocks(string, number):
    """
    Takes a base64 string and returns a list of certain length blocks
    """

    # Converts to hex
    hex = base64_to_hex(string)
    bytes = re.findall("..", hex)

    # Adds padding if the lengths are not equal
    while len(bytes) % number != 0:
        bytes.append("00")

    chunks=[]
    for x in range(0, len(bytes), number):
        chunk=""

        for i in range(x, x + number):
            chunk += bytes[i]
        chunks.append(hex_to_base64(chunk))

    return chunks
def xor_base64(a, b):
    bytesA = base64.b64decode(a)
    bytesB = base64.b64decode(b)

    result = []
    for b1, b2 in zip(bytesA, bytesB):
        result.append(bytes([b1 ^ b2]))
    
    result = b"".join(result)

    return base64.b64encode(result)
def AES_decrypt_block(key, data):
    """
    Works with base64 encoded data
    """

    cipher = AES.new(key, AES.MODE_ECB)
    e = cipher.decrypt(base64.b64decode(data))
    return base64.b64encode(e)
def AES_encrypt_block(key, data):
    """
    Works with base64 encoded data
    """

    cipher = AES.new(key, AES.MODE_ECB)
    e = cipher.encrypt(base64.b64decode(data))
    return base64.b64encode(e)


# CBC
def CBC_Decrypt(iv, key, data, blocksize=16):

    blocks = split_base64_into_blocks(data, blocksize)
    previous = iv
    plainText = []

    for block in blocks:
        
        # Decrypts the data
        d = AES_decrypt_block(key, block)
        
        pt = xor_base64(previous, d)

        plainText.append(base64.b64decode(pt))

        previous = block

    resultBytes = b"".join(plainText)
    result = str(resultBytes)[2:-1]
    #result = result.rstrip('\\x08')

    return result

# CTR
def CTR_Decrypt(iv, key, data, blocksize=16):

    # TODO - What proportion is it iv to counter?

    plaintext = []
    nonce = iv
    blocks = split_base64_into_blocks(data, 16)

    for block in blocks:
        d = AES_encrypt_block(key, nonce)

        pt = base64.b64decode(xor_base64(blocks[0], d))

        # Increment
        ivBytes = bytearray(base64.b64decode(iv))
        ivBytes[15] += 1
        iv = base64.b64encode(ivBytes)
        nonce = iv

        plaintext.append(pt)

    print()

def decrypt(key, cipherText, func):

    ct = cipherText[32:]
    iv = cipherText[:32]

    # Key needs to be raw bytes
    key = base64.b64decode(hex_to_base64(key))
    iv = hex_to_base64(iv)
    data = hex_to_base64(ct)

    result = func(iv, key, data)
    print(result)
    print()

print("> Question 1")
ct = "4ca00ff4c898d61e1edbf1800618fb2828a226d160dad07883d04e008a7897ee2e4b7465d5290d0c0e6c6822236e1daafb94ffe0c5da05d9476be028ad7c1d81"
k = "140b41b22a29beb4061bda66b6747e14"
decrypt(k, ct, CBC_Decrypt)

print("> Question 2")
ct = "5b68629feb8606f9a6667670b75b38a5b4832d0f26e1ab7da33249de7d4afc48e713ac646ace36e872ad5fb8a512428a6e21364b0c374df45503473c5242a253"
k = "140b41b22a29beb4061bda66b6747e14"
decrypt(k, ct, CBC_Decrypt)

print("> Question 3")
ct = "69dda8455c7dd4254bf353b773304eec0ec7702330098ce7f7520d1cbbb20fc388d1b0adb5054dbd7370849dbf0b88d393f252e764f1f5f7ad97ef79d59ce29f5f51eeca32eabedd9afa9329"
k = "36f18357be4dbd77f050515c73fcf9f2"
decrypt(k, ct, CTR_Decrypt)

print("> Question 4")
ct = "770b80259ec33beb2561358a9f2dc617e46218c0a53cbeca695ae45faa8952aa0e311bde9d4e01726d3184c34451"
k = "36f18357be4dbd77f050515c73fcf9f2"
decrypt(k, ct, CTR_Decrypt)