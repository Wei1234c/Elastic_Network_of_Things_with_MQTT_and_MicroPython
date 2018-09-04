# coding: utf-8


def wait_for_wifi():
    import network

    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        print('connecting to network...')
        sta_if.active(True)        
        # sta_if.connect(SSID, PASSWORD)
        sta_if.connect('Wei RN4', '51557010')        
        while not sta_if.isconnected():
            pass
    print('Network configuration:', sta_if.ifconfig())

wait_for_wifi()

import led
led.blink_on_board_led(times = 2)

import node
node.main()
