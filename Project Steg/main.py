# main.py - Steganography Project with Passphrase Prompt After Image Selection

import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog, scrolledtext
from encryption import encrypt_message, decrypt_message
from steganography import hide_message_in_image, extract_message_from_image
from cryptography.exceptions import InvalidTag


# Functions
def upload_image():
    file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
    if file_path:
        image_path_var.set(file_path)
        image_label.config(text=f"Selected: {file_path.split('/')[-1]}")

def hide_data():
    passphrase = passphrase_entry.get()
    message = message_entry.get("1.0", tk.END).strip()
    image_path = image_path_var.get()
    if not (passphrase and message and image_path):
        messagebox.showerror("Error", "All fields are required!")
        return
    try:
        encrypted_message = encrypt_message(message, passphrase)
        hide_message_in_image(image_path, encrypted_message)
        messagebox.showinfo("Success", "Data hidden in 'stego_image.png'")
    except Exception as e:
        messagebox.showerror("Error", str(e))

def extract_data():
    image_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png")])
    if image_path:
        image_label.config(text=f"Extracting from: {image_path.split('/')[-1]}")
        passphrase = simpledialog.askstring("Passphrase", "Enter passphrase for extraction:", show="*")
        if not passphrase:
            messagebox.showerror("Error", "Passphrase is required!")
            return
        try:
            hidden_message = extract_message_from_image(image_path)
            if not hidden_message:
                messagebox.showwarning("No Message", "No hidden message found in the image.")
                return
            decrypted_message = decrypt_message(hidden_message, passphrase)
            output_text.delete("1.0", tk.END)
            output_text.insert(tk.END, decrypted_message or "Incorrect passphrase or no message found.")
        except ValueError:
            messagebox.showerror("Error", "Decryption failed: Invalid passphrase or IV.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

# Tkinter GUI Setup
root = tk.Tk()
root.title("Steganography Tool")
root.geometry("420x500")
root.configure(bg="#E8F6F3")

image_path_var = tk.StringVar()

tk.Label(root, text="Message to Hide:", bg="#E8F6F3", font=("Arial", 10, "bold")).pack(pady=5)
message_entry = scrolledtext.ScrolledText(root, height=4, width=50, font=("Arial", 9))
message_entry.pack(pady=5)

tk.Label(root, text="Passphrase (for Hiding Only):", bg="#E8F6F3", font=("Arial", 10, "bold")).pack(pady=5)
passphrase_entry = tk.Entry(root, show="*", font=("Arial", 10))
passphrase_entry.pack(pady=5)

tk.Button(root, text="Upload Image", bg="#4CAF50", fg="white", font=("Arial", 10, "bold"), command=upload_image).pack(pady=5)
image_label = tk.Label(root, text="No image selected", bg="#E8F6F3", font=("Arial", 9, "italic"))
image_label.pack(pady=5)

tk.Button(root, text="Hide Data", bg="#2196F3", fg="white", font=("Arial", 10, "bold"), command=hide_data).pack(pady=5)
tk.Button(root, text="Extract Data", bg="#FF5722", fg="white", font=("Arial", 10, "bold"), command=extract_data).pack(pady=5)

tk.Label(root, text="Extracted Message:", bg="#E8F6F3", font=("Arial", 10, "bold")).pack(pady=5)
output_text = scrolledtext.ScrolledText(root, height=4, width=50, font=("Arial", 9))
output_text.pack(pady=5)

root.mainloop()
