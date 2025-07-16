import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import os, string, time, ctypes



def click():
    usb = combo_box.get()
    if not usb:
        messagebox.showerror("No USB Chosen", "Choose a USB.")
        return
    firstfour = first.get()
    if len(firstfour) < 4:
        messagebox.showerror("Short","There are less than 4 characters for the first four.")
        return
    elif len(firstfour) > 4:
        messagebox.showerror("Long", "There are more than 4 characters for the first four.")
        return
    elif firstfour.find(":") != -1:
        messagebox.showerror("Colon", "Do not include the colon (:) with the first four.")
        return
    lastfour = last.get()
    if len(lastfour) < 4:
        messagebox.showerror("Short","There are less than 4 characters for the last four.")
        return
    elif len(lastfour) > 4:
        messagebox.showerror("Long", "There are more than 4 characters for the last four.")
        return
    elif lastfour.find(":") != -1:
        messagebox.showerror("Colon", "Do not include the colon (:) with the last four.")
        return
    
    with open("key.cfg", "w") as file:
        file.write(f"{firstfour},{lastfour}")

def get_usb_drives():
    drive_list = []
    bitmask = ctypes.windll.kernel32.GetLogicalDrives()
    for letter in string.ascii_uppercase:
        if bitmask & 1:
            drive = f"{letter}:/"
            type = ctypes.windll.kernel32.GetDriveTypeW(drive)
            if type == 2:  # DRIVE_REMOVABLE
                drive_list.append(drive)
        bitmask >>= 1
    return drive_list

print("USB drives:", get_usb_drives())

root = tk.Tk()
root.title('AvaLAN Key Generator')
root.geometry("550x300")

label = tk.Label(root, text="Choose your USB:")
label.pack(pady=10)

combo_box = ttk.Combobox(root, values=["USB 1", "USB 2"])
combo_box.pack(pady=10)

label = tk.Label(root, text="The IDSU has a sticker next to its Cloud ID sticker, in the gap at the bottom of the unit.\nThat sticker contains the E01 Mac address.\nYou will need the first 4 and last 4 characters of that E01.\nFor example if the E01 is 48:8F:2C:7B:5A:4C you would need 488F and 5A4C.")
label.pack()
label = tk.Label(root, text="What are the first 4 Characters of the E01 Mac Address:")
label.pack()

first = tk.Entry(root)
first.pack()

label = tk.Label(root, text="What are the last 4 Characters of the E01 Mac Address:")
label.pack()

last = tk.Entry(root)
last.pack()

button = tk.Button(root, text="Create Pairing Key", command=click)
button.pack()

root.mainloop()

