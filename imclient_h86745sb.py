import im
import time
import atexit
server = im.IMServerProxy(
    'https://web.cs.manchester.ac.uk/h86745sb/COMP28112_ex1/IMserver.php')


# When one user closes terminal, log them off and delete lastMessage
def exit_handler():
    if logged:
        server['user%d' % user] = 'off'
        del server['lastMessage']
        del server['userTurn']
atexit.register(exit_handler)

TIME_WAITING = 0.5

logged = False
# Wait until someone logs off
if server['user1'] == b'on\n' and server['user2'] == b'on\n':
    print('Two users are logged on. Wait until one of them logs off.\n')
    while (server['user1'] == b'on\n' and server['user2'] == b'on\n'):
        time.sleep(TIME_WAITING)

if server['user1'] == b'off\n':  # user1 is not logged on. Log on as user1
    user = 1
    otherUser = 2
elif server['user2'] == b'off\n':  # user2 is not logged on. Log on as user2
    user = 2
    otherUser = 1
else:   # This point is reached only when 'waiting until someone logs off' loop
        # was somehow left. Exit the program
    print('Login error occured!')
    exit()

logged = True
server['user%d' % user] = 'on'
print('Logged on as user%d.' % user)
if (user == 1 and server['user2'] == b'off\n'):  # Wait for user2 to log on
    print('User2 is not logged on. Wait until they log on.')
    while (server['user2'] == b'off\n'):
        time.sleep(TIME_WAITING)

# Both users are logged on. Start conversation
while True:  # This loop is left only when killing program
    server['userTurn'] = '1'  # Always start with user1
    while True:  # This loop is left only when the second user logs off
        # Replying
        if (server['userTurn'] == b'%d\n' % user):  # The user is replying
            print('\n----------------\n')
            message = input('Type your message: ')
            print('\nYou sent: %s' % message)
            server['lastMessage'] = message
            server['userTurn'] = '%d' % otherUser  # It's the other user's turn
        # Waiting
        if (server['userTurn'] == b'%d\n' % otherUser):  # The user is waiting
            break_out_flag = False
            while server['userTurn'] == (b'%d\n' % otherUser):  # Waiting
                time.sleep(TIME_WAITING)
                # Check if the other user logged off
                if server['user%d' % otherUser] == b'off\n':
                    break_out_flag = True
                    break  # Leave inner loop
            if break_out_flag:
                break  # Leave outer loop
            else:
                print('\n----------------\n')
                print('User%d: %s' % (otherUser,
                      server['lastMessage'].decode('UTF-8').rstrip('\n')))

    # Code below is executed only when the other user logs off
    print('\n----------------\n')
    print('User%d has logged off. Wait until new user%d logs on.' %
          (otherUser, otherUser))
    print('\n----------------\n')
    while (server['user%d' % otherUser] == b'off\n'):
        time.sleep(TIME_WAITING)
    if user == 1:
        print('A new user2 has logged on. Start conversation.')
    else:  # user2
        print('A new user1 has logged on. Wait until they start conversation.')
