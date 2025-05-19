import colorama
import os
import time

green = colorama.Fore.GREEN
red = colorama.Fore.RED
magenta = colorama.Fore.MAGENTA

os.system("cls" if os.name == "nt" else "clear")
print(green + r"""
 _____                      _               
/  __ \                    | |              
| /  \/ _ __  _   _  _ __  | |_   ___  _ __ 
| |    | '__|| | | || '_ \ | __| / _ \| '__|
| \__/\| |   | |_| || |_) || |_ |  __/| |   
 \____/|_|    \__, || .__/  \__| \___||_|   
               __/ || |                     
              |___/ |_|      
                     
""")

ascii_text = "placeholder"
converted_bits = "placeholder"
converted_key = "placeholder"
ascii_key = "placeholder"

def get_inputs():
    ascii_text = input(green + "Enter the text you want to encrypt: ")
    converted_text = ''.join(format(ord(i), '08b') for i in ascii_text)
    ascii_key = input(green + "Enter the key: ")
    converted_key = ''.join(format(ord(i), '08b') for i in ascii_key)
    print(green + f"Binary: {converted_key}")
    print(green + f"Key: {converted_key}")

def crypt(text, key):
    # Placeholder implementation for the crypt function
    pass

def main():
    get_inputs()
    print("L")

if __name__ == "__main__":
    main()
