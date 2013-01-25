#!/usr/bin/python

import sys, signal
from jenkins import *
from ledstrip import *

def signal_handler(signal, frame):
  shutdown()

def shutdown():
  ledStrip.switch_off()
  sys.exit(0)

def main():
  signal.signal(signal.SIGTERM, signal_handler)

  jenkins = JenkinsBuildStatus("http://hudson2.datadev.last.fm:8080/")
  jenkins.start()
  try:
    while True:
      delay = jenkins.update(ledStrip)
      time.sleep(delay)
  except KeyboardInterrupt:
    shutdown()

ledStrip = LedStrip(32, "/dev/spidev0.0")

main()
