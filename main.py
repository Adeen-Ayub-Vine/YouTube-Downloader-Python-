import customtkinter as ctk
from tkinter import ttk
from pytube import YouTube, Playlist
import os

def download_video():
    url = video_url.get()
    resolution = resolution_var.get()
    audio_only = audio_only_var.get()
    
    progress_label.pack(padx=5,pady=10)
    progress_bar.pack(padx=5,pady=10)
    status_label.pack(padx=5,pady=10)
    
    try:
        # Check if the URL is for a playlist or a single video
        if 'playlist' in url.lower():
            playlist = Playlist(url)
            i=0
            for x in playlist.video_urls:
                i=i+1
                yt = YouTube(x, on_progress_callback=on_progress)
                download_single_video(yt, resolution, audio_only)
                print(f"Done {i} / {len(playlist.video_urls)}")
        else:
            yt = YouTube(url, on_progress_callback=on_progress)
            download_single_video(yt, resolution, audio_only)
        
        status_label.configure(text="Download Completed Successfully", text_color="white", fg_color="green")
        
    except Exception as e:
        status_label.configure(text=f"Error {str(e)}", text_color="white", fg_color="red")


def download_single_video(yt, resolution, audio_only):
    try:
        if audio_only:
            # Get the audio-only stream
            stream = yt.streams.filter(only_audio=True).first()
            file_extension = ".mp3"
        else:
            # Get the stream with both video and audio
            stream = yt.streams.filter(res=resolution, progressive=True).first()
            file_extension = ".mp4"
        
        # Check if stream is None
        if stream is None:
            raise Exception("Stream not found for the specified resolution or audio-only option.")
        
        # Construct file name with resolution
        file_name = f"{yt.title} {resolution}{file_extension}"
        
        # Construct the full file path
        file_path = os.path.join("downloads", file_name)
        
        # Download the video/audio to a specific directory
        stream.download(output_path=file_path, filename=file_name)
        
    except OSError as e:
        status_label.configure(text=f"Error: {str(e)}", text_color="white", fg_color="red")
    except Exception as e:
        status_label.configure(text=f"Error: {str(e)}", text_color="white", fg_color="red")



def on_progress(stream,chunk,bytes_remaining):
    total_size = stream.filesize
    bytes_downloaded = total_size - bytes_remaining
    percentage_completed = bytes_downloaded / total_size * 100
    
    progress_label.configure(text=str(int(percentage_completed)) + "%")
    progress_label.update()
    progress_bar.set(float(percentage_completed/100))
    
    
# Create Root window
root = ctk.CTk()
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

# Title of the root window
root.title("YouTube Video Downloader")

# Set min/max dimensions(width & height) of the window
root.geometry("720x480")
root.minsize(720, 480)
root.maxsize(1080, 720)

# Create a frame to hold the content
content_frame = ctk.CTkFrame(root)
content_frame.pack(fill = ctk.BOTH, expand=True, padx=10, pady=10)

# Create a label and video url textbox 
url_label = ctk.CTkLabel(content_frame, text="Enter The YouTube Video Url Here :")
video_url = ctk.CTkEntry(content_frame, width=400, height=40)

url_label.pack(padx=5,pady=10)
video_url.pack(padx=5,pady=10)

# Create a check button to select audio-only download
audio_only_var = ctk.BooleanVar()
audio_only_checkbox = ctk.CTkCheckBox(content_frame, text="Download Audio Only", variable=audio_only_var)
audio_only_checkbox.pack(padx=5, pady=5)

# Create a download button
download_button = ctk.CTkButton(content_frame, text="Download", command=download_video)
download_button.pack(padx=5,pady=10)

# Create resolution combo box (dropdown menu)
resolution_list = ["1080p","720p","480p","360p","240p"]
resolution_var = ctk.StringVar()
resolution_combobox = ttk.Combobox(content_frame, values=resolution_list, textvariable=resolution_var)
resolution_combobox.pack(padx=5,pady=10)
resolution_combobox.set("720p")

# Create a label and progress bar to display download progress
progress_label = ctk.CTkLabel(content_frame, text="0%")
progress_bar = ctk.CTkProgressBar(content_frame, width=400)
progress_bar.set(0.0)

# Create Status label
status_label = ctk.CTkLabel(content_frame, text="")


# To start the app
root.mainloop()