import os
import colorama

green = colorama.Fore.GREEN
red = colorama.Fore.RED
yellow = colorama.Fore.YELLOW
blue = colorama.Fore.BLUE
magenta = colorama.Fore.MAGENTA
cyan = colorama.Fore.CYAN
white = colorama.Fore.WHITE

print(green + """
Choose a cypher or send exit to go back to main:
1. Base""")
while True:
    i = input(yellow + "Cypher: ")
    if i == "1":
        os.system("python base64_crypter.py")
    elif i == "exit":
        os.system("python main.py")
    else:
        print(red + f"{i} is not a valid choice.")