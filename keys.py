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
    #creates an array to store the usb info on the computer 
    drive_list = []
    #gets a binary string of what drives are active
    #ex: 00000000000000000000011100
    # 0 is off and 1 is on
    bitmask = ctypes.windll.kernel32.GetLogicalDrives()
    #print(f"Bitmask: {bin(bitmask)[2:].zfill(26)}")
    #loops through each uppercase letter in the alphabet
    for letter in string.ascii_uppercase:
        print(f"Letter: {letter}")
        print(f"bitmask & 1: {bitmask & 1}")
        # for each uppercase letter it checks to see if the drive is active by checking the smallest bit
        # for 11100 it would check the 0 on the right
        if bitmask & 1:
            #if true it makes the drive match the current letter
            drive = f"{letter}:/"
            #then it finds the type of drive, such as removable, internal, etc
            type = ctypes.windll.kernel32.GetDriveTypeW(drive)
            print(type)
            #if the drive is a removable drive (type 2) then it adds that drive to the drive array
            if type == 2:  # DRIVE_REMOVABLE
                drive_list.append(drive)
        # this removes the smalles bit so for 11100 it would remove the right most 0
        bitmask >>= 1
    #returns the array
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

