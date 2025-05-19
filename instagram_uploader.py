import os
import colorama
from instagrapi import Client

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


def upload_instagram_reel(username: str, password: str, video_path: str, caption: str):
    """
    Logs into Instagram and uploads a video as a Reel (clip).

    :param username: Instagram username
    :param password: Instagram password
    :param video_path: Path to the .mp4 video file
    :param caption: Caption text for the Reel
    :return: Returns the uploaded media object if successful, else None
    """
    cl = Client()

    try:
        cl.login(username, password)
    except Exception as e:
        print("Login failed:", e + red)
        return None

    try:
        media = cl.clip_upload(video_path, caption)
        print("Reel uploaded successfully!" + blue)
        print("URL:", f"https://www.instagram.com/reel/{media.pk}/" + blue)
        return media
    except Exception as e:
        print("Error during upload:", e + red)
        return None

while __name__ == "__main__":
    upload_instagram_reel(
    username=input("your_username: " + green),
    password=input("your_password: " +green),
    video_path=input("path/to/your/video.mp4: " + green),
    caption=input("caption here: " + green)
)
