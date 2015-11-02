#!/usr/bin/env python
import RPi.GPIO as GPIO
import time
import commands
import math

COLUMN = 1
ROW = 6
DEVIDE = 1
CONROL_LED = COLUMN*ROW / DEVIDE
FILL_DATA_SIZE = 6

FILE_NAME = 'sample.txt'

COLOR = [000,001,010,011,100,101,110,111]

# AVR   B3 B2 B1 B0 C7 C6 ... C1 C0 D7 D6 ... D1 D0 E1 E0
# GPIO  24 25 26 27  6  7 ... 12 13 14 15 ... 22 23  4  5
# NUM   18 19 20 21  2  3 ...  8  9 10 11 ... 16 17  0  1
pin = [4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,22,23,24,25,26,27]

GPIO.setmode(GPIO.BCM)
for i in range(0, len(pin)):
  print(pin[i])
  GPIO.setup(pin[i], GPIO.OUT, pull_up_down=GPIO.PUD_OFF)
  GPIO.output(pin[i], False)

# pattern 0
# check(E1 E0)-row_address(C4-C0)-col_address(D4-D0)-color_data(B2-B0)
# check(E1 E0) - 0

# pattern 1
# check(E1 E0)-d1(C5-C3)-d2(C2-C0)-d3(D7-D5)-d4(D4-D2)-d5(D1D0B3)-d6(B2-B0)
# This is continued 100 times
# check(E1 E0) - 0
def write_data(pattern, col, row, *data):
  if pattern == 0:
    print('pin['+str(pin[0])+']: 0')
    print('pin['+str(pin[1])+']: 1')
    GPIO.output(pin[0], False)
    GPIO.output(pin[1], True)
    print('col: '+str(col))
    print('row: '+str(row))
    for i in range(0, 5):
      print('pin['+str(pin[5+i])+']: '+str((col >> 5-i-1)&1))
      print('pin['+str(pin[13+i])+']: '+str((row >> 5-i-1)&1))
      GPIO.output(pin[5+i], (col >> 5-i-1) & 1)
      GPIO.output(pin[13+i], (row >> 5-i-1) & 1)
    for i in range(0, 3):
      print('pin['+str(pin[19+i])+']: '+str((data[0]>>3-i-1)&1))
      GPIO.output(pin[19+i], (data[0] >> 3-i-1) & 1)
  elif pattern == 1:
    print('pin['+str(pin[0])+']: 1')
    print('pin['+str(pin[1])+']: 0')
    GPIO.output(pin[0], True)
    GPIO.output(pin[1], False)
    for i in range(0, 6):
      for j in range(0, 3):
        print('pin['+str(pin[4+j+(3*i)])+']: '+str((data[i]>>3-j-1)&1))
        GPIO.output(pin[4+j+(3*i)], (data[i] >> 3-j-1) & 1)
  elif pattern == 2:
    print('pin['+str(pin[0])+']: 1')
    print('pin['+str(pin[1])+']: 1')
    GPIO.output(pin[0], True)
    GPIO.output(pin[1], True)
    for i in range(2, len(pin)):
      GPIO.output(pin[i], False)


count = 0
i = 0
toggle = 1
try:
  while True:
    i+=1
    f = open(FILE_NAME,'r')
    line = f.readline()
    #if i%1000 == 0:
    #  print("Get" + str(i))
    if '' == line:
      print('empty')
      continue
    data = line.replace(',', '')
    data = data.strip()
    option = data[0]
    data = data[1:]

    if count == 0:
      data_tmp = ''
      data_list = []
      for i in range(0, len(data)):
        data_tmp = data_tmp + '0'
      count = 1;
    
    if data == data_tmp:
      continue;
    
    if int(option):
      for i in range(0, len(data)):
        if data[i] != data_tmp[i]:
          print(data[i])
          #command = commands.getoutput('sleepenh 5')
          #print(command)
          write_data(0, int(i/ROW)+1, i%ROW+1,int(data[i]))
      write_data(2, 0, 0)
      data_tmp = data

    else:
      print('option = 0')
      for i in range(0, ((COLUMN*ROW-1)/FILL_DATA_SIZE)+1):
        print('pin[2]: '+str(toggle))
        GPIO.output(pin[2], toggle)
        if toggle == 1:
          toggle = 0
        else:
          toggle = 1
        print(toggle)
        for j in range(0, FILL_DATA_SIZE):
          if j+(6*i) < len(data):
            data_list.append(data[j+(6*i)])
          else:
            data_list.append('0')
        print(data_list)
        write_data(1, 0, 0, *map(int, data_list))
        #command = commands.getoutput('sleepenh 1')
        #print(command)
        data_list = []
      write_data(2,0,0)
      data_tmp = data
except KeyboardInterrupt:
  f.closed
  GPIO.cleanup()
  print('Interrupt')

