# Building a Caesar Cipher Key 
# To encrypt text using a Caesar cipher, you shift the alphabet by a certain number of spaces. 
# Slicing makes creating this shifted alphabet incredibly easy.

# python

# alphabet = "abcdefghijklmnopqrstuvwxyz"
# shift = 3

# # 1. Split and rearrange the alphabet
# # alphabet[3:]  -> "defghijklmnopqrstuvwxyz"
# # alphabet[:3]  -> "abc"

# shifted_alphabet = alphabet[shift:] + alphabet[:shift]

# print(f"Original: {alphabet}")
# print(f"Shifted:  {shifted_alphabet}")

# # Output: defghijklmnopqrstuvwxyzabc

# #==================================================================================================
# # NEW FILE
# #==================================================================================================
# # Full Encryption Script Example
# # Once you have the original alphabet and the shifted alphabet, you can use Python's built-in str.maketrans() and translate() functions to instantly encrypt any message.



def encrypt_caesar(text, shift):
    alphabet = "abcdefghijklmnopqrstuvwxyz"
    
    # Ensure the shift wraps around if it is greater than 26
    shift = shift % 26
    
    # Create the cipher key using slicing
    shifted_alphabet = alphabet[shift:] + alphabet[:shift]
    
    # Map the original letters to the shifted letters
    cipher_table = str.maketrans(alphabet, shifted_alphabet)
    
    # Encrypt the text (and handle uppercase by mapping it too)
    return text.lower().translate(cipher_table)

# Test the script
secret_message = input("\nEnter message to encrypt: ")
encrypted = encrypt_caesar(secret_message, 5)

print(f"Encrypted Message: {encrypted}")

# Output: mjqqt btwqi

# # Important Edge Cases to Watch For
# # Oversized Shifts: If your shift integer is larger than the length of your alphabet (e.g., a shift of 30 on a 26-letter alphabet), slicing will break or fail to rotate properly. 
# # Always use the modulo operator (shift = shift % len(alphabet)) first.
# # Negative Shifts: If shift is a negative number, [shift:] grabs from the end of the string moving backward, which natively creates a decryption utility.

# #==================================================================================================
# # NEW FILE: Encryption
# #==================================================================================================
# # A New Cyber Security Project
# # This script takes a plain text file, applies the slicing rotation technique, and writes the scrambled text to a new file.

# import string

# def create_cipher_table(shift):
#     # Combine lowercase, uppercase, digits, and punctuation into one master alphabet
#     base_alphabet = string.ascii_lowercase + string.ascii_uppercase + string.digits + string.punctuation
    
#     # Keep shifts within the boundaries of our alphabet length
#     shift = shift % len(base_alphabet)
    
#     # Use slicing to rotate the alphabet
#     shifted_alphabet = base_alphabet[shift:] + base_alphabet[:shift]
    
#     # Create the translation mapping
#     return str.maketrans(base_alphabet, shifted_alphabet)

# def encrypt_file(input_filename, output_filename, shift):
#     try:
#         with open(input_filename, 'r', encoding='utf-8') as f:
#             plain_text = f.read()
            
#         cipher_table = create_cipher_table(shift)
#         encrypted_text = plain_text.translate(cipher_table)
        
#         with open(output_filename, 'w', encoding='utf-8') as f:
#             f.write(encrypted_text)
            
#         print(f"Success! Encrypted file saved as '{output_filename}'")
#     except FileNotFoundError:
#         print(f"Error: The file '{input_filename}' was not found.")

# # Operational Execution
# if __name__ == "__main__":
#     # Example: Create a dummy secret file first to test
#     with open("secret.txt", "w") as f:
#         f.write("Meet me at 12:30 PM. The password is: Python123!")
        
#     encrypt_file("secret.txt", "encrypted.txt", shift=15)



# #==================================================================================================
# # NEW FILE: Decryption
# #==================================================================================================
# # Decryption reverses the slice logic. Instead of moving items from the front to the back, we move items from the back to the front by passing a negative shift value.

# import string

# def create_decipher_table(shift):
#     base_alphabet = string.ascii_lowercase + string.ascii_uppercase + string.digits + string.punctuation
#     shift = shift % len(base_alphabet)
    
#     # Reverse the rotation using a negative shift
#     # This maps the shifted characters back to the original characters
#     shifted_alphabet = base_alphabet[-shift:] + base_alphabet[:-shift]
    
#     return str.maketrans(base_alphabet, shifted_alphabet)

# def decrypt_file(input_filename, output_filename, shift):
#     try:
#         with open(input_filename, 'r', encoding='utf-8') as f:
#             cipher_text = f.read()
            
#         decipher_table = create_decipher_table(shift)
#         decrypted_text = cipher_text.translate(decipher_table)
        
#         with open(output_filename, 'w', encoding='utf-8') as f:
#             f.write(decrypted_text)
            
#         print(f"Success! Decrypted file saved as '{output_filename}'")
#     except FileNotFoundError:
#         print(f"Error: The file '{input_filename}' was not found.")

# # Operational Execution
# if __name__ == "__main__":
#     decrypt_file("encrypted.txt", "decrypted.txt", shift=15)

# # Notes: Understanding str.maketrans() and .translate()
# # Python's built-in string translation tools are highly optimized C-level operations designed to swap characters instantly across massive strings without manually looping through letters.
# # str.maketrans(x, y): This function creates a translation table dictionary. 
# # It takes two strings of equal length (x and y). It maps the Unicode ordinal (integer ID) of the character at x[0] to the character at y[0], x[1] to y[1], and so on.
# # Example: str.maketrans("abc", "xyz") generates a hidden dictionary mapping looking like {97: 120, 98: 121, 99: 122}.string.translate(table): This string method takes the dictionary map generated by maketrans() and passes the entire target string through it. 
# # Any character found matching a key in the table is instantly swapped out for its mapped value. Characters not in the dictionary are ignored and left completely untouched.

# #==================================================================================================
# # NEW FILE: Password Strength Checker
# #==================================================================================================
# # What it does: Analyzes a password against standard industry complexity rules, rates it, and generates a secure, non-reversible cryptographic hash (SHA-256) for storage.
# # The Code:

# import hashlib
# import string

# def check_and_hash_password(password):
#     # 1. Evaluate Strength Criteria
#     has_upper = any(c in string.ascii_uppercase for c in password)
#     has_lower = any(c in string.ascii_lowercase for c in password)
#     has_digit = any(c in string.digits for c in password)
#     has_spec  = any(c in string.punctuation for c in password)
#     length_ok = len(password) >= 8
    
#     score = sum([has_upper, has_lower, has_digit, has_spec, length_ok])
    
#     # 2. Output Strength Rating
#     ratings = {5: "Excellent", 4: "Good", 3: "Moderate", 2: "Weak", 1: "Dangerous", 0: "Dangerous"}
#     print(f"Password Strength: {ratings[score]} ({score}/5)")
    
#     # 3. Generate Cryptographic Hash
#     # Convert string to bytes before hashing
#     password_bytes = password.encode('utf-8')
#     sha256_hash = hashlib.sha256(password_bytes).hexdigest()
    
#     print(f"Secure SHA-256 Hash for Database: {sha256_hash}")

# # Test
# check_and_hash_password("Secur3P@ss!")


# #==================================================================================================
# # NEW FILE: BAsic Port Scanner
# #==================================================================================================
# # What it does: Probes a target host IP address across a range of common ports to identify network exposure risks (open ports).
# # The Code:

# import socket

# def scan_ports(target_host, port_list):
#     print(f"Starting scan on host: {target_host}\n")
    
#     for port in port_list:
#         # Create a socket object (IPv4, TCP stream)
#         s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
#         # Set a fast timeout so the script doesn't freeze on closed ports
#         s.settimeout(1.0)
        
#         # Attempt connection connection
#         result = s.connect_ex((target_host, port))
        
#         if result == 0:
#             print(f"[*] Port {port}: OPEN")
#         else:
#             print(f"[ ] Port {port}: Closed/Filtered")
            
#         # Always close the network socket connection
#         s.close()

# # Test scanning localhost (your own computer safety baseline)
# scan_ports("127.0.0.1", [21, 22, 80, 443, 8080])

# # How it works:
# # socket.socket() establishes a raw network connection pipeline.
# # connect_ex() attempts a TCP three-way handshake with the target address. 
# # Unlike standard connect(), which crashes the script if it fails, connect_ex() handles network blocks gracefully by returning an error code. 
# # If the code returned is 0, the port actively accepted the connection, proving it is open and exposed.