# coding: utf-8


def wait_for_wifi():
    import network

    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        print('connecting to network...')
        sta_if.active(True)
        while not sta_if.isconnected():
            pass
    print('Network configuration:', sta_if.ifconfig())

wait_for_wifi()

import led
led.blink_on_board_led(times = 2)

import node
node.main()
