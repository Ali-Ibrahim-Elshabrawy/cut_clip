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

def process_text(input_text,video_path,start = 0):
    
    last_timestamp = get_last_timestamp(video_path)
    # Regular expression to match timestamps (HH:MM:SS format) followed by text
    pattern = r"(\d{2}:\d{2}:\d{2})\s(.+)"
    
    # Split input into lines
    lines = input_text.strip().split("\n")
    if start > len(lines):
        print("check start value as it's greater than total number of sections")
    # Initialize lists for timestamps and filenames
    timestamps = []
    filenames = []
    
    for i,line in enumerate(lines):
        if i < start:
            continue
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
00:00:00 Introduction
00:00:11 Variables
00:24:02 Strings
00:46:00 Object Types
01:12:15 Boolean
01:37:17 Comments
01:41:21 Sequences (Iterables)
01:45:10 Lists
02:22:09 range()
02:43:42 Tuples
02:50:40 Strings as Iterables
02:54:46 Sets
03:04:34 Dictionaries
03:28:18 Strings - A Deeper Look
04:06:06 If Statement
04:37:55 while Loop
04:55:32 for Loop
05:35:45 Functions
06:36:29 Classes
08:25:24 Modules and Packages
08:59:00 Python Standard Library Tour
09:37:55 Working with Files
10:16:02 Testing and Exception Handling
10:52:52 Bonus and Quiz
"""
start_cut = 0
timestamps, output_filename = process_text(input_text,'input_file.mp4',start = start_cut)
# print(timestamps)
# print(output_filename)
cut_video_no_encoding("input_file.mp4", timestamps,output_filename,)