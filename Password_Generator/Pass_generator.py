import secrets
import string
import math
import tkinter as tk
from tkinter import messagebox
import qrcode
from PIL import Image, ImageTk


def generate_password():
    length = int(length_var.get())
    
    chars = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(secrets.choice(chars) for _ in range(length))
    
    password_var.set(password)
    check_strength(password)


def calculate_entropy(password):
    pool = 0

    if any(c.islower() for c in password):
        pool += 26
    if any(c.isupper() for c in password):
        pool += 26
    if any(c.isdigit() for c in password):
        pool += 10
    if any(c in string.punctuation for c in password):
        pool += len(string.punctuation)

    if pool == 0:
        return 0

    entropy = len(password) * math.log2(pool)
    return entropy



def estimate_crack_time(entropy):
    guesses_per_second = 1e10 

    seconds = (2 ** entropy) / guesses_per_second

    if seconds < 60:
        return f"{seconds:.2f} seconds"
    elif seconds < 3600:
        return f"{seconds/60:.2f} minutes"
    elif seconds < 86400:
        return f"{seconds/3600:.2f} hours"
    elif seconds < 31536000:
        return f"{seconds/86400:.2f} days"
    else:
        return f"{seconds/31536000:.2f} years"



def check_strength(password=None):
    if password is None:
        password = password_var.get()

    if not password:
        return

    entropy = calculate_entropy(password)
    crack_time = estimate_crack_time(entropy)

    if entropy < 40:
        strength = "Weak 🔴"
    elif entropy < 70:
        strength = "Moderate 🟡"
    else:
        strength = "Strong 🟢"

    result_label.config(
        text=f"Strength: {strength}\nEntropy: {entropy:.2f} bits\nCrack Time: {crack_time}"
    )



def toggle_password():
    if show_var.get():
        password_entry.config(show="")
    else:
        password_entry.config(show="*")



def generate_qr():
    password = password_var.get()
    if not password:
        messagebox.showwarning("Warning", "No password to generate QR")
        return

    qr = qrcode.make(password)
    qr.save("password_qr.png")

    img = Image.open("password_qr.png")
    img = img.resize((150, 150))
    img_tk = ImageTk.PhotoImage(img)

    qr_label.config(image=img_tk)
    qr_label.image = img_tk



root = tk.Tk()
root.title("Password Generator & Strength Checker 🔐")
root.geometry("400x500")

password_var = tk.StringVar()
length_var = tk.StringVar(value="12")
show_var = tk.BooleanVar()

# Password Entry
tk.Label(root, text="Password:").pack()
password_entry = tk.Entry(root, textvariable=password_var, show="*", width=30)
password_entry.pack()

# Show toggle
tk.Checkbutton(root, text="Show Password", variable=show_var, command=toggle_password).pack()

# Length input
tk.Label(root, text="Length:").pack()
tk.Entry(root, textvariable=length_var, width=5).pack()

# Buttons
tk.Button(root, text="Generate Password", command=generate_password).pack(pady=5)
tk.Button(root, text="Check Strength", command=check_strength).pack(pady=5)
tk.Button(root, text="Generate QR Code", command=generate_qr).pack(pady=5)

# Result
result_label = tk.Label(root, text="Strength: ", justify="left")
result_label.pack(pady=10)

# QR Display
qr_label = tk.Label(root)
qr_label.pack()

root.mainloop()