import colorama
import os
import random  # Importing random module for generating random characters
import string  # Importing string module for character sets

red = colorama.Fore.RED
green = colorama.Fore.GREEN

# Remove the space character from the ASCII characters list
ascii_chars = [char for char in string.printable if char != ' ']
# List of alphanumeric characters
alphanumeric_chars = list(string.ascii_letters + string.digits)

def generate_password():
    length = int(input(green + "Enter the length of the password: "))
    if length < 1:
        os.system('cls' if os.name == 'nt' else 'clear')
        print(red + "Password length must be at least 1.")
        generate_password()
    choice = input(green + "Choose a password type:\n1. Alphanumeric\n2. ASCII\n")
    if choice == "1":
        for char in range(5):
            password = ''.join(random.choice(alphanumeric_chars) for _ in range(length))
            print(green + f"Generated Password {char + 1}: {password}")
    elif choice == "2":
        for char in range(5):
            password = ''.join(random.choice(ascii_chars) for _ in range(length))
            print(green + f"Generated Password {char + 1}: {password}")
    else:
        os.system('cls' if os.name == 'nt' else 'clear')
        print(red + "Invalid choice. Please select 1 or 2.")
        generate_password()
        
def main():
    print(green + "Welcome to the Password Generator!")
    while True:
        generate_password()
        again = input(green + "Do you want to generate another password? (y/n): ").lower()
        if again != 'y':
            print(green + "Thank you for using the Password Generator!")
            break
        os.system('cls' if os.name == 'nt' else 'clear')
        
if __name__ == "__main__":
    main()
