#!/usr/bin/python

import math, time
from rgb import *
from ledstrip import *
from pulser import *

# Bar graph of time days in Dec passed and days remaining until Xmas (25th Dec)

class XmasCountdown():

  pulser = Pulser()
  day_increment = None

  def start(self, ledStrip):
    self.day_increment = ledStrip.stripLength / 25.0
  
  def update(self, ledStrip):
    date = time.localtime()
    intensity = self.pulser.get_update()
    colours = list()
    for i in range(ledStrip.stripLength):
      if date.tm_mon != 12 or (i < (date.tm_mday * self.day_increment)):
        colours.append(BLUE.atIntensity(intensity))
      else:
        colours.append(YELLOW.atIntensity(intensity))
    ledStrip.push_colours(colours)
    return 0.02 

  def is_active(self):
    t = time.localtime()
    return t.tm_hour >= 8 and t.tm_hour <= 19 and t.tm_min % 12 == 2 

