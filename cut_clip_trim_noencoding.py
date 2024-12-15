from moviepy import VideoFileClip
import subprocess

# Function to cut video based on start and end time
def cut_video(input_video, timestamps,output_name):
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

# Example usage
output_filename = [
    "01_Introduction.mp4",
    "02_Installing_OpenCV_and_Cae.mp4",
    "03_Reading_Images_and_Video.mp4",
    "04_Resizing_and_Rescaling_Frames.mp4",
    "05_Drawing_Shapes_and_Putting_Text.mp4",
    "06_Essential_Functions_in_OpenCV.mp4",
    "07_Image_Transformations.mp4",
    "08_Contour_Detection.mp4",
    "09_Color_Spaces.mp4",
    "10_Color_Channels.mp4",
    "11_Blurring.mp4",
    "12_BITWISE_operations.mp4",
    "13_Masking.mp4",
    "14_Histogram_Computation.mp4",
    "15_Thresholding_Binarizing_Images.mp4",
    "16_Edge_Detection.mp4",
    "17_Face_Detection_with_Haar_Cascades.mp4",
    "18_Face_Recognition_with_OpenCV.mp4",
    "19_Deep_Computer_Vision_The_Simpsons.mp4"
]

timestamps = [
    ("00:00:00", "01:07"),
    ("01:07", "04:12"),
    ("04:12", "12:57"),
    ("12:57", "20:21"),
    ("20:21", "31:55"),
    ("31:55", "44:18"),
    ("44:18", "57:06"),
    ("57:06", "1:12:58"),
    ("1:12:58", "1:23:10"),
    ("1:23:10", "1:31:03"),
    ("1:31:08", "1:44:27"),
    ("1:44:27", "1:58:06"),
    ("1:58:06", "2:01:43"),
    ("2:01:43", "2:15:22"),
    ("2:15:22", "2:26:27"),
    ("2:26:27", "2:35:25"),
    ("2:35:25", "2:49:05"),
    ("2:49:05", "3:11:57"),
    ("3:11:57", "3:41:41")
]

cut_video("input_video.mp4", timestamps,output_filename)
