#!/usr/bin/python

from jenkins import *
from ledstrip import *

def main():
  jenkins = JenkinsBuildStatus("http://hudson2.datadev.last.fm:8080/")
  jenkins.start()
  while True:
    delay = jenkins.update(ledStrip)
    time.sleep(delay)

ledStrip = LedStrip(5, "/dev/spidev0.0")

main()
