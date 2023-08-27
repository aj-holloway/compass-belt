from machine import I2C
from hmc5883l import HMC5883L
from time import sleep
from machine import Pin

# Please check that correct PINs are set on hmc5883l library!
sensor = HMC5883L()

# GPIO pins for our different motors/LEDs
position_1 = Pin(8, Pin.OUT)
position_2 = Pin(9, Pin.OUT)
position_3 = Pin(10, Pin.OUT)
position_4 = Pin(11, Pin.OUT)
position_5 = Pin(12, Pin.OUT)
position_6 = Pin(13, Pin.OUT)
position_7 = Pin(14, Pin.OUT)
position_8 = Pin(15, Pin.OUT)

# Push button for resetting our heading
zero_button = Pin(28, Pin.IN, Pin.PULL_UP)
# By default, no offset - use whatever the chip thinks is north
heading_offset = 0

while True:
    # Adjust as needed
    sleep(.1)

    x, y, z = sensor.read()
    
    # Heading in degrees. Range: 0 - 359 
    degrees = sensor.get_degrees(x,y,z)
    
    # If the button is being pressed, get the current heading and save it as the offset
    if zero_button.value()==0:
        heading_offset = degrees

    # Add 360 to our current heading and subtract the offset, then mod by 360 to get
    # the corrected heading
    degrees = (360 + degrees - heading_offset) % 360
    
    # There's probably a better way of doing this, but check to see if the heading is
    # between two points on the compass and light up the corresponding pin. Remember that
    # N is at 0 degrees, therefore you want the pin to be lit up between 337.5 and 22.5 so
    # that 0 degrees is right in the middle. "degrees" will always be an integer, so I've
    # rounded up to 338 and 23.
    if(degrees >= 338 or degrees < 23):
        position_1.value(1)
        position_2.value(0)
        position_3.value(0)
        position_4.value(0)
        position_5.value(0)
        position_6.value(0)
        position_7.value(0)
        position_8.value(0)
        
    if(degrees >= 23 and degrees < 68):
        position_1.value(0)
        position_2.value(1)
        position_3.value(0)
        position_4.value(0)
        position_5.value(0)
        position_6.value(0)
        position_7.value(0)
        position_8.value(0)
        
    if(degrees >= 68 and degrees < 113):
        position_1.value(0)
        position_2.value(0)
        position_3.value(1)
        position_4.value(0)
        position_5.value(0)
        position_6.value(0)
        position_7.value(0)
        position_8.value(0)
        
    if(degrees >= 113 and degrees < 158):
        position_1.value(0)
        position_2.value(0)
        position_3.value(0)
        position_4.value(1)
        position_5.value(0)
        position_6.value(0)
        position_7.value(0)
        position_8.value(0)
        
    if(degrees >= 158 and degrees < 203):
        position_1.value(0)
        position_2.value(0)
        position_3.value(0)
        position_4.value(0)
        position_5.value(1)
        position_6.value(0)
        position_7.value(0)
        position_8.value(0)
    
    if(degrees >= 203 and degrees < 248):
        position_1.value(0)
        position_2.value(0)
        position_3.value(0)
        position_4.value(0)
        position_5.value(0)
        position_6.value(1)
        position_7.value(0)
        position_8.value(0)
    
    if(degrees >= 248 and degrees < 293):
        position_1.value(0)
        position_2.value(0)
        position_3.value(0)
        position_4.value(0)
        position_5.value(0)
        position_6.value(0)
        position_7.value(1)
        position_8.value(0)
    
    if(degrees >= 293 and degrees < 338):
        position_1.value(0)
        position_2.value(0)
        position_3.value(0)
        position_4.value(0)
        position_5.value(0)
        position_6.value(0)
        position_7.value(0)
        position_8.value(1)
    
    # Just for debugging if you're having issues
    print("degrees: " + str(degrees))