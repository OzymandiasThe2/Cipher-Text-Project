# Encryption/Decryption
A project made using various different types of encryption keys and methods.
This is a game where you enter a message and the program will encrypt the message. The user will continue to enter messages till they deside to exit, to exit the user enters STOP. Once the user enters STOP the program will show the encrypted, decrypted message. It will also show the algorithmic method used to encrypt the message.

## Encryption/Decryption Methods Used
- Columnar Transposition 
- Substitution 
- Rivest–Shamir–Adleman (RSA), default Prime Numbers are: 103, 157
- Playfair
- Caesar, shifted 3
- Product, uses 1 substitution then 1 transposition 

## Things that dont work
- Substitution seems to crash sometimes, not sure whats causing that
  - Product will crash if substitution doesnt work right.
- RSA crashes if the inputted text is too large. This is an easy fix, it requires the default prime number to be made bigger.


## TODO
- I'm not sure why we made it spit of ciphers randomly, but fix it so it just spits out all variants and or let user choose which cipher to work with
- Make a working GUI
  - Certain things like Ceasar Shifts, and RSA Prime Numbers, configurable
- Figure out why sometimes substitution randomly crashes


