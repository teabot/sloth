#!/usr/bin/python

from rgb import *

def convert_colours_to_bytes(colours, stripLength):
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
 
