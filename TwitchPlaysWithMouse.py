#06/04/2021 Carlos Astengo Macias

#Designed for Chess.com on full screen in a 1920*1080 resolution

# Documentation:
# Twitch IRC connection: https://dev.twitch.tv/docs/irc/guide
# Python socket: https://docs.python.org/3/library/socket.html#functions
# Pyautogui: https://pyautogui.readthedocs.io/en/latest/keyboard.html
# Pynput: https://pynput.readthedocs.io/en/latest/index.html
# Get OAuth key: https://twitchapps.com/tmi/
#Chess.com site: https://www.chess.com/play/computer

import socket
import pyautogui
from pynput.mouse import Button, Controller
from pynput.keyboard import Listener, KeyCode
import time

#Twitch address and port found in documentation
address = "irc.twitch.tv"
port = 6667

#User credentials
oauthKey = ""
nickname = ""
channelName = ""

#Starts connection with irc and sends credentials
irc = socket.socket()
irc.connect((address, port)) 
irc.send(("PASS " + oauthKey + "\n" + "NICK " + nickname + "\n" + "JOIN #" + channelName + "\n").encode())

mouse = Controller()

def main():

    #Clicks a specific position on the screen
    def Click(x,y):
        mouse.position = (x,y)
        mouse.click(Button.left,1)

    #Checks if the message contains a valid input and correct format (example "!d2-d4")
    def ValidateInput(moveInput):
        try:
            moveInput = moveInput.lower()
            if moveInput[3] == "-":
                if ord(moveInput[1]) >= 97 and ord(moveInput[1]) <= 104 and ord(moveInput[4]) >= 97 and ord(moveInput[4]) <= 104:
                    if int(moveInput[2]) >= 1 and int(moveInput[2]) <= 8 and int(moveInput[5]) >= 1 and int(moveInput[5]) <= 8:
                        x = 425 + (ord(moveInput[1])-97)*100
                        y = 925 - (int(moveInput[2])-1)*100
                        Click(x,y)
                        time.sleep(0.01)
                        x = 425 + (ord(moveInput[4])-97)*100
                        y = 925 - (int(moveInput[5])-1)*100
                        Click(x, y)
                        mouse.position = (0,0)
        except:
            print("Invalid input")

    #Checks if the program has correctly connected by looking for the message ">"
    #According to the irc documentation when you see that message you have correctly connected
    def ConfirmConnection():
        isJoining = True
        while isJoining:
            reader = irc.recv(1024)
            reader = reader.decode()
            for line in reader.split("\n"):
                print(line)
                if ">" in line:
                    print("\n" + "Bot has successfully connected to the channel.")
                    isJoining = False

    #Splits the string to get the user that sent the message
    def GetUser(line):
        separate = line.split(":", 2)
        user = separate[1].split("!", 1)[0]
        return user

    #Splits the string to get the message the user sent
    def GetMesssage(line):
        try:
            message = (line.split(":", 2)[2])
        except:
            message = ""
        return message

    ConfirmConnection()

    while True:
        #Receives new messages from chat
        try:
            reader = irc.recv(1024)
            reader = reader.decode()
        except:
            reader = ""
        
        for line in reader.split("\r\n"):
            if(line == ""):
                continue
            
            #if the line contains PRIVMSG it means that it was sent by a user
            elif "PRIVMSG" in line:
                user = GetUser(line)
                message = GetMesssage(line)
                print(user + " : " + message)
                if message[0] == "!" and len(message) == 6:
                    ValidateInput(message)

            #According to twitch documentation:
                # “About once every five minutes, the server will send you a PING :tmi.twitch.tv. 
                # To ensure that your connection to the server is not prematurely terminated, reply with PONG :tmi.twitch.tv.
            elif "PING" in line:
                print(line)
                message = "PONG tmi.twitch.tv\r\n".encode()
                irc.send(msgg)
                print(msgg)
                continue

main()