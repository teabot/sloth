#!/usr/bin/python

import math, time
from rgb import *
from ledstrip import *

# Squishy/slidy HSV colour wheel

class Lunch():

  hueOffset = 0.0
  hueOffsetIncrement = 0.02
  hueIncrement = None
 
  def start(self, ledStrip):
    self.hueIncrement = 1.0 / ledStrip.stripLength
  
  def update(self, ledStrip):
    colours = list()
    for i in range(ledStrip.stripLength):
      hue = (self.hueOffset + (self.hueIncrement * i)) % 1.0
      colours.append(newHsvColour(hue))
    ledStrip.push_colours(colours)
    self.hueOffset += self.hueOffsetIncrement
    if self.hueOffset > 1.0:
      self.hueOffset = 0.0
    return 0.01 

  def is_active(self):
    t = time.localtime()
    return t.tm_hour == 13 and t.tm_min == 0


TWO_PI = math.pi * 2

