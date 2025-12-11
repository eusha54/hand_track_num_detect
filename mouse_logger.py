from pynput import mouse

def on_move(x,y):
    print(f'Pointer moved to {(x,y)}')

def on_click(x, y, button, pressed):
    if pressed:
        print(f"{button} clicked at {(x,y)}")

def on_scroll(x,y,dx,dy):
    print(f'Scrolled {"down" if dy<0 else "up"} at {(x,y)}')


with mouse.Listener(
    on_move=on_move,
    on_click=on_click,
    on_scroll=on_scroll
) as listener:
    listener.join()
    