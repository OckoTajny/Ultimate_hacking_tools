import os
import colorama
from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip


green = colorama.Fore.GREEN
red = colorama.Fore.RED
yellow = colorama.Fore.YELLOW
blue = colorama.Fore.BLUE
magenta = colorama.Fore.MAGENTA
cyan = colorama.Fore.CYAN
white = colorama.Fore.WHITE

os.system("cls" if os.name == "nt" else "clear")
print(magenta + r""" ___           _                                  
|_ _|_ __  ___| |_ __ _  __ _ _ __ __ _ _ __ ___  
 | || '_ \/ __| __/ _` |/ _` | '__/ _` | '_ ` _ \ 
 | || | | \__ \ || (_| | (_| | | | (_| | | | | | |
|___|_| |_|___/\__\__,_|\__, |_|  \__,_|_| |_| |_|
|  _ \ ___  ___| |___   |___/                     
| |_) / _ \/ _ \ / __|                            
|  _ <  __/  __/ \__ \                            
|_| \_\___|\___|_|___/                            
|  \/  | __ _| | _____ _ __                       
| |\/| |/ _` | |/ / _ \ '__|                      
| |  | | (_| |   <  __/ |                         
|_|  |_|\__,_|_|\_\___|_|                         """)

def edit_video(video_path, text):
    video = VideoFileClip(video_path)
    txt_clip = TextClip(text, fontsize=70, color='white')
    txt_clip = txt_clip.set_position('center').set_duration(video.duration)
    vysledek = CompositeVideoClip([video, txt_clip])
    vysledek.write_videofile("vystupni_video.mp4")
