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
print(magenta + r"""
 ____            _                                         
|  _ \ ___  _ __| |_   ___  ___ __ _ _ __  _ __   ___ _ __ 
| |_) / _ \| '__| __| / __|/ __/ _` | '_ \| '_ \ / _ \ '__|
|  __/ (_) | |  | |_  \__ \ (_| (_| | | | | | | |  __/ |   
|_|   \___/|_|   \__| |___/\___\__,_|_| |_|_| |_|\___|_|   """)