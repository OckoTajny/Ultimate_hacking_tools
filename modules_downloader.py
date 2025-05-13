import colorama
import os

green = colorama.Fore.GREEN
red = colorama.Fore.RED
yellow = colorama.Fore.YELLOW
blue = colorama.Fore.BLUE
magenta = colorama.Fore.MAGENTA
cyan = colorama.Fore.CYAN
white = colorama.Fore.WHITE

def py_install():
    while True:
        system = input(yellow + "Select your operating system. (supported only linux or windows)").lower()
        if system == "windows":
            print(green + "OK, starting python instalation...")
            os.system("winget install Python.Python.3")
            break
        elif system == "linux":
            print(green + "OK, starting python instalation...")
            os.system("sudo apt-get install python3")
            break
        else:
            print(red + f"Error, {system} is not a valid operating system")
            continue
    return


print(magenta + """                     _       _                           
 _ __ ___   ___   __| |_   _| | ___  ___                 
| '_ ` _ \ / _ \ / _` | | | | |/ _ \/ __|                
| | | | | | (_) | (_| | |_| | |  __/\__ \                
|_| |_| |_|\___/ \__,_|\__,_|_|\___||___/    _           
  __| | _____      ___ __ | | ___   __ _  __| | ___ _ __ 
 / _` |/ _ \ \ /\ / / '_ \| |/ _ \ / _` |/ _` |/ _ \ '__|
| (_| | (_) \ V  V /| | | | | (_) | (_| | (_| |  __/ |   
 \__,_|\___/ \_/\_/ |_| |_|_|\___/ \__,_|\__,_|\___|_|   """)
while True:
    if input(yellow + "Do you have python installed? (y/n) ").lower() == "n":
        if input(yellow + "OK, we will have to install it, do you want to proceed?").lower() == "y":
            py_install()
        else:
            continue