import im
import time
import atexit
server = im.IMServerProxy('https://web.cs.manchester.ac.uk/h86745sb/COMP28112_ex1/IMserver.php')

if server['user1'] == 'logged' and server['user2'] == 'logged':
    print("Two users are logged in. Wait until one of them logs off")
    while (server['user1'] == 'logged' and server['user2'] == 'logged'):
        time.sleep(0.5)

if server['user1'] == 'unlogged': # user1 is not logged in. Log in as user1
    server['user1'] = 'logged'
else: # user2 is not logged in. Log in as user2
    server['user2'] = 'logged'

# while True:
#     if responding:
#         myMessage = input("Type your message: ")
#         server['message'] = myMessage
#         responding = false
#         waiting = true
#     if waiting:
#         while ()
