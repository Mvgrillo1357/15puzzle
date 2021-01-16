from Board import Board
from pynput import keyboard
from time import sleep
b= Board()
def main():
    b.shuffle()
    b.refresh()
    
    with keyboard.Listener(
            on_press=on_press,
            on_release=on_release) as listener:
        listener.join()


def on_press(key):
    b.refresh()

def on_release(key):
    if key == keyboard.Key.esc:
        # Stop listener
        return False
    
    elif key== keyboard.Key.up:
        b.board, b.empty_loc= b.move_up(b.board, b.empty_loc)
    elif key== keyboard.Key.right:
        b.board, b.empty_loc= b.move_right(b.board, b.empty_loc)
    elif key== keyboard.Key.down:
        b.board, b.empty_loc= b.move_down(b.board, b.empty_loc)
    elif key== keyboard.Key.left:
        b.board, b.empty_loc= b.move_left(b.board, b.empty_loc)
    elif key== keyboard.Key.shift:
        print("........")
        moves= b.solve()
        for m in moves:
            b.moves[m](b.board, b.empty_loc)
            b.refresh()
            sleep(1)

    return b.refresh()

if __name__ == "__main__":
    main()
