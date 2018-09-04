# coding: utf-8
import os


# for NodeMCU32
ON_BOARD_LED_PIN_NO = 2
ON_BOARD_LED_HIGH_IS_ON = (os.uname().sysname == 'esp32')

# for Lolin32
# ON_BOARD_LED_HIGH_IS_ON = False
# ON_BOARD_LED_PIN_NO = 5

# for Lolin32 Lite
# ON_BOARD_LED_PIN_NO = 22


gpio_pins = (0, 1, 2, 3, 4, 5, 12, 13, 14, 15, 16)
