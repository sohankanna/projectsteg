from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend
import base64, os

# Derive a key from the passphrase
def derive_key(passphrase: str, salt: bytes) -> bytes:
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    return kdf.derive(passphrase.encode())

# AES Encryption
def encrypt_message(message: str, passphrase: str) -> str:
    salt = os.urandom(16)
    key = derive_key(passphrase, salt)
    iv = os.urandom(16)

    padder = padding.PKCS7(128).padder()
    padded_message = padder.update(message.encode()) + padder.finalize()

    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(padded_message) + encryptor.finalize()

    return base64.b64encode(salt + iv + ciphertext).decode()

# AES Decryption
def decrypt_message(encrypted_message: str, passphrase: str) -> str:
    data = base64.b64decode(encrypted_message)
    salt, iv, ciphertext = data[:16], data[16:32], data[32:]
    key = derive_key(passphrase, salt)

    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    decrypted_padded = decryptor.update(ciphertext) + decryptor.finalize()

    unpadder = padding.PKCS7(128).unpadder()
    decrypted_message = unpadder.update(decrypted_padded) + unpadder.finalize()

    return decrypted_message.decode()

# Test the module
if __name__ == "__main__":
    msg = "Hello, Steganography!"
    pw = "strongpassword"
    enc = encrypt_message(msg, pw)
    print(f"Encrypted: {enc}")
    dec = decrypt_message(enc, pw)
    print(f"Decrypted: {dec}")
