import im
import time
import atexit
server = im.IMServerProxy('https://web.cs.manchester.ac.uk/h86745sb/COMP28112_ex1/IMserver.php')

# When one user closes terminal, log them off and delete lastMessage
def exit_handler():
    if logged:
        server['user%d' % user] = 'off'
        del server['lastMessage']
        del server['userTurn']
atexit.register(exit_handler)

TIME_WAITING = 0.5

logged = False
if server['user1'] == b'on\n' and server['user2'] == b'on\n':
    print('Two users are logged on. Wait until one of them logs off.\n')
    while (server['user1'] == b'on\n' and server['user2'] == b'on\n'): # Wait until someone logs off
        time.sleep(TIME_WAITING)

if server['user1'] == b'off\n': # user1 is not logged on. Log on as user1
    user = 1
    otherUser = 2
elif server['user2'] == b'off\n': # user1 is logged on. user2 is not logged on. Log on as user2
    user = 2
    otherUser = 1
else: # This point is reached only when 'waiting until someone logs off' loop somehow was left. Leave the program.
    print('Login error occured!')
    exit()
logged = True
server['user%d' % user] = 'on'
print('Logged on as user%d.\n' % user)
if (user == 1 and server['user2'] == b'off\n'): # Wait for user2 to log on
    print('User2 is not logged on. Wait until they log on.\n')
    while (server['user2'] == b'off\n'):
        time.sleep(TIME_WAITING)

# Both users are logged on. Start conversation
while True: # This loop is left only when killing program
    server['userTurn'] = '1' # Always start with user1
    while True: # This loop is left only when the second user logs off
        # Replying
        if (server['userTurn'] == b'%d\n' % user): # user is replying
            # Check if the other user logged off
            if server['user%d' % otherUser] == b'off\n':
                break
            print('----------------\n')
            message = input('Type your message: ')
            print('\nYou sent: %s\n' % message)
            # Check if the other user logged off
            if server['user%d' % otherUser] == b'off\n':
                break
            server['lastMessage'] = message
            server['userTurn'] = '%d' % otherUser # It is turn for user2 to read and reply
        # Waiting
        if (server['userTurn'] == b'%d\n' % otherUser): # user1 is waiting
            break_out_flag = False
            while server['userTurn'] == (b'%d\n' % otherUser): # user1 waits for their turn
                time.sleep(TIME_WAITING)
                # Check if the other user logged off
                if server['user%d' % otherUser] == b'off\n':
                    break_out_flag = True
                    break
            if break_out_flag:
                break
            print('----------------\n')
            print('User%d: %s' % (otherUser, server['lastMessage'].decode('UTF-8')))

    # Code below is executed only when the other user logs off
    print('\n----------------\n')
    print('User%d logged off. Wait until new user%d logs on.' % (otherUser, otherUser))
    while (server['user%d' % otherUser] == b'off\n'):
        time.sleep(TIME_WAITING)
    if user == 1:
        print('User2 logged on. Start a new conversation.')
    else: # user2
        print('User1 logged on. Wait until they start a new conversation.')
