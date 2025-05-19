import os
import colorama
from instagrapi import Client
from moviepy import VideoFileClip

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


def convert_video_for_instagram(input_path: str, output_path: str) -> str:
    """
    Converts a video to a vertical 9:16 mp4 format for Instagram Reels.
    """
    print(yellow + "\n[+] Converting video to vertical 9:16 format...\n")
    clip = VideoFileClip(input_path)
    w, h = clip.size

    target_width = 1080
    target_height = 1920

    if w / h != 9 / 16:
        clip = clip.resize(width=target_width)
        clip = clip.crop(y_center=h // 2, width=target_width, height=target_height)

    clip.write_videofile(output_path, codec="libx264", audio_codec="aac")
    print(green + "[✓] Video conversion complete.\n")
    return output_path


def upload_instagram_reel(username: str, password: str, video_path: str, caption: str):
    """
    Logs into Instagram and uploads a video as a Reel (clip).
    Accepts Windows paths with backslashes and spaces.
    """
    cl = Client()

    # Normalize the path (převod zpětných lomítek, odstranění nadbytečných částí)
    video_path = os.path.normpath(video_path)

    try:
        cl.login(username, password)
    except Exception as e:
        print(red + "Login failed:", e)
        return None

    try:
        media = cl.clip_upload(video_path, caption)
        print(blue + "Reel uploaded successfully!")
        print("URL:", f"https://www.instagram.com/reel/{media.pk}/")
        return media
    except Exception as e:
        print(red + "Error during upload:", e)
        return None


if __name__ == "__main__":
    username = input(green + "your_username: ")
    password = input(green + "your_password: ")
    original_video = input(green + "path/to/your/video.mp4: ")
    caption = input(green + "caption here: ")

    converted_video = "converted_reel.mp4"
    convert_video_for_instagram(original_video, converted_video)

    upload_instagram_reel(username, password, converted_video, caption)
