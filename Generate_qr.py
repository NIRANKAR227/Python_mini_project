import tkinter as tk
import qrcode
from PIL import Image, ImageTk

root=tk.Tk()

def generate():
    link_name = name_entry.get()
    link = link_entry.get()
    file_name = link_name + ".jpeg"

    qr = qrcode.make(link)
    qr.save(file_name)

    img = Image.open(file_name)
    img = img.resize((200, 200))  
    image = ImageTk.PhotoImage(img)

    image_label = tk.Label(root, image=image)
    image_label.image = image   # “Store the image INSIDE the label object.”  if function is over the image is deleted so nothing to show on canvas if it is not used
    canvas.create_window(200, 400, window=image_label)

canvas=tk.Canvas(root,width=400,height=600)
canvas.pack()

app_label=tk.Label(root,text="QR code generator",fg='grey',font=("Arial",30))
canvas.create_window(200,50,window=app_label)

name_label=tk.Label(root,text="Link name")
link_label=tk.Label(root,text="Link")
canvas.create_window(200,100,window=name_label)
canvas.create_window(200,160,window=link_label)

name_entry=tk.Entry(root)
link_entry=tk.Entry(root)
canvas.create_window(200,130,window=name_entry)
canvas.create_window(200,180,window=link_entry)

button=tk.Button(text="Generate QR code",command=lambda:generate())
canvas.create_window(200,230,window=button)

root.mainloop()