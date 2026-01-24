import tkinter as tk
from tkinter import filedialog, messagebox
from pytubefix import YouTube 
from moviepy import VideoFileClip


def get_path():
    path = filedialog.askdirectory()
    if path:
        path_label.config(text=path)


def download():
    video_path = url_entry.get()
    file_path = path_label.cget("text")

    if not video_path:
        messagebox.showerror("Error", "Please enter video URL")
        return

    if file_path == "Select path to download":
        messagebox.showerror("Error", "Please select download folder")
        return

    try:
        yt = YouTube(video_path)

        stream = yt.streams.get_highest_resolution()

        mp4 = stream.download(output_path=file_path)

        video_clip = VideoFileClip(mp4)
        video_clip.close()

        messagebox.showinfo("Success", "Download completed")

    except Exception as e:
        messagebox.showerror("Error", f"Download failed \n{e}")


root = tk.Tk()
root.title("Video Downloader")
root.geometry("400x300")

canvas = tk.Canvas(root, width=400, height=300)
canvas.pack()

# App Label
app_label = tk.Label(root, text="Video Downloader",
                     fg="grey", font=("Arial", 20))
canvas.create_window(200, 20, window=app_label)

# Entry for URL
url_label = tk.Label(root, text="Enter Video URL")
url_entry = tk.Entry(root, width=40)

canvas.create_window(200, 80, window=url_label)
canvas.create_window(200, 100, window=url_entry)

# Path selector
path_label = tk.Label(root, text="Select path to download")

path_button = tk.Button(root, text="Select", command=get_path)

canvas.create_window(200, 150, window=path_label)
canvas.create_window(200, 170, window=path_button)

# Download button
download_button = tk.Button(root, text="Download", command=download)
canvas.create_window(200, 250, window=download_button)

root.mainloop()
