#!/usr/bin/python

import signal, time, re, threading
from rgb import *
from jenkins import *
from pulser import *
from ledstrip import *

def prepare_colours(currentColours, pulseStates):
  intensity = pulser.get_update()
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
  t = JenkinsJobFetcher("http://hudson2.datadev.last.fm:8080/")
  t.setDaemon(True)
  t.start()
  while True:
    colours = prepare_colours(t.buildState, t.progressState)    
    ledStrip.push_colours(colours)
    print "DONE"
    time.sleep(0.5)

ledStrip = LedStrip(5)
pulser = Pulser()

main()
