# Names: Nicholas Hughes(100743493), Khalid Hafizi(100754554), Franklin Muhuni(10074490),
# Chris McGill(100745212), Shriji Shah(100665031)
# Date: March 29 2020
# Description: This is a game where you enter a message and the program will encript the message. The user will
# continue to enter messages till they deside to exit, to exit the user enters STOP. Once the user enters STOP the
# program will show the encrypted, decrypted message. It will also show the algorithmic method used to encrypt the
# message.

from abc import ABC, abstractmethod  # imports abstract base class.
import random  # imports random library.


class Message:  # message class.
    def __init__(self, string=""):
        self._string = string  # string.
        self._key1 = list("etaoinshrdlcumwfgypbvkjzxq")  # sub key.
        self._key2 = "hope"  # transposition key.
        self._alpha = list("abcdefghijklmnopqrstuvwxyz")  # alphabet.
        self._modulus = 0  # RSA encryption and decryption.
        self._privateKey = 0
        self._publicKey = 0
        self._key3 = list("ROLEX")  # playfair key
        self._key4 = 3  # caesar cipher key

    @abstractmethod
    def display(self):  # abstract base class.
        pass

    def delete(self):  # deleter.
        del self._string

    def set_message(self, message):  # setter.
        self._string = message

    def get_message(self, message):  # getter.
        return self._string

    # USED FOR RSA ENCRYPTION AND DECRYPTION
    # greatest common divisor
    def gcd(self, a, b):
        while b:
            a, b = b, a % b
        return a

    # USED FOR RSA ENCRYPTION AND DECRYPTION / key creation for RSA
    def get_keys(self):
        # arbitrary prime numbers chosen, it could be any prime numbers
        prime_num1 = 103
        prime_num2 = 157
        # modulus = p*q
        self._modulus = prime_num1 * prime_num2
        # public exponent = (p-1)*(q-1)
        public_exponent = (prime_num1 - 1) * (prime_num2 - 1)

        public_keys = []
        for x in range(public_exponent):
            if self.gcd(x, public_exponent) == 1:
                public_keys.append(x)
        self._publicKey = public_keys[4]

        # private exponent = (e*d-1)/[(p-1)*(q-1)] =>
        # (publicKey * privateKey - 1) % public exponent == 0
        # to calculate the private key
        self._privateKey = 0
        x = -1
        while x != 0:
            self._privateKey += 1
            x = (self._publicKey * self._privateKey - 1) % public_exponent

    # USED FOR PLAYFAIR ENCRYPTION AND DECRYPTION
    def playfair_key(self):
        alpha = list(x.upper() for x in self._alpha)
        alpha.pop(alpha.index("J"))  # removes j
        grid = []  # local variables.
        temp = []
        encrypt = []

        for x in self._key3:  # if letter in key matches with one in alphabet then its poped from the alphabet
            for char in alpha:
                if x == char:
                    alpha.pop(alpha.index(char))

        temp += self._key3 + alpha  # temp value

        for x in range(0, 25, 5):  # makes the grid 5 by 5
            grid.append(list(temp[0 + x: 5 + x]))

        for x in range(0, len(self._string), 2):  # makes the strings into 2 letter lists.
            encrypt.append(list(self._string[0 + x: 2 + x]))

        return grid, encrypt

    # USED FOR PLAYFAIR ENCRYPTION AND DECRYPTION
    def playfair_postion(self):
        grid, encrypt = self.playfair_key()
        result = list()  # local variables.
        result2 = list()
        result3 = list()

        for y in encrypt:  # Gets positon of the letters and appends to results.
            for x in grid:
                if y[0] in x:
                    result.append([grid.index(x), x.index(y[0])])
                if y[1] in x:
                    result2.append([grid.index(x), x.index(y[1])])

        for x in range(len(result)):  # adds the first x elements of each list together.
            result3.append([result[x], result2[x]])

        return result3, grid  # returns result and grid


class PlaintextMsg(Message):  # to encrypt text.
    def __init__(self, string=""):
        super().__init__(string)
        self._encrypt = []  # holds encrypted word.

    def display(self):  # displays encrypted message.
        print("Encrypted Message:", self._encrypt)

    def substitution_encryption(self):
        # lowers each value in the sting list, then appends the alpha postion of the key into the encrypt list.
        x = list(self._string)
        for char in x:
            char.lower()
            if char.isalpha():
                self._encrypt.append(self._key1[self._alpha.index(char)])
            else:
                self._encrypt.append(char)

        self._encrypt = "".join(self._encrypt)
        return self._encrypt  # returns the encrypted value.

    def transposition_encryption(self):  # Columnar Transposition Cipher encryption method.
        x = dict()  # encoding dictionary.
        string = list(self._string)  # string list.
        start = 0  # position value.

        for val in range(len(self._key2)):  # adds spaces to the list if its not divisible by length of the key.
            if not len(string) % len(self._key2) == 0:
                string.append(" ")
            else:
                pass

        for val in self._key2:  # dictionary initialization
            x.setdefault(val, list())

        for dkey in self._key2:  # for every value of the key saves every 4th letter into each position.
            for pos in range(start, len(string), len(self._key2)):
                x[dkey].append(string[pos])
            start += 1

        for val in sorted(self._key2):  # saves string values to z in alphabetical order.
            self._encrypt += x[val]

        self._encrypt = "".join(self._encrypt)  # creates a string from the list.
        return self._encrypt  # returns the string

    def product_encryption(self):  # uses 1 substitution then 1 transposition which is a product method.
        self._string = self.substitution_encryption()  # applies substitution encryption.
        self._encrypt = []  # erases value.
        self._encrypt = self.transposition_encryption()  # applies transposition encryption.
        return self._encrypt  # returns string.

    # Encryption using the ASCII letters
    def rsa_encryption(self):
        self.get_keys()  # creates the key.
        string_chars = [ord(character) for character in self._string]
        self._encrypt = ''.join([chr(letter ** self._publicKey % self._modulus) for letter in string_chars])
        return self._encrypt  # returns string.

    def playfair_encryption(self):
        self._string = list(self._string.upper().replace(" ", ""))  # removes spaces.

        for x in range(len(self._string) * 2):  # checks if there is two letter beside eachother and adds x.
            try:
                if self._string[x] == self._string[x + 1]:
                    self._string.insert(x + 1, "X")
            except:
                pass

        if len(self._string) % 2 != 0:  # if not divisible by 2 append x.
            self._string += "X"

        position, grid = self.playfair_postion()  # gets position

        for pos in range(len(position)):  # gets new position cords.
            if position[pos][0][0] == position[pos][1][0]:  # Rule 1 if some row move right 1.
                if position[pos][0][1] == 4:
                    self._encrypt.append(grid[position[pos][0][0]][position[pos][0][1] - 4])  # at max so goes to start.
                else:
                    self._encrypt.append(grid[position[pos][0][0]][position[pos][0][1] + 1])  # moves over 1.

                if position[pos][1][1] == 4:
                    self._encrypt.append(grid[position[pos][1][0]][position[pos][1][1] - 4])  # at max so goes to start.
                else:
                    self._encrypt.append(grid[position[pos][1][0]][position[pos][1][1] + 1])  # moves over 1.

            elif position[pos][0][1] == position[pos][1][1]:  # Rule 1 if some column move down 1.
                if position[pos][0][0] == 4:
                    self._encrypt.append(grid[position[pos][0][0] - 4][position[pos][0][1]])  # at max so goes to start.
                else:
                    self._encrypt.append(grid[position[pos][0][0] + 1][position[pos][0][1]])  # moves down 1.

                if position[pos][1][0] == 4:
                    self._encrypt.append(grid[position[pos][1][0] - 4][position[pos][1][1]])  # at max so goes to start.
                else:
                    self._encrypt.append(grid[position[pos][1][0] + 1][position[pos][1][1]])  # moves down 1.

            else:
                self._encrypt.append(grid[position[pos][0][0]][position[pos][1][1]])  # swaps corners
                self._encrypt.append(grid[position[pos][1][0]][position[pos][0][1]])

        self._encrypt = "".join(self._encrypt)  # creates a string
        return self._encrypt  # returns encrypted value

    def caesar_encryption(self):  # method which actually encrypts the users message
        alpha = "".join(self._alpha)  # string alphabet
        x = len(self._string)  # gets the length of the users message
        self._encrypt = ''  # blank string to contain encrypted message

        for n in range(x):  # for loop which iterates through each character and encrypts it
            if self._string[n].isalpha():  # ensures character is in the alphabet
                char_i = self._string[n].lower()  # makes the character lower case
                position = alpha.find(char_i)  # finds the character within the alphabet string
                new_position = (position + self._key4) % 26  # uses the cipher encryption formula to shift the character
                self._encrypt += alpha[new_position]  # adds the new character  to the encrypted message
            elif self._string[n] == " ":  # if whitespace is detected, a white space is simply added
                self._encrypt += " "
            else:  # for any other type of character the program simply skips it
                pass

        return self._encrypt  # returns the encrypted message


class CiphertextMsg(Message):  # to decrypt text.
    def __init__(self, string=""):
        super().__init__(string)
        self._decrypt = []

    def display(self):  # displays decrypted message.
        print("Original Message:", self._decrypt)

    def substitution_decryption(self):
        # lowers each value in the sting list, then appends the key postion of the alpha into the decrypt list.
        x = list(self._string)
        for char in x:
            char.lower()
            if char.isalpha():
                self._decrypt.append(self._alpha[self._key1.index(char)])
            else:
                self._decrypt.append(char)

        self._decrypt = "".join(self._decrypt)  # creates string.
        return self._decrypt  # returns decrypted value.

    def transposition_decryption(self):  # Columnar Transposition Cipher decryption method.
        x = dict()  # local variables.
        string = list(self._string)
        start = 0

        for val in sorted(self._key2):
            x.setdefault(val, list())

        for dkey in sorted(self._key2):  # for every value of the sorted key saves every n letter in each dkey.
            for pos in range(int(len(string) / len(self._key2))):
                x[dkey].append(string[pos + start])
            start += int(len(string) / len(self._key2))

        for pos in range(0, int(len(string) / len(self._key2))):
            for val in self._key2:
                self._decrypt.append(x[val][pos])

        self._decrypt = "".join(self._decrypt)  # creates string.
        return self._decrypt  # returns string.

    def product_decryption(self):  # product decryption method.
        self._string = self.transposition_decryption()  # decrypts the transposition.
        self._decrypt = []  # erases the value.
        self._decrypt = self.substitution_decryption()  # decrypts the substitution.
        return self._decrypt  # returns string.

    # Decryption using the ASCII letters
    def rsa_decryption(self):
        self.get_keys()  # creates the key.
        string_encrypted_chars = [ord(character) for character in self._string]
        self._decrypt = ''.join(
            [chr(character ** self._privateKey % self._modulus) for character in string_encrypted_chars])
        return self._decrypt  # returns string.

    def playfair_decryption(self):
        position, grid = self.playfair_postion()  # gets postion and grid.

        for pos in range(len(position)):  # gets new position cords.
            if position[pos][0][0] == position[pos][1][0]:  # Rule 1 if some row move right 1.
                if position[pos][0][1] == 0:
                    self._decrypt.append(grid[position[pos][0][0]][position[pos][0][1] + 4])  # at max so goes to start.
                else:
                    self._decrypt.append(grid[position[pos][0][0]][position[pos][0][1] - 1])  # moves over 1.

                if position[pos][1][1] == 0:
                    self._decrypt.append(grid[position[pos][1][0]][position[pos][1][1] + 4])  # at max so goes to start.
                else:
                    self._decrypt.append(grid[position[pos][1][0]][position[pos][1][1] - 1])  # moves over 1.

            elif position[pos][0][1] == position[pos][1][1]:  # Rule 1 if some column move down 1.
                if position[pos][0][0] == 0:
                    self._decrypt.append(grid[position[pos][0][0] + 4][position[pos][0][1]])  # at max so goes to start.
                else:
                    self._decrypt.append(grid[position[pos][0][0] - 1][position[pos][0][1]])  # moves down 1.

                if position[pos][1][0] == 0:
                    self._decrypt.append(grid[position[pos][1][0] + 4][position[pos][1][1]])  # at max so goes to start.
                else:
                    self._decrypt.append(grid[position[pos][1][0] - 1][position[pos][1][1]])  # moves down 1.

            else:
                self._decrypt.append(grid[position[pos][0][0]][position[pos][1][1]])  # swaps corners
                self._decrypt.append(grid[position[pos][1][0]][position[pos][0][1]])

        if len(self._decrypt) % 2 == 0 and self._decrypt[-1] == "X":  # if not divisible by 2 append x.
            self._decrypt.pop(-1)

        for x in range(len(self._decrypt) * 2):  # chceks if there is two letter beside eachother and adds x.
            try:
                if self._decrypt[x] == self._decrypt[x + 2] and self._decrypt[x + 1] == "X":
                    self._decrypt.pop(x + 1)
            except:
                pass

        self._decrypt = "".join(self._decrypt)  # creates a string.
        return self._decrypt  # returns decrypted value.

    def caesar_decryption(self):  # method to decrypt the users message
        alpha = "".join(self._alpha)  # string alphabet
        x = len(self._string)
        self._decrypt = ''

        for n in range(x):
            if self._string[n].isalpha():
                char_i = self._string[n]
                position = alpha.find(char_i)
                new_position = (position - self._key4) % 26  # decrypting formula shifts the letter to its original spot
                self._decrypt += alpha[new_position]  # adds decrypted letter to decrypted message
            elif self._string[n] == " ":
                self._decrypt += " "
            else:
                pass

        return self._decrypt  # returns the decrypted message


def quit(string, All_Values):  # function to check for exit command.
    text = ("Encrypted:", "Decrypted:", "Type:")  # holds type of text.
    if string == "stop":  # program exits if "stop" is entered.
        if len(All_Values) > 0:
            for tuple in All_Values:
                print("\n")  # prints newline.
                for value in tuple:
                    print(text[tuple.index(value)], value)  # prints tuple with all values.
        else:
            pass
        exit()  # exits the program.
    else:
        pass


def main():  # main function
    all_values = []  # holds all the values encrypted, decrypted and type used.
    while True:  # loops till stop is entered.
        while True:
            try:  # Error Handling
                user_input = input("Enter a sentence: ").lower()  # user input.

                for x in user_input:  # error raised if string has a number in it.
                    if x.isdigit():
                        raise ValueError

                if len(user_input) == 0:  # error raised if nothing is in the string.
                    raise RuntimeError
                break

            except ValueError:  # called if raised.
                print("Enter a string with no numbers.\n")

            except RuntimeError:  # called if raised.
                print("Enter a string, you entered nothing.\n")

        quit(user_input.lower(), all_values)  # quits if stop was entered.
        plain = PlaintextMsg(user_input)  # Temporary plain text class.
        cipher = CiphertextMsg()  # Temporary cipher class.
        random_num = random.randrange(6)  # gets random number.

        if random_num == 0:  # substitution method called.
            encrypted_message = plain.substitution_encryption()  # encodes message.
            cipher.set_message(encrypted_message)  # sets message.
            decry_message = cipher.substitution_decryption()  # decodes message.
            type_of_encryption = "Substitution Cipher"

        elif random_num == 1:  # transposition method called.
            encrypted_message = plain.transposition_encryption()  # encodes message.
            cipher.set_message(encrypted_message)  # sets message.
            decry_message = cipher.transposition_decryption()  # decodes message.
            type_of_encryption = "Transposition Cipher"

        elif random_num == 2:  # product method called.
            encrypted_message = plain.product_encryption()  # encodes message.
            cipher.set_message(encrypted_message)  # sets message.
            decry_message = cipher.product_decryption()  # decodes message.
            type_of_encryption = "Production Cipher"

        elif random_num == 3:  # RSA method called.
            encrypted_message = plain.rsa_encryption()  # encodes message.
            cipher.set_message(encrypted_message)  # sets message.
            decry_message = cipher.rsa_decryption()  # decodes message.
            type_of_encryption = "RSA Cipher"

        elif random_num == 4:  # playfair method called.
            encrypted_message = plain.playfair_encryption()  # encodes message.
            cipher.set_message(encrypted_message)  # sets message.
            decry_message = cipher.playfair_decryption()  # decodes message.
            type_of_encryption = "Playfair Cipher"

        else:
            encrypted_message = plain.caesar_encryption()  # encodes message.
            cipher.set_message(encrypted_message)  # sets message.
            decry_message = cipher.caesar_decryption()  # decodes message.
            type_of_encryption = "Caesar Cipher"

        plain.display()  # prints encoded message.
        cipher.display()  # prints decoded message.
        print(type_of_encryption)
        print("\n")
        Message().delete()  # deletes string value.

        # saves the encrypted, decrypted and type of encryption used into a tuple then appends it to a list.
        all_values.append((encrypted_message, decry_message, type_of_encryption))


if __name__ == "__main__":
    main()  # function call if this program is the main.
