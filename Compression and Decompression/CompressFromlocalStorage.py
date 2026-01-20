import tkinter as tk
from compressmodule import *
from tkinter import filedialog

def open_file():
    filename=filedialog.askopenfilename(initialdir='/',title="Select a file to compress")
    return filename

def compression(i,o):
    compress(i,o)

def decompression(i,o):
    decompress(i,o)


window=tk.Tk()
window.title("Compression engine")
window.geometry("600x400")



compress_button=tk.Button(window,text="Compress",command=lambda:compression(open_file(),'output_compress_local.txt'))
decompress_button=tk.Button(window,text="Decompress",command=lambda:decompression(open_file(),'output_decompress_local.txt'))


compress_button.grid(row=1,column=0)
decompress_button.grid(row=1,column=1)

window.mainloop()