#!/usr/bin/python

import math, time
from rgb import *
from ledstrip import *

# Chase

class Chase():
  
  position = -1
  increment = 1

  def start(self, ledStrip):
    x = 1
  
  def update(self, ledStrip):
    self.position = self.position + self.increment
    if self.position == ledStrip.stripLength:
      self.position = ledStrip.stripLength -2
      self.increment = -1
    if self.position == -1:
      self.position = 1
      self.increment = 1

    colours = list()
    for i in range(ledStrip.stripLength):
      if i == self.position:
        colours.append(RED)
      else:
        colours.append(BLACK)
    ledStrip.push_colours(colours)
    return 0

  def is_active(self):
    t = time.localtime()
    return t.tm_hour >= 8 and t.tm_hour <= 19 and t.tm_min % 12 == 4 

