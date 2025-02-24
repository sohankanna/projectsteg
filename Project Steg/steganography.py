# steganography.py - LSB Steganography Module using OpenCV
# To install OpenCV: pip install opencv-python

import cv2
import numpy as np
import base64
import os

# Hide message in image (LSB)
def hide_message_in_image(image_path: str, encrypted_message: str, output_path: str = 'stego_image.png'):
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Image file not found: {image_path}")

    image = cv2.imread(image_path)
    if image is None:
        raise FileNotFoundError("Failed to read image. Ensure the file is accessible and valid.")

    message = encrypted_message + '::END'
    binary_message = ''.join(format(ord(char), '08b') for char in message)

    data_index = 0
    for row in image:
        for pixel in row:
            for channel in range(3):
                if data_index < len(binary_message):
                    pixel[channel] = (pixel[channel] & 0xFE) | int(binary_message[data_index])
                    data_index += 1

    cv2.imwrite(output_path, image)
    print(f"Message hidden in {output_path}")

# Extract message from image
def extract_message_from_image(image_path: str) -> str:
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Stego image not found: {image_path}")

    image = cv2.imread(image_path)
    if image is None:
        raise FileNotFoundError("Failed to read stego image. Ensure it is a valid image file.")

    binary_data = ""
    for row in image:
        for pixel in row:
            for channel in range(3):
                binary_data += str(pixel[channel] & 1)

    all_bytes = [binary_data[i:i+8] for i in range(0, len(binary_data), 8)]
    decoded_message = ''.join(chr(int(byte, 2)) for byte in all_bytes)
    
    if '::END' in decoded_message:
        return decoded_message.split('::END')[0]
    return "No hidden message found"

# Test the module
if __name__ == "__main__":
    input_image = 'input.png'
    if not os.path.exists(input_image):
        print(f"Error: {input_image} not found. Place the image in the project directory.")
    else:
        hide_message_in_image(input_image, 'This is a secret message')
        message = extract_message_from_image('stego_image.png')
        print(f"Extracted Message: {message}")
