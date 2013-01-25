#!/usr/bin/python

import RPi.GPIO as GPIO
import time
from rgb import *

class LedStrip():

  device = None
  stripLength = 0 
  colours = None
  spidev = None

  def __init__(self, stripLength, device = "/dev/spidev0.0"):
    self.stripLength = stripLength
    self.device = device
    self.spidev = file(device, "wb")

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
    self.push_to_spi(raster)
    self.colours = colours

  def push_to_spi(self, raster):
    #for b in raster:
    #  print b
    self.spidev.write(raster)
    self.spidev.flush()

  def convert_colours_to_bytes(self, colours, stripLength):
    column = bytearray(stripLength * 3 + 1)
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
 
