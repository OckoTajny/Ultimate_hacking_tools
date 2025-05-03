import os
import colorama

green = colorama.Fore.GREEN
red = colorama.Fore.RED
yellow = colorama.Fore.YELLOW
blue = colorama.Fore.BLUE
magenta = colorama.Fore.MAGENTA
cyan = colorama.Fore.CYAN
white = colorama.Fore.WHITE

print(magenta + """
 _   _ _ _   _                 _       
| | | | | |_(_)_ __ ___   __ _| |_ ___ 
| | | | | __| | '_ ` _ \ / _` | __/ _ \
| |_| | | |_| | | | | | | (_| | ||  __/
 \___/|_|\__|_|_| |_| |_|\__,_|\__\___|
| |__   __ _  ___| | _(_)_ __   __ _   
| '_ \ / _` |/ __| |/ / | '_ \ / _` |  
| | | | (_| | (__|   <| | | | | (_| |  
|_| |_|\__,_|\___|_|\_\_|_| |_|\__, |  
| |_ ___   ___ | |___          |___/   
| __/ _ \ / _ \| / __|                 
| || (_) | (_) | \__ \                 
 \__\___/ \___/|_|___/                 
""")
print(green + """
1. DDOS attack
2. Password generator""")
while True:
    a = input(magenta + "Choose a number: ")
    if a == "1":
        os.system("python ddos.py")
    elif a == "2":
        os.system("python random_password.py")
    else:
        print(red + f"{a} is not a valid number.")
        continue
