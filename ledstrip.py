#!/usr/bin/python

#import RPi.GPIO as GPIO
from rgb import *

class LedStrip():

  device = None
  stripLength = 0 
  #spidev = None

  def __init__(self, stripLength, device = "/dev/spidev0.0"):
    self.stripLength = stripLength
    self.device = device
    #self.spidev = file(device, "wb")

  def push_colours(self, colours):
    raster = self.convert_colours_to_bytes(colours, self.stripLength)
    self.push_to_spi(raster)

  def push_to_spi(self, raster):
    for b in raster:
      print b
  #  spidev.write(raster)
  #  spidev.flush()

  def convert_colours_to_bytes(self, colours, stripLength):
    column = bytearray(stripLength * 3 + 1)
    index = 0
    colourIndex = 0 
    for colour in colours:
      column[index]     = colour.green
      column[index + 1] = colour.red
      column[index + 2] = colour.blue
      index += 3
      colourIndex += 1
      if colourIndex >= stripLength:
        break 
    return column
 
