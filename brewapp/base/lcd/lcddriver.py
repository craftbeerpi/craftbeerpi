import i2c_lib
from time import sleep

# LCD Address
#ADDRESS = 0x3F
ADDRESS = 0x27

# I2C bus
BUS = 1

# commands
LCD_CLEARDISPLAY = 0x01
LCD_RETURNHOME = 0x02
LCD_ENTRYMODESET = 0x04
LCD_DISPLAYCONTROL = 0x08
LCD_CURSORSHIFT = 0x10
LCD_FUNCTIONSET = 0x20
LCD_SETCGRAMADDR = 0x40
LCD_SETDDRAMADDR = 0x80

# flags for display entry mode
LCD_ENTRYRIGHT = 0x00
LCD_ENTRYLEFT = 0x02
LCD_ENTRYSHIFTINCREMENT = 0x01
LCD_ENTRYSHIFTDECREMENT = 0x00

# flags for display on/off control
LCD_DISPLAYON = 0x04
LCD_DISPLAYOFF = 0x00
LCD_CURSORON = 0x02
LCD_CURSOROFF = 0x00
LCD_BLINKON = 0x01
LCD_BLINKOFF = 0x00

# flags for display/cursor shift
LCD_DISPLAYMOVE = 0x08
LCD_CURSORMOVE = 0x00
LCD_MOVERIGHT = 0x04
LCD_MOVELEFT = 0x00

# flags for function set
LCD_8BITMODE = 0x10
LCD_4BITMODE = 0x00
LCD_2LINE = 0x08
LCD_1LINE = 0x00
LCD_5x10DOTS = 0x04
LCD_5x8DOTS = 0x00

# flags for backlight control
LCD_BACKLIGHT = 0x08
LCD_NOBACKLIGHT = 0x00

En = 0b00000100 # Enable bit
Rw = 0b00000010 # Read/Write bit
Rs = 0b00000001 # Register select bit

class lcd:
  """ 
  Class to control the 16x2 I2C LCD display from sainsmart from the Raspberry Pi
  """

  def __init__(self):
    """Setup the display, turn on backlight and text display + ...?"""
    self.device = i2c_lib.i2c_device(ADDRESS, BUS)

    self.write(0x03)
    self.write(0x03)
    self.write(0x03)
    self.write(0x02)

    self.write(LCD_FUNCTIONSET | LCD_2LINE | LCD_5x8DOTS | LCD_4BITMODE)
    self.write(LCD_DISPLAYCONTROL | LCD_DISPLAYON)
    self.write(LCD_CLEARDISPLAY)
    self.write(LCD_ENTRYMODESET | LCD_ENTRYLEFT)
    sleep(0.2)

  def strobe(self, data):
    """clocks EN to latch command"""
    self.device.write_cmd(data | En | LCD_BACKLIGHT)
    sleep(0.0005)
    self.device.write_cmd(((data & ~En) | LCD_BACKLIGHT))
    sleep(0.001)

  def write_four_bits(self, data):
    self.device.write_cmd(data | LCD_BACKLIGHT)
    self.strobe(data)

  def write(self, cmd, mode=0):
    """write a command to lcd"""
    self.write_four_bits(mode | (cmd & 0xF0))
    self.write_four_bits(mode | ((cmd << 4) & 0xF0))

  def display_string(self, string, line):
    if line == 1:
       self.write(0x80)
    if line == 2:
       self.write(0xC0)
    if line == 3:
       self.write(0x94)
    if line == 4:
       self.write(0xD4)

    for char in string:
       self.write(ord(char), Rs)

  def clear(self):
    """clear lcd and set to home"""
    self.write(LCD_CLEARDISPLAY)
    self.write(LCD_RETURNHOME)

  def backlight_off(self):
    """turn off backlight, anything that calls write turns it on again"""
    self.device.write_cmd(LCD_NOBACKLIGHT)

  def display_off(self):
    """turn off the text display"""
    self.write(LCD_DISPLAYCONTROL | LCD_DISPLAYOFF)

  def display_on(self):
    """turn on the text display"""
    self.write(LCD_DISPLAYCONTROL | LCD_DISPLAYON)
