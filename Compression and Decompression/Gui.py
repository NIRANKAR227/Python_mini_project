import tkinter as tk
from compressmodule import *

def compression(i,o):
    compress(i,o)

def decompression(i,o):
    decompress(i,o)


window=tk.Tk()
window.title("Compression engine")
window.geometry("600x400")

input_entry=tk.Entry(window)
output_Entry=tk.Entry(window)

input_label=tk.Label(window,text="File to be compressed:")
output_label=tk.Label(window,text="File to be compressed:")

compress_button=tk.Button(window,text="Compress",command=lambda:compression(input_entry.get(),output_Entry.get()))
decompress_button=tk.Button(window,text="Decompress",command=lambda:decompression(input_entry.get(),output_Entry.get()))

input_label.grid(row=0,column=0)
output_label.grid(row=1,column=0)
input_entry.grid(row=0,column=1)
output_Entry.grid(row=1,column=1)
compress_button.grid(row=3,column=0)
decompress_button.grid(row=3,column=1)

window.mainloop()