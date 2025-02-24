# projectsteg

# Overview

This project integrates AES encryption with image steganography to securely hide and extract confidential messages within images. By encrypting the message before embedding it, we ensure an extra layer of protection, making it unreadable without the correct passphrase.

# Features

AES-256 Encryption for securing messages before hiding them in an image.

Image Steganography using LSB (Least Significant Bit) encoding.

User-Friendly GUI built with Tkinter for ease of use.

File Upload & Extraction with real-time status updates.

Error Handling to manage incorrect passphrases, invalid images, and missing data.

# Technologies Used

Python

Tkinter (GUI)

PIL (Pillow) (Image Processing)

OpenCV (Image Handling)

Cryptography (AES Encryption)

NumPy (Data Manipulation)


# Usage

Hiding a Message

Upload an image.

Enter a passphrase for encryption.

Type the secret message to hide.

Click "Hide Data", and the output stego-image will be saved as stego_image.png.

Extracting a Message

Upload a stego-image.

Enter the passphrase.

Click "Extract Data" to retrieve the hidden message.

