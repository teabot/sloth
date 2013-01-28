#!/usr/bin/python

import sys, signal, time
from jenkins import *
from ledstrip import *
from lunch import *

def signal_handler(signal, frame):
  shutdown()

def shutdown():
  ledStrip.switch_off()
  sys.exit(0)

def main():
  signal.signal(signal.SIGTERM, signal_handler)

  jenkins = JenkinsBuildStatus("http://hudson2.datadev.last.fm:8080/")
  jenkins.start(ledStrip)
  lunch = Lunch()
  lunch.start(ledStrip)
  try:
    while True:
      if lunch.is_active():
        delay = lunch.update(ledStrip)
      elif jenkins.is_active():
        delay = jenkins.update(ledStrip)
      else:
        ledStrip.switch_off()
        delay = 60
      time.sleep(delay)
  except KeyboardInterrupt:
    shutdown()

ledStrip = LedStrip(32, "/dev/spidev0.0")

main()
