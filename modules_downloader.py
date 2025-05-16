import colorama
import os

colorama.init(autoreset=True)
green = colorama.Fore.GREEN
red = colorama.Fore.RED
yellow = colorama.Fore.YELLOW
blue = colorama.Fore.BLUE
magenta = colorama.Fore.MAGENTA
cyan = colorama.Fore.CYAN
white = colorama.Fore.WHITE
filesinfolder = [f for f in os.listdir(".") if os.path.isfile(f)]
system = ""

def py_install():
    while True:
        global system
        system = input(yellow + "Select your operating system. (supported only linux or windows): ").lower()
        if system == "windows":
            print(green + "OK, starting python installation...")
            os.system("winget install Python.Python.3")
            break
        elif system == "linux":
            print(green + "OK, starting python installation...")
            os.system("sudo apt-get install python3")
            break
        else:
            print(red + f"Error, {system} is not a valid operating system")
            continue
    return

def get_inputs():
    print(magenta + r""" __  __           _       _                              
|  \/  | ___   __| |_   _| | ___  ___                    
| |\/| |/ _ \ / _` | | | | |/ _ \/ __|                   
| |  | | (_) | (_| | |_| | |  __/\__ \                   
|_|__|_|\___/ \__,_|\__,_|_|\___||___/       _           
|  _ \  _____      ___ __ | | ___   __ _  __| | ___ _ __ 
| | | |/ _ \ \ /\ / / '_ \| |/ _ \ / _` |/ _` |/ _ \ '__|
| |_| | (_) \ V  V /| | | | | (_) | (_| | (_| |  __/ |   
|____/ \___/ \_/\_/ |_| |_|_|\___/ \__,_|\__,_|\___|_|   """)
    while True:
        if input(yellow + "Do you have python installed? (y/n) ").lower() == "n":
            if input(yellow + "OK, we will have to install it, do you want to proceed? (y/n): ").lower() == "y":
                py_install()
            else:
                continue
        print(green + "Nice, select from which file you want to download modules, or send module name.")
        number = 0
        for file in filesinfolder:
            if file not in ["README.MD", "modules.exe"]:
                number += 1
                print(green + f"{str(number)}. {file}")
        inp = input(yellow)
        r = search_nuber(inp)
        if r:
            modules = modules_from_file(r)
            download_modules(modules)
            continue
        r = search_filename(inp)
        if r:
            modules = modules_from_file(r)
            download_modules(modules)
            continue
        else:
            download_modules([inp])

def search_nuber(inp):
    try:
        index = int(inp) - 1
        gfile = filesinfolder[index]
        return gfile
    except ValueError:
        return False
    except IndexError:
        print(red + f"Error: There are not {len(filesinfolder)} files in the folder!")
        return False

def search_filename(inp):
    try:
        with open(inp, "r") as file:
            inside = file.readlines()
        return inp
    except FileNotFoundError:
        return False

def modules_from_file(file):
    modules = set()
    with open(file, "r") as f:
        lines = f.readlines()
    for line in lines:
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("import "):
            imported = line.replace("import", "").strip()
            for mod in imported.split(","):
                modules.add(mod.strip().split(" ")[0])
        elif line.startswith("from "):
            parts = line.split()
            if len(parts) >= 2:
                modules.add(parts[1])
    return list(modules)

def download_modules(modules):
    global system
    if isinstance(modules, str):
        modules = [modules]
    if system == "":
        system = input(yellow + "Select your operating system. (supported only linux or windows): ").lower()
    if system == "windows":
        for module in modules:
            os.system(f"pip install {module}")
        print(blue + "All modules downloaded successfully!")
    elif system == "linux":
        for module in modules:
            apt_name = f"python3-{module.lower()}"
            print(yellow + f"Trying to install {apt_name} via apt...")
            os.system(f"sudo apt-get install -y {apt_name}")
        print(blue + "All modules downloaded (or attempted) via apt! If any error appeared try running this program as administrator using sudo.")
    else:
        print(red + "Unsupported operating system.")

if __name__ == "__main__":
    get_inputs()
