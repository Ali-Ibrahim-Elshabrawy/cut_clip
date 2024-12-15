from moviepy import VideoFileClip
import subprocess
import re

def get_last_timestamp(video_path):
    # Load the video using moviepy
    video = VideoFileClip(video_path)
    
    # Get the duration of the video in seconds
    duration = video.duration
    
    # Convert the duration into HH:MM:SS format
    hours = int(duration // 3600)
    minutes = int((duration % 3600) // 60)
    seconds = int(duration % 60)
    
    # Format the last timestamp as HH:MM:SS
    last_timestamp = f"{hours:02}:{minutes:02}:{seconds:02}"
    
    return last_timestamp

def process_text(input_text,video_path):
    last_timestamp = get_last_timestamp(video_path)
    # Regular expression to match timestamps (HH:MM:SS format) followed by text
    pattern = r"(\d{2}:\d{2}:\d{2})\s(.+)"
    
    # Split input into lines
    lines = input_text.strip().split("\n")
    
    # Initialize lists for timestamps and filenames
    timestamps = []
    filenames = []
    
    for i,line in enumerate(lines):
        # Use regex to find the timestamp and text
        match = re.match(pattern, line)
        video_timestamps = []
        
        if match:
            timestamp = match.group(1)
            text = match.group(2)
            
            # Append timestamp to the timestamps list
            timestamps.append(timestamp)
            
            # Generate a filename based on the text, here we just use the first few words
            # Remove non-alphanumeric characters and replace spaces with underscores
            filename = str(i).zfill(2) + "-" + re.sub(r'[^a-zA-Z0-9\s]', '', text).replace(' ', '_') + '.mp4'
            filenames.append(filename)
    for i in range(0,len(timestamps)):
        if i == len(timestamps)-1:
            video_timestamps.append((timestamps[i],last_timestamp))
        else:
            video_timestamps.append((timestamps[i],timestamps[i+1]))
    
    return video_timestamps, filenames

# Function to cut video based on start and end time
def cut_video_encoding(input_video, timestamps,output_name):
    video = VideoFileClip(input_video)
    for i, (start, end) in enumerate(timestamps):
        cut_clip = video.subclipped(start, end)
        cut_clip.write_videofile(output_name[i], codec="libx264", audio_codec="aac",threads = 8)

# Function to cut video based on start and end time
def cut_video_no_encoding(input_video, timestamps,output_name):
    video = VideoFileClip(input_video)
    for i, (start, end) in enumerate(timestamps):
        # Use FFmpeg directly for cutting without re-encoding
        command = [
            'ffmpeg', 
            '-i', input_video,           # Input file
            '-ss', start,                # Start time
            '-to', end,                  # End time
            '-c:v', 'copy',              # Copy video without re-encoding
            '-c:a', 'copy',              # Copy audio without re-encoding
            output_name[i]
        ]
        
        subprocess.run(command)
    
# Sample input text
input_text = """
00:00:00 Intro
00:00:30 Introduction to Containers
00:19:49 Container Architecture
00:50:14 Introduction to Docker
01:07:38 Installing Docker
01:27:17 Container = Application
01:43:21 Docker Engine Architecture
01:51:17 Images - Deep Dive
02:37:17 Docker in VSCode
02:48:28 Containers - Deep Dive
03:03:40 Network
03:47:31 Storage
04:22:22 Containerizing an Application
04:55:23 Dockerfile - Deep Dive
06:05:38 Image Registries
06:16:10 Docker Compose
07:04:52 Docker Swarm
08:04:17 Docker Stack
08:27:15 Portainer
08:36:37 Introduction to Kubernetes
08:41:25 K8s High Level Architecture
08:56:10 Installing Minikube
09:07:56 K8s Logical Architecture 
09:23:26 K8s Sample Deployment
10:01:21 K8s in VSCode
10:05:52 Jupyter in Containers
"""

timestamps, output_filename = process_text(input_text,'input_file.mp4')
# print(timestamps)
# print(output_filename)
cut_video_no_encoding("input_file.mp4", timestamps,output_filename)