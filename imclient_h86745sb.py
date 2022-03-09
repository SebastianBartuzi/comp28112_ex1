import im
import time
import atexit
server = im.IMServerProxy('https://web.cs.manchester.ac.uk/h86745sb/COMP28112_ex1/IMserver.php')

if server['user1'] == b'logged\n' and server['user2'] == b'logged\n':
    print("Two users are logged in. Wait until one of them logs off.")
    while (server['user1'] == b'logged\n' and server['user2'] == b'logged\n'): #Wait until someone logs off
        time.sleep(0.5)

if server['user1'] == b'unlogged\n': # user1 is not logged in. Log in as user1
    server['user1'] = 'logged'
    user = False # False is for user1
    print("Logged in as user1.")
    if (server['user2'] == b'unlogged\n'):
        print("User2 is not logged in. Wait until they log in.")
        while (server['user2'] == b'unlogged\n'): # Wait until user2 logs in
            time.sleep(0.5)

else: # user1 is logged in. user2 is not logged in. Log in as user2
    server['user2'] = 'logged'
    user = True # True is for user2
    print("Logged in as user2.")

# Both users are logged in. Start conversation

# Give users initial states
if user == False: # user1
    responding = True
    waiting = False
else: # user2
    responding = False
    waiting = True

conversationHistory = []
server['userTurn'] = '1'
while True:
    if responding:
        message = input("Type your message: ")
        conversationHistory.append(message)
        server['lastMessage'] = message
        if user == False: # user1
            server['userTurn'] = '2' # It is turn for user2 to read and reply
        else: # user2
            server['userTurn'] = '1' # It is turn for user1 to read and reply
        responding = False
        waiting = True
    if waiting:
        if user == False: # user1
            while server['userTurn'] == b'2\n': # user1 waits for their turn
                time.sleep(0.5)
            print("User2: " + server['lastMessage'].decode('UTF-8'))
        else: # user2
            while server['userTurn'] == b'1\n': # user2 waits for their turn
                time.sleep(0.5)
            print("User1: " + server['lastMessage'].decode('UTF-8'))
        responding = True
        waiting = False
