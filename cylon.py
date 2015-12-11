#!/usr/bin/python

import math, time
from rgb import *
from ledstrip import *

# Cylon

class Cylon():

  stops = 15
  size = 20
  max_position = 0
  position = 0
  direction = 1

  def start(self, ledStrip):
    self.max_position = self.stops + self.size

  def update(self, ledStrip):
    colours = list()

    for i in range(0, self.max_position):
      colours.append(BLACK)

    current_position = self.position
    for i in range(1, self.stops):
      x = (float(i) / self.stops) * 255
      colours[current_position] = RgbColour(x, 0, x);
      if current_position < self.max_position - 1:
        current_position += 1

    colours = colours[self.stops:self.max_position]

    if self.direction < 0:
      colours = list(reversed(colours))
      
    colours_to_push = list()
    
    while len(colours_to_push) < ledStrip.stripLength:
      colours_to_push.extend(colours)

    ledStrip.push_colours(colours_to_push)

    if self.position < self.max_position - 1:
      self.position += 1
    else:
      self.direction = self.direction * -1
      self.position = 0

    return 0.015

  def is_active(self):
    t = time.localtime()
    return t.tm_hour >= 8 and t.tm_hour <= 19 and t.tm_min % 12 == 9
