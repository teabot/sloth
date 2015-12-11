#!/usr/bin/python

import sys, signal, time
from bibliopixel.drivers.WS2801 import *
from bibliopixel.drivers.visualizer import DriverVisualizer
from jenkins import *
from ledstrip import *
from lunch import *
from snow import *
from xmas_countdown_bar import *
from chase import *
from pacman import *
from cylon import *

WS2801_DRIVER = 'WS2801'
VISUALIZER_DRIVER = 'Visualizer'
NUMBER_OF_LEDS = 160

def createWS2801Driver():
  return DriverWS2801(NUMBER_OF_LEDS, ChannelOrder.BGR, True, "/dev/spidev0.0", 1)

def createVisualizerDriver():
  return DriverVisualizer(num=NUMBER_OF_LEDS)

driver = None
if len(sys.argv) == 1:
  driver = createWS2801Driver()
elif len(sys.argv) == 2:
  if sys.argv[1] == WS2801_DRIVER:
    driver = createWS2801Driver()
  elif sys.argv[1] == VISUALIZER_DRIVER:
    driver = createVisualizerDriver()
  else:
    print 'Driver ', sys.argv[1], ' is not supported'
    sys.exit(-1)
else:
  print 'Usage: ', sys.argv[0], ' <driver>'
  print '<driver>:'
  print '  WS2801'
  print '  Visualizer'
  sys.exit(-1)

def signal_handler(signal, frame):
  shutdown()

def shutdown():
  ledStrip.switch_off()
  sys.exit(0)

def main():
  signal.signal(signal.SIGTERM, signal_handler)

  # Change this to point to your Jenkins host and view:
  jenkins = JenkinsBuildStatus("https://<jenkins.host>/jenkins/view/<view.to.visualise>/api/python")
  jenkins.start(ledStrip)
  pacman = Pacman()
  pacman.start(ledStrip)
  cylon = Cylon()
  cylon.start(ledStrip)
  snow = Snow()
  snow.start(ledStrip)
  xmas_countdown = XmasCountdown()
  xmas_countdown.start(ledStrip)
  chase = Chase()
  chase.start(ledStrip)
  lunch = Lunch()
  lunch.start(ledStrip)
  try:
    while True:
      if lunch.is_active():
        delay = lunch.update(ledStrip)
      elif cylon.is_active():
        delay = cylon.update(ledStrip)
      elif pacman.is_active():
        delay = pacman.update(ledStrip)
      elif snow.is_active():
        delay = snow.update(ledStrip)
      elif xmas_countdown.is_active():
        delay = xmas_countdown.update(ledStrip)
      elif chase.is_active():
        delay = chase.update(ledStrip)
      elif jenkins.is_active():
        delay = jenkins.update(ledStrip)
      else:
        ledStrip.switch_off()
        delay = 60
      time.sleep(delay)
  except KeyboardInterrupt:
    shutdown()

ledStrip = LedStrip(driver)

main()
