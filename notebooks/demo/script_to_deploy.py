print('_______ Testing remote deploy ______')
print('_______ Deployed from remote _______')

# noinspection PyPep8,PyUnresolvedReferences
import machine
# noinspection PyPep8
import time
            

def blink(pin, on_seconds = 0.5, off_seconds = 0.5, on = 0, off = 1):
    pin.value(on)
    time.sleep(on_seconds)
    pin.value(off)
    time.sleep(off_seconds)


def main():
    on_board_led = machine.Pin(2, machine.Pin.OUT)    
    while True:
        blink(on_board_led)

# main() will be invoked after this script is uploaded.
main()


