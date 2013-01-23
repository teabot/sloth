#!/usr/bin/python

from jenkins import *
from ledstrip import *

def main():
  jenkins = JenkinsBuildStatus()
  jenkins.start()
  while True:
    delay = jenkins.update(ledStrip)
    time.sleep(delay)

ledStrip = LedStrip(5)

main()
