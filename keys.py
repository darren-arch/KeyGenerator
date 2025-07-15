import tkinter as tk
from tkinter import ttk

root = tk.Tk()
root.title('AvaLAN Key Generator')
root.geometry("500x500")

label = tk.Label(root, text="Choose your USB:")
label.pack(pady=10)

combo_box = ttk.Combobox(root, values=["USB 1", "USB 2"])
combo_box.pack(pady=10)

#label

button = tk.Button(root, text="")

root.mainloop()



#with open('key.cfg', 'w') as file:
#    file.write(key)
