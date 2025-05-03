#imports
import colorama
import socket
import time
import os
import multiprocessing

#variables setup
green = colorama.Fore.GREEN
red = colorama.Fore.RED
yellow = colorama.Fore.YELLOW
blue = colorama.Fore.BLUE
magenta = colorama.Fore.MAGENTA
cyan = colorama.Fore.CYAN
white = colorama.Fore.WHITE
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


#getting imports
def get_inputs():
    os.system("cls" if os.name == "nt" else "clear")
    print(green + r"""
 ____            _                                         
|  _ \ ___  _ __| |_   ___  ___ __ _ _ __  _ __   ___ _ __ 
| |_) / _ \| '__| __| / __|/ __/ _` | '_ \| '_ \ / _ \ '__|
|  __/ (_) | |  | |_  \__ \ (_| (_| | | | | | | |  __/ |   
|_|   \___/|_|   \__| |___/\___\__,_|_| |_|_| |_|\___|_|   """)
    ip = input(yellow + "Enter ip you want to scan, if you know only the domain name, type domain: ")
    results = ""
    if ip == "domain":
        domain = input(yellow + "Enter domain name: ")
        ip = socket.gethostbyname(domain)
        print(blue + f"IP adress of {domain} is {ip}")
    try:
        ports = int(input(yellow + "How many ports do you want to scan (max is 65535): "))
        if ports <= 65535 and ports > 0:
            s.settimeout(1)
            print(green + f"Scanning {ip} for active ports, this may take a while...")
            for port in range(1, ports):
                result = search(ip, port)
                if result == "Active":
                    results = results + blue + str(port) + ":" + green + result + "\n"
                elif result == "Closed":
                    results = results + blue + str(port) + ":" + red + result + "\n"
                continue
            print_results(results)
        else:
            print(red + "Error, port must be between 1 and 65535.")
            time.sleep(3)
            get_inputs()
    except ValueError:
        print(red + "Error, port must be a number.")
        time.sleep(3)
        get_inputs()

#Test if port is active or not
def search(ip, port):
    result = s.connect_ex((ip, port))
    s.close()
    if result == 0:
        result = "Active"
    else:
        result = "Closed"
    return result

#print results
def print_results(results):
    print(blue + results)
    a = input(yellow + "Do you want to start another scan? (y/n): ")
    if a.lower() == "y":
        get_inputs()
    else:
        print(red + "OK, quitting")
        time.sleep(2)

get_inputs()