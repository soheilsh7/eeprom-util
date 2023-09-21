#   EEPROM
#How To Use :
#   Read :
#        python3 eeprom.py r <Address>

#   Write :
#        python3 sram.py w <Address> <Value> 
#Usage example :
#   python3 eeprom.py w 11111111111 00110111
#   python3 eeprom.py r 11111111111

import RPi.GPIO as GPIO
import time
import threading
import sys

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False) 
clk = 21
r_clk = 16
clk_freq = 0
address_set_pin = 20
write_enable = 25
output_enable = 12
io_pin_array = [19, 13, 6, 5, 22, 27, 17, 4]


GPIO.cleanup()
GPIO.setup(clk, GPIO.OUT)
GPIO.setup(r_clk, GPIO.OUT)
GPIO.setup(address_set_pin, GPIO.OUT)
GPIO.setup(write_enable, GPIO.OUT)
GPIO.setup(output_enable, GPIO.OUT)
GPIO.output(write_enable, GPIO.HIGH)
GPIO.output(output_enable, GPIO.HIGH)

try :
    mode = sys.argv[1] 

except :
    mode = (input("mode : "))

if mode == 'w' :

    try :
        address = sys.argv[2] 

    except :
        address = (input("address : "))

    try :
        data = sys.argv[3] 

    except :
        data = (input("data : "))

elif mode == 'r' :

    try :
        address = sys.argv[2] 

    except :
        address = (input("address : "))



def setAddress(inp, clk_pin, r_clk_pin, clk_freq, data_pin) :
    GPIO.output(r_clk_pin, GPIO.LOW)
    GPIO.output(clk_pin, GPIO.LOW)
    GPIO.output(data_pin, GPIO.LOW)
    i = 0
    time.sleep(clk_freq)
    for bit in inp :
        GPIO.output(clk_pin, GPIO.LOW)
        GPIO.output(data_pin, int(bit))
        time.sleep(clk_freq)
        GPIO.output(clk_pin, GPIO.HIGH) 
        time.sleep(clk_freq)
        GPIO.output(clk_pin, GPIO.LOW)
        #print(str(i) + "'th bit Written : " + bit)
        i+=1
    #print("set address " + inp)
    GPIO.output(r_clk_pin, GPIO.HIGH)


def set_io_out(io_array) :
    for pin in io_array :
        GPIO.setup(pin, GPIO.OUT)


def set_io_in(io_array) :
    for pin in io_array :
        GPIO.setup(pin, GPIO.IN)

def write(address, clk, r_clk, clk_freq, address_set_pin, write_enable_pin, output_enable_pin, io_pin_array):
    GPIO.output(output_enable_pin, GPIO.HIGH)
    setAddress(address, clk, r_clk, clk_freq, address_set_pin)
    set_io_out(io_pin_array)
    for (pin, bit) in zip(io_pin_array, data) :
        GPIO.output(pin, int(bit))
        #print (str(pin) + " >> " + bit)

    GPIO.output(write_enable_pin, GPIO.LOW)
    print (data + " Writed to addtess " + address)
    GPIO.output(write_enable_pin, GPIO.HIGH)


def read(address, clk, r_clk, clk_freq, address_set_pin, write_enable_pin, output_enable_pin, io_pin_array):
    GPIO.output(write_enable_pin, GPIO.HIGH)
    setAddress(address, clk, r_clk, clk_freq, address_set_pin)
    set_io_in(io_pin_array)
    GPIO.output(output_enable_pin, GPIO.LOW)
    out = str()
    for pin in io_pin_array :
        out +=  str(GPIO.input(pin))
        #print (str(pin) + " >> " + str(GPIO.input(pin)))

    
    print ("Address " + address + " = " + out)

def read_byte(address, clk, r_clk, clk_freq, address_set_pin, write_enable_pin, output_enable_pin, io_pin_array):
    GPIO.output(write_enable_pin, GPIO.HIGH)
    setAddress(address, clk, r_clk, clk_freq, address_set_pin)
    set_io_in(io_pin_array)
    GPIO.output(output_enable_pin, GPIO.LOW)
    byte = 0
    for pin in io_pin_array :
        byte = (byte << 1) | GPIO.input(pin)
        
    return byte


def read_all():
    for base in range(0,8192,16):
        data = []
        for offset in range(0,16):
            adrs = (format(base+offset, '#013b'))
            #print(adrs)
            #print(base+offset)
            data.append(read_byte(adrs[2:] , clk, r_clk, clk_freq, address_set_pin, write_enable, output_enable, io_pin_array))
        print("{:#04X}:  {:#02X} {:#02X} {:#02X} {:#02X} {:#02X} {:#02X} {:#02X} {:#02X}     {:#02X} {:#02X} {:#02X} {:#02X} {:#02X} {:#02X} {:#02X} {:#02X}".format(base, data[0], data[1], data[2], data[3], data[4], data[5], data[6], data[7], data[8], data[9], data[10], data[11], data[12], data[13], data[14], data[15]) )







if mode == 'w' :
    write(address, clk, r_clk, clk_freq, address_set_pin, write_enable, output_enable, io_pin_array)

elif mode == 'r' :
    read(address, clk, r_clk, clk_freq, address_set_pin, write_enable, output_enable, io_pin_array)
    #read_byte(address, clk, r_clk, clk_freq, address_set_pin, write_enable, output_enable, io_pin_array)
elif mode == 'a' :
    read_all()



#read(address, clk, r_clk, clk_freq, address_set_pin, write_enable, output_enable, io_pin_array)
#read(address, clk, r_clk, clk_freq, address_set_pin, write_enable, output_enable, io_pin_array)

