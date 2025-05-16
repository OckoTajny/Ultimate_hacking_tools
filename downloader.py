import os
import colorama

green = colorama.Fore.GREEN
red = colorama.Fore.RED
yellow = colorama.Fore.YELLOW
blue = colorama.Fore.BLUE
magenta = colorama.Fore.MAGENTA
cyan = colorama.Fore.CYAN
white = colorama.Fore.WHITE

os.system("cls" if os.name == "nt" else "clear")
print(magenta + r""" _   _ _ _   _                 _                         
| | | | | |_(_)_ __ ___   __ _| |_ ___                   
| | | | | __| | '_ ` _ \ / _` | __/ _ \                  
| |_| | | |_| | | | | | | (_| | ||  __/                  
 \___/|_|\__|_|_| |_| |_|\__,_|\__\___|      _           
|  _ \  _____      ___ __ | | ___   __ _  __| | ___ _ __ 
| | | |/ _ \ \ /\ / / '_ \| |/ _ \ / _` |/ _` |/ _ \ '__|
| |_| | (_) \ V  V /| | | | | (_) | (_| | (_| |  __/ |   
|____/ \___/ \_/\_/ |_| |_|_|\___/ \__,_|\__,_|\___|_|   """)
print(green + """
Choose your what you want to download:
1. Python modules""")
while True:
    a = input(yellow)
    if a == "1":
        os.system("python downloaders/modules_downloader.py")
    else:
        print(red + f"{a} is not a valid choice.")
        continue