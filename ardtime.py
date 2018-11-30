import time
import httplib
import serial
import requests
import os
import socket

HTTPS_LED = 0
DNS_LED   = 1
PING_LED  = 2

DELAY = 30


def checkHTTPS(domain):
    try:
        c = httplib.HTTPSConnection(domain)
        c.request("GET", "/")
        response = c.getresponse()
        #print(response.status, response.reason)
        data = response.read()
        return 0
    except Exception as e:
        print(e)
        return 1

def checkWeb(url):
    try:
        r = requests.get(url)
        if r.status_code == 200:
            return 0
        else:
            return 1
    except Exception as e:
        print(e)
        return 1

def checkPing(target):
    return os.system("ping -c 1 " + target +" >/dev/null")

def checkTeamSpeak(target):
    
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(3)
    try:
        s.connect((target, 10011))
    except:
        print("Failed to connect to teamspeak")
        return 1
    # reduce the timeout
    data = s.recv(4096)

    if data.startswith("TS3"):
        return 0
    else:
        print("Got wrong welcome message from teamspeak")
        print(data)
        return 1

def createBitmask(*argv):
    i = 0
    bitmask = 0

    for arg in argv:
        bitmask |= arg << i
        i+=1

    return bitmask


if __name__ == "__main__":

    ser = serial.Serial("/dev/ttyACM0",9600)

    print("Waiting for the arduino to finish to boot")
    time.sleep(1)

    while True:

        https_val = 0
        dns_val = 0
        ping_val = 0
        web_val = 0
        teamspeak_val = 0

        https_val |= checkHTTPS("edznux.fr")
        https_val |= checkHTTPS("schweisguth.fr")
        https_val |= checkHTTPS("edouard.schweisguth.fr")

        ping_val |= checkPing("edznux.fr")
        ping_val |= checkPing("acidburn.edznux.fr")
        ping_val |= checkPing("schweisguth.fr")
        ping_val |= checkPing("edouard.schweisguth.fr")

        web_val |= checkWeb("https://edznux.fr")
        web_val |= checkWeb("https://edouard.schweisguth.fr")
        web_val |= checkWeb("https://schweisguth.fr")
        web_val |= checkWeb("https://edznux.github.io")

        teamspeak_val |= checkTeamSpeak("edznux.fr")

        bitmask = createBitmask(https_val, web_val, teamspeak_val)

        print(bin(bitmask))

        ser.flushInput()
        ser.write("V" + str(bitmask))

        time.sleep(DELAY)

