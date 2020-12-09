import socket, string

# Set all the variables necessary to connect to Twitch IRC
HOST = "irc.twitch.tv"
NICK = "Your_username"
PORT = 6667
PASS = "oauth:somenumbersandletters"
readbuffer = ""
MODT = False

# Connecting to Twitch IRC by passing credentials and joining a certain channel
s = socket.socket()
s.connect((HOST, PORT))
s.send(("PASS " + PASS + "\r\n").encode())
s.send(("NICK " + NICK + "\r\n").encode())
s.send(('JOIN #thenameofthechannel\r\n').encode())

# Method for sending a message (NOT TESTED)
def Send_message(message):
    s.send("PRIVMSG #YOURCHANNELNAME :" + message + "\r\n")


while True:
    readbuffer = readbuffer + s.recv(1024).decode()
    temp = readbuffer.split("\n")
    readbuffer = temp.pop()

    for line in temp:
        # Checks whether the message is PING because its a method of Twitch to check if you're afk
        if (line[0] == "PING"):
            s.send("PONG %s\r\n" % line[1])
        else:
            # Splits the given string so we can work with it better
            parts = line.split( ":")

            if "QUIT" not in parts[1] and "JOIN" not in parts[1] and "PART" not in parts[1]:
                try:
                    # Sets the message variable to the actual message sent
                    message = parts[2][:len(parts[2]) - 1]
                except:
                    message = ""
                # Sets the username variable to the actual username
                usernamesplit = parts[1].split("!")
                username = usernamesplit[0]

                # Only works after twitch is done announcing stuff (MODT = Message of the day)
                if MODT:
                    print (username + ": " + message)

                    print(line[0])

                    print(line)
                    print("================================================================")

                    # You can add all your plain commands here (NOT TESTED)
                    if message == "Hey":
                        Send_message("Welcome to my stream, " + username)

                for l in parts:
                    if "End of /NAMES list" in l:
                        MODT = True
