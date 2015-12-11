#!/usr/bin/python

import math, time
from rgb import *
from ledstrip import *
from random import randint

# Snow

class Snow():

  def start(self, ledStrip):
    x = 1
  
  def update(self, ledStrip):
    colours = list()
    for i in range(ledStrip.stripLength):
      if randint(0,1) == 1:
        intensity = randint(0,10) / 10.0
        colours.append(WHITE.atIntensity(intensity))
      else:
        colours.append(BLACK)
    ledStrip.push_colours(colours)
    return 0.5 

  def is_active(self):
    t = time.localtime()
    return t.tm_hour >= 8 and t.tm_hour <= 19 and t.tm_min % 12 == 0

