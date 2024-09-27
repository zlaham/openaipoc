from cryptography.fernet import Fernet

def generate_key(file_name="secret.key"):
    key = Fernet.generate_key()
    with open(file_name, "wb") as key_file:
        key_file.write(key)

def load_key(file_name="secret.key"):
    return open(file_name, "rb").read()

# Function to encrypt the API key
def encrypt_api_key(api_key, key):
    fernet = Fernet(key)
    encrypted_key = fernet.encrypt(api_key.encode())
    return encrypted_key

# Function to decrypt the API key
def decrypt_api_key(encrypted_key, key):
    fernet = Fernet(key)
    decrypted_key = fernet.decrypt(encrypted_key).decode()
    return decrypted_key