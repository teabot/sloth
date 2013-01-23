#!/usr/bin/python

import signal, time, re, threading
#import RPi.GPIO as GPIO
from rgb import *
from jenkins import *
from pulser import *
from ledstrip import *

#def push_to_spi(raster):
#  spidev.write(raster)
#  spidev.flush()

def prepare_colours(currentColours, pulseStates):
  intensity = pulser.getUpdate()
  colours = list()
  for i in range(len(currentColours)):
    sourceColour = currentColours[i]
    isPulsing = pulseStates[i]
    if isPulsing:
      colours.append(sourceColour.atIntensity(intensity))
    else:
      colours.append(sourceColour)
  return colours

def main():
  t = JenkinsJobFetcher()
  t.setDaemon(True)
  t.start()
  while True:
    colours = prepare_colours(t.buildState, t.progressState)    
    raster = convert_colours_to_bytes(colours, stripLength)
    #print raster
    for b in raster:
      print b
    #push_to_spi(raster)
    print "DONE"
    time.sleep(0.5)

device = "/dev/spidev0.0"
stripLength = 5
#spidev = file(device, "wb")
pulser = Pulser()

main()
