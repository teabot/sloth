#!/usr/bin/python

import math

class Pulser():

  increment = 0.1
  position  = 0
  
  def __init__(self, increment=0.1):
    self.increment = increment

  def __str__(self):
    return self.position

  def __repr__(self):
    return self.__str__()

  def get_update(self):
    value = (math.sin(self.position) + 1.0) / 2.0 
    self.position += self.increment
    if self.position > TWO_PI:
      self.position = 0.0
    return value
   
TWO_PI = math.pi * 2

