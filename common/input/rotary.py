import board
from adafruit_seesaw import seesaw, rotaryio, digitalio

class RotaryEncoder():
    def __init__(self):
        self.i2c = board.I2C()  
        self.encoderSeesaw = seesaw.Seesaw(self.i2c, addr=0x49)
#        self.seesaw_product = (seesaw.get_version() >> 16) & 0xFFFF
#        print(f"Found product {seesaw_product}")
#        if seesaw_product != 5740:
#            print("Wrong firmware loaded?  Expected 5740")
        self.encoderSeesaw.pin_mode(1, self.encoderSeesaw.INPUT_PULLUP)
        self.encoderSeesaw.pin_mode(2, self.encoderSeesaw.INPUT_PULLUP)
        self.encoderSeesaw.pin_mode(3, self.encoderSeesaw.INPUT_PULLUP)
        self.encoderSeesaw.pin_mode(4, self.encoderSeesaw.INPUT_PULLUP)
        self.encoderSeesaw.pin_mode(5, self.encoderSeesaw.INPUT_PULLUP)
        
        self.select = digitalio.DigitalIO(self.encoderSeesaw, 1)
        self.select_held = False
        
        self.up = digitalio.DigitalIO(self.encoderSeesaw, 2)
        self.up_held = False
        self.down = digitalio.DigitalIO(self.encoderSeesaw, 4)
        self.down_held = False
        
        self.left = digitalio.DigitalIO(self.encoderSeesaw, 3)
        self.left_held = False
        self.right = digitalio.DigitalIO(self.encoderSeesaw, 5)
        self.right_held = False
        
        self.wheel = rotaryio.IncrementalEncoder(self.encoderSeesaw)
        self.last_position = self.wheel.position
        self.button_count = 5
        self.buttons = [self.select, self.up, self.left, self.down, self.right]
        self.button_names = ["Select", "Up", "Left", "Down", "Right"]
        self.button_states = [self.select_held, self.up_held, self.left_held, self.down_held, self.right_held]
    
    def getEncoderActivity(self):
#        print('a: ', self.wheel)
        self.position = self.wheel.position
       
        if self.position < self.last_position:
            self.last_position = self.position
            return {'Wheel': 'Up'}
        
        if self.position > self.last_position:
            self.last_position = self.position
            return {'Wheel': 'Down'}
        
        for b in range(self.button_count ):
            if not self.buttons[b].value and self.button_states[b] is False:
                self.button_states[b] = True
                return {self.button_names[b]:  'Press'}

            if self.buttons[b].value and self.button_states[b] is True:
                self.button_states[b] = False
                return {self.button_names[b]:  'Release'}
