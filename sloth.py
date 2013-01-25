#!/usr/bin/python

import sys
from jenkins import *
from ledstrip import *

def main():
  jenkins = JenkinsBuildStatus("http://hudson2.datadev.last.fm:8080/")
  jenkins.start()
  try:
    while True:
      delay = jenkins.update(ledStrip)
      time.sleep(delay)
  except KeyboardInterrupt:
    ledStrip.switch_off()
    sys.exit(0) 

ledStrip = LedStrip(32, "/dev/spidev0.0")

main()
