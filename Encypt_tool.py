import logging
from cryptography.fernet import Fernet, InvalidToken
import argparse

# Configure logging to write events to encryption_tool.log at the INFO level
logging.basicConfig(filename='encryption_tool.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Function to generate and save an encryption key
def generate_key(key_filename="encryption_key.key"):
    """
    Generates an encryption key and saves it to a specified file.
    Default filename is 'encryption_key.key' if not provided.
    """
    try:
        key = Fernet.generate_key()
        with open(key_filename, "wb") as key_file:
            key_file.write(key)
        logging.info(f"Key generated and saved in '{key_filename}'")
        print(f"Your key has been saved in {key_filename}")
    except Exception as e:
        logging.error(f"Failed to generate key: {e}")
        print("Failed to generate key.")

# Function to load the encryption key
def load_key(key_filename="encryption_key.key"):
    """
    Loads the encryption key from the specified file.
    Returns the key if successful, or None if the file is not found.
    """
    try:
        with open(key_filename, "rb") as key_file:
            key = key_file.read()
            logging.info(f"Key loaded successfully from '{key_filename}'")
            return key
    except FileNotFoundError:
        logging.warning(f"The key file '{key_filename}' was not found.")
        print(f"The key file '{key_filename}' was not found.")
        return None

# Function to encrypt a file
def encrypt_file(filename, key_filename="encryption_key.key"):
    """
    Encrypts the contents of a file using the encryption key.
    Saves the encrypted file with '.encrypted' added to the filename.
    """
    key = load_key(key_filename)
    if key is None:
        logging.warning("Encryption aborted: No key found.")
        print("Encryption aborted. No key was found.")
        return
    
    fernet = Fernet(key)
    
    try:
        with open(filename, "rb") as file:
            file_data = file.read()
        encrypted_data = fernet.encrypt(file_data)
        with open(filename + ".encrypted", "wb") as file:
            file.write(encrypted_data)
        
        logging.info(f"File '{filename}' encrypted and saved as '{filename}.encrypted'")
        print(f"Your file has been encrypted and saved as {filename}.encrypted")
    except FileNotFoundError:
        logging.error(f"The file '{filename}' was not found for encryption")
        print(f"The file '{filename}' was not found.")

# Function to decrypt a file
def decrypt_file(filename, key_filename="encryption_key.key"):
    """
    Decrypts the contents of an encrypted file using the encryption key.
    Restores the original filename by removing '.encrypted' if present.
    Handles invalid key errors and notifies the user if decryption fails.
    """
    key = load_key(key_filename)
    if key is None:
        logging.warning("Decryption aborted: No key found.")
        print("Decryption aborted. No key was found.")
        return
    
    fernet = Fernet(key)
    
    try:
        with open(filename, "rb") as file:
            encrypted_data = file.read()
        decrypted_data = fernet.decrypt(encrypted_data)  # This may raise InvalidToken if key is wrong
        
        # Save decrypted data by removing ".encrypted" if present, otherwise add "_decrypted"
        new_filename = filename.replace(".encrypted", "")
        with open(new_filename, "wb") as file:
            file.write(decrypted_data)
        
        logging.info(f"File '{filename}' decrypted and saved as '{new_filename}'")
        print(f"Your file has been decrypted and saved as {new_filename}")
    
    except FileNotFoundError:
        logging.error(f"The file '{filename}' was not found for decryption")
        print(f"The file '{filename}' was not found.")
    except InvalidToken:
        logging.error("Decryption failed: Invalid key or corrupted data.")
        print("Decryption failed. The key may be incorrect or the data may be corrupted.")

# Main function for command-line argument handling
def main():
    """
    Parses command-line arguments and calls the appropriate function
    for key generation, file encryption, or file decryption based on the user's choice.
    """
    parser = argparse.ArgumentParser(description="Tool for encryption and decryption")
    parser.add_argument("action", choices=["generate_key", "encrypt", "decrypt"], help="Select the action you want to perform")
    parser.add_argument("filename", nargs="?", help="Enter the file name you want to work with")
    parser.add_argument("-k", "--keyfile", default="encryption_key.key", help="Specify the key file name (default: encryption_key.key)")

    args = parser.parse_args()

    if args.action == "generate_key":
        generate_key(args.keyfile)
    elif args.action == "encrypt":
        if args.filename:
            encrypt_file(args.filename, args.keyfile)
        else:
            logging.warning("No filename provided for encryption.")
            print("Filename must be provided for encryption.")
    elif args.action == "decrypt":
        if args.filename:
            decrypt_file(args.filename, args.keyfile)
        else:
            logging.warning("No filename provided for decryption.")
            print("Filename must be provided for decryption.")

if __name__ == "__main__":
    main()
