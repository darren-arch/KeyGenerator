import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import os, string, time, ctypes, subprocess, webbrowser

#how to compile the program into a .exe
#first run the python virtual enviroment when in the parent directory run .\.venv\Scripts\activate
#then you can run pyinstaller with the script below
#onefile makes the executable all one file
#windowed makes the exe not open a cmd window to run
#the add data adds the avalan logos
#icon sets the icon of the exe
#pyinstaller --onefile --windowed --add-data "AvaLAN.png:." --add-data "AvaLANLogo.ico:." --icon=AvaLANLogo.ico keys.py

#this allows the python program to use the included AvaLAN.png and AvaLANLogo.ico files
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

#this is for the help button, it links to the knowledge base article on how to use the app
def link():
    webbrowser.open_new("https://support.avalan.com/portal/en/kb/articles/how-to-remake-an-idsu-s-pairing-key-17-7-2025")

#this runs when the user clicks SubmitButton/Create Pairing Key button
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
    
    #Warns the User that their usb is about to be formatted
    confirm = messagebox.askquestion("Format", "You are about to format your USB.\nAll data on it will be ERASED!\nDo you want to Continue?", icon=messagebox.WARNING, )
    if confirm == "no":
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
#sets the icon to the avalan logo
root.iconbitmap(resource_path("AvaLANLogo.ico"))

# configures the amount of space that the column takes up
# the first number is the column that is being configured, and the second number is the amount of space that the column takes up
# using 1 means that it uses 100% of the space and centers it
root.columnconfigure(0, weight=1)

AvaLANImage = tk.PhotoImage(file=str(resource_path("AvaLAN.png")))
AvaLANImage = AvaLANImage.subsample(4,4)
ImageLabel = tk.Label(root, image=AvaLANImage)
ImageLabel.grid(row=0, column=0, pady=5)

#to keep all of the items centered and not spread out they need a frame
# the frame is made in that root and put at row 0 column 0 and gets centered by the root window
# everything inside of the frame is equally separated and centered in their own rows and columns
frame = tk.Frame(root)
frame.grid(row=1, column=0)

#The Label asking the user to pick a USB
USBLabel = tk.Label(frame, text="Choose your USB:")
USBLabel.grid(row = 0, column = 0, pady=5)
#USBLabel.pack(pady=5)

#Combobox for the user to pick a USB
USBChoice = ttk.Combobox(frame, values=usb_drives, width=17)
USBChoice.grid(column=1, row=0, padx=5, pady=5)
#USBChoice.pack(pady=5)

#Label asking for the first 4 characters of the E01
FirstFourLabel = tk.Label(frame, text="First 4 Characters of the E01 Mac Address:")
FirstFourLabel.grid(column=0, row=1, pady=5)

#Entry to hold the first 4 of the E01
FirstEntry = tk.Entry(frame, width=20)
FirstEntry.grid(column=1, row=1, padx=5, pady=5)

#Label asking for the last 4 characters of the E01
LastFourLabel = tk.Label(frame, text="Last 4 Characters of the E01 Mac Address:")
LastFourLabel.grid(column=0, row=2, pady=5)

#Entry to hold the last 4 of the E01
LastEntry = tk.Entry(frame, width=20)
LastEntry.grid(column=1, row=2, padx=5, pady=5)

#help button that links to the knowledgebase article on how to use the tool
HelpButton = tk.Button(frame, text="Help", command=link)
HelpButton.grid(column=0, row=3, pady=5)

#button to submit the information and create the USB
SubmitButton = tk.Button(frame, text="Create Pairing Key", command=click)
SubmitButton.grid(column=1, row=3, pady=5, padx=5)

if len(usb_drives) <= 0:
    #informs the user to plug a usb into the computer then exits
    messagebox.showerror("No USB", "Plug a USB drive into the computer")

#runs the tkinter root
root.mainloop()

