# eeprom-util
A simple utility for raspberry pi for reading and writing to an eeprom (Address through shift registers)

# How To Use :
##   Read :
```
python3 eeprom.py r <Address>
```
##   Write :
```
python3 sram.py w <Address> <Value>
```

## Usage example :

### write value 00110111 to addrss 11111111111
```
python3 eeprom.py w 11111111111 00110111
```

### reading from address 11111111111
```
python3 eeprom.py r 11111111111
```
