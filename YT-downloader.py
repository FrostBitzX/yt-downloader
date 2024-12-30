import yt_dlp as ytdl
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import os
import threading

root = Tk()
root.title("YouTube Downloader and Convert to MP3")
root.geometry("500x400")
root.resizable(False, False)

root.grid_rowconfigure(0, weight=1)
root.grid_rowconfigure(1, weight=2)
root.grid_rowconfigure(2, weight=1)
root.grid_rowconfigure(3, weight=1)
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=3)
root.grid_columnconfigure(2, weight=1)

l1 = Label(root, text="YouTube Downloader and Convert to MP3", font=("Helvetica", 14, "bold"), anchor="center")
l1.grid(row=0, column=0, columnspan=3, padx=20, sticky="nsew")

file_label = Label(root, text="Enter YouTube URLs below (one per line)", width=50, anchor="center", font=("Helvetica", 10))
file_label.grid(row=1, column=0, columnspan=3, sticky="nsew")

text_box = Text(root, height=10, width=50, font=("Helvetica", 10))
text_box.grid(row=2, column=0, columnspan=3, pady=10, padx=10, sticky="nsew")

scroll_bar = Scrollbar(root, orient="vertical", command=text_box.yview)
scroll_bar.grid(row=2, column=3, sticky="ns")
text_box.config(yscrollcommand=scroll_bar.set)

progress_label = Label(root, text="Progress: Waiting for download", font=("Helvetica", 10))
progress_label.grid(row=3, column=0, columnspan=3, sticky="w", padx=10)

progress_bar = ttk.Progressbar(root, length=400, mode='indeterminate')
progress_bar.grid(row=4, column=0, columnspan=3, padx=10, pady=10)
progress_bar.grid_remove()  # Hide the progress bar initially

def read_urls_from_text():
    urls_text = text_box.get("1.0", "end-1c")
    urls = [url.strip() for url in urls_text.split('\n') if url.strip()]
    return urls

def download_progress_hook(d):
    if d['status'] == 'downloading':
        current_filename = d.get('filename', '')
        progress_label.config(text=f"Downloading: {current_filename}")

def mainClick():
    download_thread = threading.Thread(target=download_and_convert)
    download_thread.start()

def download_and_convert():
    urls = read_urls_from_text()
    
    if not urls:
        messagebox.showwarning("No URLs", "Please enter YouTube URLs.")
        return

    output_folder = "output"
    os.makedirs(output_folder, exist_ok=True)

    progress_bar.grid()  # Show the progress bar
    progress_bar.start()
    progress_label.config(text="Progress: Downloading...")

    for url in urls:
        if url:
            try:
                ydl_opts = {
                    'format': 'bestaudio/best',
                    'extractaudio': True,
                    'outtmpl': os.path.join(output_folder, '%(title)s.mp3'),
                    'progress_hooks': [download_progress_hook]
                }

                with ytdl.YoutubeDL(ydl_opts) as ydl:
                    print(f"Downloading: {url}")
                    ydl.download([url])
                    print(f"Download completed: {url}")
            except Exception as e:
                print(f"Error downloading {url}: {e}")
                root.after(0, messagebox.showerror, "Error", f"Error downloading {url}: {str(e)}")
                return

    root.after(0, progress_bar.stop)
    root.after(0, progress_label.config, {"text": "Progress: All downloads are completed!"})
    root.after(0, messagebox.showinfo, "Status", "All downloads are completed!")
    progress_bar.grid_remove()

convert_btn = Button(
    root,
    text="Download and Convert to MP3",
    width=20,
    font=("Helvetica Bold", 14),
    bg="#78CE19",
    fg="white",
    relief="flat",
    command=mainClick
)
convert_btn.grid(row=5, column=0, columnspan=4, pady=20, padx=10, sticky="nsew")

root.mainloop()
