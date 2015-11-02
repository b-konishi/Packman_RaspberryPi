#!/usr/bin/env python
import RPi.GPIO as GPIO
import time

f = open('sample.txt', 'w')
f.write("1121,2232,3433")
f.close()
