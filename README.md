<img align="right" src="./logo.png">

# Coursera - Cryptography 1
This repository contains the programming assignments for Dan Boneh's Cryptography I course.

## Week 1 - Many time pad
This programming assignment involved the cracking of 10 ciphertexts that had been encrypted using the same one time pad. 

This assignment was designed to show that a one-time pad should only be used once.


## Week 2 - AES
The assignment involved implementing AES in CBC and CTR mode.


## Week 3 - Hashing
Week 3's assignment was to build a hashing scheme that verified data in chunks. A use case for this is streaming services that need to verify data as it is being downloaded. SHA256 was used as the hashing algorithm.


## Week 4 - CBC Padding Oracle Attack
This assignment was one of the most interesting. We were provided with a 'toy' website that verified a ciphertext. If the decryption failed and the website releases information about what error has occurred (padding invalid in this case) it forms what is known as a 'padding oracle'. This small leak of information can be enough to fully encrypt the ciphertext!

This is known as a [padding oracle attack](https://help.github.com/articles/about-readmes/).


## Week 5 - Discrete Modulo Log
This weeks assignment was a [Meet in the middle](https://en.wikipedia.org/wiki/Meet-in-the-middle_attack) attack to compute a Discrete Modular Log. It involved basic number theory knowledge and is a good example of constructing a Meet in the Middle attack.


## Week 6 - RSA
The final week involved cracking faulty modular values of an RSA key. If the values of p and q that construct N are too close, it can make it very trivial to factorise N. By factoring N you can construct the private key.