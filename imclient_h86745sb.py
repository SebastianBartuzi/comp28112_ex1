import im
import time
import atexit
server = im.IMServerProxy('https://web.cs.manchester.ac.uk/h86745sb/COMP28112_ex1/IMserver.php')

if server['user1'] == b'logged\n' and server['user2'] == b'logged\n':
    print("Two users are logged in. Wait until one of them logs off.")
    while (server['user1'] == b'logged\n' and server['user2'] == b'logged\n'):
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

# while True:
#     if responding:
#         myMessage = input("Type your message: ")
#         server['message'] = myMessage
#         responding = false
#         waiting = true
#     if waiting:
#         while ()
