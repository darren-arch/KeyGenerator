import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import os, string, time, ctypes, subprocess



def click():
    #gets the USB that the user chose
    usb = USBChoice.get()
    #checks to make sure that the user chose a usb
    if not usb:
        messagebox.showerror("No USB Chosen", "Choose a USB.")
        return
    
    #gets the first 4 characters of the E01
    firstfour = FirstEntry.get()
    #makes sure that firstfour is capitalized
    firstfour = firstfour.upper()
    #checks to make sure that firstfour is 4 characters long and doesn't contain a :
    if len(firstfour) < 4:
        messagebox.showerror("Short","There are less than 4 characters for the first four.")
        return
    elif len(firstfour) > 4:
        messagebox.showerror("Long", "There are more than 4 characters for the first four.")
        return
    elif firstfour.find(":") != -1:
        messagebox.showerror("Colon", "Do not include the colon (:) with the first four.")
        return
    
    #gets the last 4 characters of the E01
    lastfour = LastEntry.get()
    #makes sure that firstfour is capitalized
    lastfour = lastfour.upper()
    #checks to make sure that lastfour is 4 characters long and doesn't contain a :
    if len(lastfour) < 4:
        messagebox.showerror("Short","There are less than 4 characters for the last four.")
        return
    elif len(lastfour) > 4:
        messagebox.showerror("Long", "There are more than 4 characters for the last four.")
        return
    elif lastfour.find(":") != -1:
        messagebox.showerror("Colon", "Do not include the colon (:) with the last four.")
        return
    
    #calls a windows command to format the USB to FAT32
    #the call function will wait for the command to finish before continuing the program
    subprocess.call(f"cmd /c format {usb} /FS:FAT32 /Q /Y")
    
    #creates the total filepath to write the key.cfg file to
    filepath = os.path.join(usb, "key.cfg")

    #creates the file in the usb
    with open(filepath, "w") as file:
        #writes the key information to the file
        file.write(f"{firstfour},{lastfour}")
    #lets the user know that the USB key was successfully generated
    messagebox.showinfo("Success", "USB Key Successfully Generated")

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
        # for each uppercase letter it checks to see if the drive is active by checking the smallest bit
        # for 11100 it would check the 0 on the right
        if bitmask & 1:
            #if true it makes the drive match the current letter
            drive = f"{letter}:\\"
            #then it finds the type of drive, such as removable, internal, etc
            type = ctypes.windll.kernel32.GetDriveTypeW(drive)
            #if the drive is a removable drive (type 2) then it adds that drive to the drive array
            if type == 2:  # DRIVE_REMOVABLE
                drive_list.append(drive)
        # this removes the smalles bit so for 11100 it would remove the right most 0
        bitmask >>= 1
    #returns the array
    return drive_list

#calls the get_usb_drives function to check what usb drives are connected to the computer
usb_drives = get_usb_drives()

#window for the program
root = tk.Tk()
#title for the window
root.title('AvaLAN Key Generator')
#specifies the size of the window
root.geometry("550x300")

#The Label asking the user to pick a USB
USBLabel = tk.Label(root, text="Choose your USB:")
USBLabel.pack(pady=5)

#Combobox for the user to pick a USB
USBChoice = ttk.Combobox(root, values=usb_drives)
USBChoice.pack(pady=5)

#information about where the E01 Mac address is located
EO1LocationLabel = tk.Label(root, text="The IDSU has a sticker next to its Cloud ID sticker, in the gap at the bottom of the unit.\nThat sticker contains the E01 Mac address.\nYou will need the first 4 and last 4 characters of that E01.\nFor example if the E01 is 48:8F:2C:7B:5A:4C you would need 488F and 5A4C.")
EO1LocationLabel.pack()

#Label asking for the first 4 characters of the E01
FirstFourLabel = tk.Label(root, text="What are the first 4 Characters of the E01 Mac Address:")
FirstFourLabel.pack()

#Entry to hold the first 4 of the E01
FirstEntry = tk.Entry(root)
FirstEntry.pack()

#Label asking for the last 4 characters of the E01
LastFourLabel = tk.Label(root, text="What are the last 4 Characters of the E01 Mac Address:")
LastFourLabel.pack()

#Entry to hold the last 4 of the E01
LastEntry = tk.Entry(root)
LastEntry.pack()

#button to submit the information and create the USB
SubmitButton = tk.Button(root, text="Create Pairing Key", command=click)
SubmitButton.pack()

#checks to make sure a USB is inserted into the computer
if len(usb_drives) <= 0:
    #informs the user to plug a usb into the computer then exits
    messagebox.showerror("No USB", "Plug a USB drive into the computer")
    exit()

root.mainloop()

