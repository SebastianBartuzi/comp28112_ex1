import im
import time
import atexit
server = im.IMServerProxy('https://web.cs.manchester.ac.uk/h86745sb/COMP28112_ex1/IMserver.php')

# When one user closes terminal, log them off and delete lastMessage
def exit_handler():
    if logged:
        if not user: # user1
            print(user)
            server['user1'] = 'unlogged'
            del server['lastMessage']
            del server['userTurn']
        elif user: # user2
            print(user)
            server['user2'] = 'unlogged'
            del server['lastMessage']
            del server['userTurn']
atexit.register(exit_handler)

TIME_WAITING = 0.5

if server['user1'] == b'logged\n' and server['user2'] == b'logged\n':
    print("Two users are logged in. Wait until one of them logs off.")
    while (server['user1'] == b'logged\n' and server['user2'] == b'logged\n'): # Wait until someone logs off
        time.sleep(TIME_WAITING)

logged = True
if server['user1'] == b'unlogged\n': # user1 is not logged in. Log in as user1
    server['user1'] = 'logged'
    user = False # False is for user1
    print("Logged in as user1.")
    if (server['user2'] == b'unlogged\n'):
        print("User2 is not logged in. Wait until they log in.")
        while (server['user2'] == b'unlogged\n'): # Wait until user2 logs in
            time.sleep(TIME_WAITING)
elif server['user2'] == b'unlogged\n': # user1 is logged in. user2 is not logged in. Log in as user2
    server['user2'] = 'logged'
    user = True # True is for user2
    print("Logged in as user2.")
else:
    print("Logging error occured!")
    logged = False
    exit()

# Both users are logged in. Start conversation

conversationHistory = []
while True: # This loop is never left
    # Give users initial states
    server['userTurn'] = '1' # Always start with user1
    while True: # This loop is left only when the second user logs off
        # Replying
        if (
            (server['userTurn'] == b'1\n' and not user) or # user1 is replying
            (server['userTurn'] == b'2\n' and user) # user2 is replying
        ):
            if server['user1'] == b'unlogged\n' or server['user2'] == b'unlogged\n':
                break
            message = input("Type your message: ")
            print("\nYou sent: %s" % message)
            if server['user1'] == b'unlogged\n' or server['user2'] == b'unlogged\n':
                break
            conversationHistory.append(message)
            server['lastMessage'] = message
            if not user: # user1
                server['userTurn'] = '2' # It is turn for user2 to read and reply
            else: # user2
                server['userTurn'] = '1' # It is turn for user1 to read and reply
        # Waiting
        if (
            (server['userTurn'] == b'2\n' and not user) or # user1 is waiting
            (server['userTurn'] == b'1\n' and user) # user2 is waiting
        ):
            break_out_flag = False
            if not user: # user1
                while server['userTurn'] == b'2\n': # user1 waits for their turn
                    if server['user2'] == b'unlogged\n':
                        break_out_flag = True
                        break
                    time.sleep(TIME_WAITING)
                if break_out_flag:
                    break
                print("\nUser2: " + server['lastMessage'].decode('UTF-8'))
            else: # user2
                while server['userTurn'] == b'1\n': # user2 waits for their turn
                    if server['user1'] == b'unlogged\n':
                        break_out_flag = True
                        break
                    time.sleep(TIME_WAITING)
                if break_out_flag:
                    break
                print("\nUser1: " + server['lastMessage'].decode('UTF-8'))

    # Code below is executed only when the second user logs off
    conversationHistory.clear()
    if not user: # user1
        print("User2 logged off. Wait until new user2 logs on.")
        while (server['user2'] == b'unlogged\n'):
            time.sleep(TIME_WAITING)
        print("User2 logged on. Start a new conversation.")
    else: # user2
        print("User1 logged off. Wait until they log on.")
        while (server['user1'] == b'unlogged\n'):
            time.sleep(TIME_WAITING)
        print("User1 logged on. Wait until they start a new conversation.")
