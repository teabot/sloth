#!/usr/bin/python

import colorsys

class RgbColour():

  red   = 0
  green = 0
  blue  = 0

  def __init__(self, red, green, blue, intensity=1.0):
    self.red   = int(red * intensity)
    self.green = int(green * intensity)
    self.blue  = int(blue * intensity)
    #print intensity, self.red, self.green, self.blue

  def asHex(self, intensity = 1.0):
    return hex(int(self.red * intensity))[2:].rjust(2, '0') +\
      hex(int(self.green * intensity))[2:].rjust(2, '0') +\
      hex(int(self.blue * intensity))[2:].rjust(2, '0') 
 
  def __str__(self):
    return self.asHex();

  def __repr__(self):
    return self.__str__()

  def atIntensity(self, intensity):
    return RgbColour(self.red, self.green, self.blue, intensity)

def newHexColour(hexValue):
  return RgbColour(int('0x' + hexValue[0:2], 16),\
    int('0x' + hexValue[2:4], 16),\
    int('0x' + hexValue[4:6], 16))

def newHsvColour(hue, saturation=1.0, value=1.0):
  rgb = colorsys.hsv_to_rgb(hue, saturation, value)
  return RgbColour(rgb[0], rgb[1], rgb[2])

RED    = newHexColour('ff0000')
BLUE   = newHexColour('0000ff')
GREEN  = newHexColour('00ff00')
YELLOW = newHexColour('ffff00')
BLACK  = newHexColour('000000')
WHITE  = newHexColour('ffffff')

