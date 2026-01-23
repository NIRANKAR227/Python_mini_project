import bcrypt
import tkinter as tk
from tkinter import messagebox

password=b"123456789asdf"
hashed_Password=bcrypt.hashpw(password,bcrypt.gensalt())
print(hashed_Password)

def validate(password):
    entered_password = password.encode('utf-8')
    
    if bcrypt.checkpw(entered_password,hashed_Password):
        print("Valid Password")
        messagebox.showinfo("Success", "Valid Password")
    else:
        print("Invalid Password")
        messagebox.showerror("Error", "Invalid Password")


root=tk.Tk()
root.geometry("300x200")

password_entry=tk.Entry(root)
password_entry.pack()
button=tk.Button(text='validate',command=lambda:validate(password_entry.get()))
button.pack()

root.mainloop()