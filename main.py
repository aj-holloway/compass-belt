import uasyncio
from machine import Pin
from time import sleep
from machine import I2C
from hmc5883l import HMC5883L

# Please check that correct PINs are set on hmc5883l library!
sensor = HMC5883L()

# Dictionary of directions. Change this if you want to use different GPIO pins
pins = {
    1: {"pin": Pin(8, Pin.OUT), "direction": "N"},
    2: {"pin": Pin(9, Pin.OUT), "direction": "NE"},
    3: {"pin": Pin(10, Pin.OUT), "direction": "E"},
    4: {"pin": Pin(11, Pin.OUT), "direction": "SE"},
    5: {"pin": Pin(12, Pin.OUT), "direction": "S"},
    6: {"pin": Pin(13, Pin.OUT), "direction": "SW"},
    7: {"pin": Pin(14, Pin.OUT), "direction": "W"},
    8: {"pin": Pin(15, Pin.OUT), "direction": "NW"}
}

# Push button for resetting our heading
zero_button = Pin(28, Pin.IN, Pin.PULL_UP)
# By default, no offset - use whatever the chip thinks is north
heading_offset = 0
last_pin_lit = 0

# Async function that turns a pin on for 3 seconds, then back off
async def pulse(pin):
    pin["pin"].on()
    await uasyncio.sleep(3)  # Pause 1s
    pin["pin"].off()

# Main loop
async def main():
    global heading_offset
    global last_pin_lit
    
    while True:

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
            pin_to_light = 1
            
        if(degrees >= 23 and degrees < 68):
            pin_to_light = 2
            
        if(degrees >= 68 and degrees < 113):
            pin_to_light = 3
            
        if(degrees >= 113 and degrees < 158):
            pin_to_light = 4
            
        if(degrees >= 158 and degrees < 203):
            pin_to_light = 5

        if(degrees >= 203 and degrees < 248):
            pin_to_light = 6

        if(degrees >= 248 and degrees < 293):
            pin_to_light = 7
        
        if(degrees >= 293 and degrees < 338):
            pin_to_light = 8
        
        # Check to make sure we aren't lighting up the same pin that was previously lit.
        # If you're stationary, you don't want one of the motors just buzzing away.
        if(pin_to_light != last_pin_lit):
            # Update the last pin lit to the new one we're lighting up
            last_pin_lit = pin_to_light
            
            # Light it up!
            pin = pins[pin_to_light]
            uasyncio.create_task(pulse(pin))
            
        await uasyncio.sleep(.1)
        # Just for debugging if you're having issues
        print("degrees: " + str(degrees))

uasyncio.run(main())
