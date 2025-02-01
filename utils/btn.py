#!/usr/bin/env python3

import gpiod
import gpiodevice
from gpiod.line import Bias, Direction, Edge
import asyncio

def handle_buttons(callback):
    # GPIO pins for each button (from top to bottom)
    # These will vary depending on platform and the ones
    # below should be correct for Raspberry Pi 5.
    # Run "gpioinfo" to find out what yours might be.
    #
    # Raspberry Pi 5 Header pins used by Inky Impression:
    #    PIN29, PIN31, PIN36, PIN18.
    # These header pins correspond to BCM GPIO numbers:
    #    GPIO05, GPIO06, GPIO16, GPIO24.
    # These GPIO numbers are what is used below and not the
    # header pin numbers.
    BUTTONS = [5, 6, 16, 24]

    # These correspond to buttons A, B, C and D respectively
    LABELS = ["A", "B", "C", "D"]

    # Create settings for all the input pins, we want them to be inputs
    # with a pull-up and a falling edge detection.
    INPUT = gpiod.LineSettings(direction=Direction.INPUT, bias=Bias.PULL_UP, edge_detection=Edge.FALLING)

    # Find the gpiochip device we need, we'll use
    # gpiodevice for this, since it knows the right device
    # for its supported platforms.
    chip = gpiodevice.find_chip_by_platform()

    # Build our config for each pin/line we want to use
    OFFSETS = [chip.line_offset_from_id(id) for id in BUTTONS]
    line_config = dict.fromkeys(OFFSETS, INPUT)

    # Request the lines, *whew*
    request = chip.request_lines(consumer="inky7-buttons", config=line_config)

    while True:
        for event in request.read_edge_events():
            index = OFFSETS.index(event.line_offset)
            gpio_number = BUTTONS[index]
            label = LABELS[index]
            callback(event, (index, gpio_number, label))
