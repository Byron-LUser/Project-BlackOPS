import random
import string

#Password generator.

#I'll print all the string functions and characters here, 
letters = string.ascii_letters
digits = string.digits
punctuations = string.punctuation
hexdigits = string.hexdigits

# print("\n")
# print(f"These are letters we are going to use: {letters}")
# print(f"These are digits we are going to use: {digits}")
# print(f"These are punctuations we are going to use: {punctuations}")
# print(f"These are hexdigits we are going to use: {hexdigits}")

def password_gen(length):
    print("\n")
    to_use = letters + digits + punctuations + hexdigits

    my_password = ''.join(random.choice(to_use) for i in range(length))

    return my_password


generated_password = password_gen(int(input("enter number of characters: ")))
print(generated_password)
