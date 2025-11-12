from pynput import keyboard

exit = False

def on_press(key):
    global exit
    try:
        if key.char == 'q':
            print("Q pressed!")
    except AttributeError:
        if key == keyboard.Key.f12:
            print("F12 pressed! Exiting.")
            exit = True

def start_listener():
    """Start the listener in a non-blocking way"""
    listener = keyboard.Listener(on_press=on_press)
    listener.start()
    return listener
