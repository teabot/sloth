#!/usr/bin/python

import math, time
from rgb import *
from ledstrip import *

# Pacman

PACMAN  = newHexColour('ffee00')
INKY    = newHexColour('46bfee')
BLINKY  = newHexColour('d03e19')
PINKY   = newHexColour('ea82e5')
CLYDE   = newHexColour('db851c')
GHOST   = newHexColour('0000ff')
DOT     = newHexColour('ffffff')

GHOST_CHASE_1 = [ None,   None,   PACMAN, PACMAN, PACMAN, None, None, None, None, INKY,  INKY,  INKY,  None,  None, BLINKY, BLINKY, BLINKY, None,   None, PINKY, PINKY, PINKY, None,  None, CLYDE, CLYDE, CLYDE, None  ]
GHOST_CHASE_2 = [ PACMAN, PACMAN, PACMAN, PACMAN, PACMAN, None, None, None, None, None,  INKY,  INKY,  INKY,  None, None,   BLINKY, BLINKY, BLINKY, None, None,  PINKY, PINKY, PINKY, None, None,  CLYDE, CLYDE, CLYDE ]
PAC_CHASE_1 =   [ PACMAN, PACMAN, PACMAN, None,   None,   None, None, None, None, None,  GHOST, GHOST, GHOST, None, None,   GHOST,  GHOST,  GHOST,  None, None,  GHOST, GHOST, GHOST, None, None,  GHOST, GHOST, GHOST ]
PAC_CHASE_2 =   [ PACMAN, PACMAN, PACMAN, PACMAN, PACMAN, None, None, None, None, GHOST, GHOST, GHOST, None,  None, GHOST,  GHOST,  GHOST,  None,   None, GHOST, GHOST, GHOST, None,  None, GHOST, GHOST, GHOST, None  ]

GHOST_CHASE = [ GHOST_CHASE_1, GHOST_CHASE_2 ]
PAC_CHASE = [PAC_CHASE_1, PAC_CHASE_2 ]

DOT_SPACING = 3 
ANIM_UPDATE_RATE = 1
POSITION_UPDATE_RATE = 3 

class Pacman():

  chaseLength = len(GHOST_CHASE_1)
  chasePosition = chaseLength
  chasePhase = 0
  chaseIndex = 0
  chase = GHOST_CHASE
  positionCount = 0
  positionIncrement = 1
  frameCount = 0

  def start(self, ledStrip):
    x = 1

  def update(self, ledStrip):
    self.frameCount = self.frameCount + 1
    if self.frameCount > ANIM_UPDATE_RATE:
      self.frameCount = 0
      if self.chaseIndex == 1:
        self.chaseIndex = 0
      else:
        self.chaseIndex = 1
       
    self.positionCount = self.positionCount + 1 
    if self.positionCount > POSITION_UPDATE_RATE:
      self.positionCount = 0
      self.chasePosition = self.chasePosition + self.positionIncrement
      if self.chasePosition >= ledStrip.stripLength:
        self.positionIncrement = -1
        self.chasePosition = self.chasePosition - 2
        self.chase = PAC_CHASE
      if self.chasePosition < self.chaseLength:
        self.positionIncrement = 1
        self.chasePosition = self.chasePosition + 2
        self.chase = GHOST_CHASE
                  
    colours = list()
    self.drawDots(ledStrip, colours)
    self.drawChase(colours)
    ledStrip.push_colours(list(reversed(colours)))
    return 0.05

  def drawDots(self, ledStrip, colours):
    for i in range(ledStrip.stripLength):
      if i > self.chasePosition and i % DOT_SPACING == 0 and self.chase == GHOST_CHASE:
        colours.append(DOT)
      else:
        colours.append(BLACK)

  def drawChase(self, colours):
    for i in range(self.chaseLength):
      colour = self.chase[self.chaseIndex][i]
      if colour != None:
        colours[self.chasePosition - i] = colour

  def is_active(self):
    t = time.localtime()
    return t.tm_hour >= 8 and t.tm_hour <= 19 and (t.tm_min % 12 == 6 or t.tm_min % 12 == 7)

