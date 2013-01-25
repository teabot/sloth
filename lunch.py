#!/usr/bin/python

from rgb import *
from ledstrip import *

class Lunch():

  hueOffset = 0.0
  hueOffsetIncrement = 0.02
  hueIncrement = None
 
  def start(self, ledStrip):
    self.hueIncrement = 1.0 / ledStrip.stripLength
  
  def update(self, ledStrip):
    colours = list()
    for i in range(ledStrip.stripLength):
      hue = self.hueOffset + (self.hueIncrement * i) 
      colours.append(newHsvColour(hue))
    ledStrip.push_colours(colours)
    return 1.0

