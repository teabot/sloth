#!/usr/bin/python

import time
from rgb import *

class LedStrip():

  stripLength = 0 
  colours = None
  driver = None

  def __init__(self, driver):
    self.stripLength = driver.numLEDs
    self.driver = driver

  def switch_off(self):
    for i in range(256): 
      intensity = 1.0 - (i / 256.0)
      newColours = list()
      for colour in self.colours:
        newColours.append(colour.atIntensity(intensity))
      self.push_colours(newColours)
      time.sleep(0.02)

  def push_colours(self, colours):
    raster = self.convert_colours_to_bytes(colours, self.stripLength)
    self.push_to_driver(raster)
    self.colours = colours

  def push_to_driver(self, raster):
    self.driver.update(raster)

  def convert_colours_to_bytes(self, colours, stripLength):
    column = bytearray(stripLength * 3)
    index = 0
    colourIndex = 0 
    for colour in colours:
      column[index]     = colour.red
      column[index + 1] = colour.green
      column[index + 2] = colour.blue
      index += 3
      colourIndex += 1
      if colourIndex >= stripLength:
        break 
    return column

