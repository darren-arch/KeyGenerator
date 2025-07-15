import tkinter as tk

root = tk.Tk()
root.title('AvaLAN Key Generator')


root.mainloop()



with open('key.cfg', 'w') as file:
    file.write(key)
