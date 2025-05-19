import os
import json
import colorama
from pathlib import Path
from instagrapi import Client
from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip

# Configuration setup
CONFIG_DIR = Path("reels")
CONFIG_FILE = CONFIG_DIR / "data.json"
CONFIG_DIR.mkdir(exist_ok=True)

# Color setup
colorama.init()
GREEN = colorama.Fore.GREEN
RED = colorama.Fore.RED
YELLOW = colorama.Fore.YELLOW
BLUE = colorama.Fore.BLUE
MAGENTA = colorama.Fore.MAGENTA


def load_config():
    """Load previous configuration if exists"""
    if CONFIG_FILE.exists():
        with open(CONFIG_FILE, "r") as f:
            return json.load(f)
    return None


def convert_video_for_instagram(input_path, output_path):
    """
    Converts a video to a vertical 9:16 mp4 format suitable for Instagram Reels.
    """
    try:
        print(f"{YELLOW}\n[+] Converting video to Instagram format (9:16)...")

        clip = VideoFileClip(input_path)
        w, h = clip.size

        # Target dimensions for Instagram Reels (9:16 aspect ratio)
        target_width = 1080
        target_height = 1920

        # Resize and crop if needed
        if w / h != 9 / 16:
            clip = clip.resize(width=target_width)
            # Center crop to 9:16
            clip = clip.crop(x_center=clip.w / 2, y_center=clip.h / 2,
                             width=target_width, height=target_height)

        # Write with optimized settings for Instagram
        clip.write_videofile(output_path,
                             codec="libx264",
                             audio_codec="aac",
                             threads=4,
                             ffmpeg_params=['-crf', '22'])

        print(f"{GREEN}[✓] Video converted successfully for Instagram")
        return output_path

    except Exception as e:
        print(f"{RED}Error converting video for Instagram: {e}")
        return None


def upload_instagram_reel(username, password, video_path, caption):
    """
    Uploads a video as an Instagram Reel using instagrapi.
    """
    try:
        print(f"{YELLOW}\n[+] Logging into Instagram as {username}...")

        # Normalize path to handle spaces and special characters
        video_path = os.path.normpath(video_path)

        # Create client and login
        cl = Client()
        cl.login(username, password)

        print(f"{YELLOW}[+] Uploading reel to Instagram...")

        # Upload as clip/reel
        media = cl.clip_upload(video_path, caption)

        print(f"{GREEN}[✓] Reel uploaded successfully!")
        print(f"{BLUE}URL: https://www.instagram.com/reel/{media.pk}/")
        return media

    except Exception as e:
        print(f"{RED}Error uploading to Instagram: {e}")
        return None

def save_config(username, password, last_video, last_caption):
    """Save current configuration"""
    config = {
        "username": username,
        "password": password,
        "last_video": last_video,
        "last_caption": last_caption
    }
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f)


def get_input_with_memory():
    """Get user input with option to reuse previous values"""
    prev_config = load_config()

    if prev_config:
        reuse = input(f"{YELLOW}Use previous inputs? [y/N]: ").lower() == 'y'
        if reuse:
            return prev_config

    video_path = input(YELLOW + "Enter path to video file: ").strip('"')
    username = input(YELLOW + "Enter your Instagram username: ")
    password = input(YELLOW + "Enter your Instagram password: ")
    caption = input(YELLOW + "Enter caption text for the Reel: ")
    day = input(YELLOW + "Enter current day number: ")

    save_config(username, password, video_path, caption)
    return {
        "video_path": video_path,
        "username": username,
        "password": password,
        "caption": caption,
        "day": day
    }


def edit_video(video_path, text, new_filename):
    """Enhanced video editing with better error handling"""
    try:
        print(f"{YELLOW}\n[+] Processing video: {Path(video_path).name}")

        if not Path(video_path).exists():
            raise FileNotFoundError(f"Video file not found: {video_path}")

        with VideoFileClip(video_path) as video:
            txt_clip = TextClip(text, fontsize=70, color='white', font='Arial-Bold')
            txt_clip = txt_clip.with_position('center').with_duration(video.duration)

            result = CompositeVideoClip([video, txt_clip])
            result.write_videofile(
                new_filename,
                codec="libx264",
                audio_codec="aac",
                threads=4,
                ffmpeg_params=['-crf', '22']
            )

        print(f"{GREEN}[✓] Video saved as {new_filename}")
        return new_filename

    except Exception as e:
        print(f"{RED}Error processing video: {e}")
        return None


# ... (keep existing convert_video_for_instagram and upload_instagram_reel functions)

def main():
    os.system("cls" if os.name == "nt" else "clear")
    print(MAGENTA + "Instagram Reels Manager 2.0\n")

    inputs = get_input_with_memory()

    edited_video = f"VideoDay{inputs['day']}.mp4"
    final_video = f"VideoDay{inputs['day']}_instagram.mp4"

    if not (edited := edit_video(inputs['video_path'], inputs['caption'], edited_video)):
        return

    if not (converted := convert_video_for_instagram(edited, final_video)):
        return

    if input(f"{YELLOW}Upload to Instagram now? [y/N]: ").lower() == 'y':
        upload_instagram_reel(
            inputs['username'],
            inputs['password'],
            converted,
            inputs['caption']
        )


if __name__ == "__main__":
    main()
