#!/usr/bin/python

from lxml import  etree
import signal, time, re, threading
import RPi.GPIO as GPIO

class RgbColour():
  r = 0
  g = 0
  b = 0

  def __init__(self, hexValue):
    self.r = int('0x' + hexValue[0:2], 16) 
    self.g = int('0x' + hexValue[2:4], 16) 
    self.b = int('0x' + hexValue[4:6], 16)

  def asHex(self, intensity = 1.0):
    return hex(int(self.r * intensity))[2:].rjust(2, '0') +\
      hex(int(self.g * intensity))[2:].rjust(2, '0') +\
      hex(int(self.b * intensity))[2:].rjust(2, '0') 
 
  def __str__(self):
    return self.asHex();

  def __repr__(self):
    return self.__str__()
 
  def red(self, intensity = 1.0):
    return int(self.r * intensity)

  def green(self, intensity = 1.0):
    return int(self.g * intensity)

  def blue(self, intensity = 1.0):
    return int(self.b * intensity)

class JenkinsJobFetcher(threading.Thread):
  
  parser = etree.HTMLParser()
  buildState = list()
  progressState = list()
  lock = threading.Lock()
  
  red    = RgbColour('ff0000')
  blue   = RgbColour('0000ff')
  green  = RgbColour('00ff00')
  yellow = RgbColour('ffff00')
  black  = RgbColour('000000')

  def __init__(self):
    threading.Thread.__init__(self)

  def run(self):
    while True:
      try:
        cBuildState = list()
        cProgressState = list()
        tree = etree.parse("http://hudson2.datadev.last.fm:8080/", self.parser)
        elems = tree.xpath(".//tr[starts-with(@id, 'job_')]/td/img[@class]")
        for img in elems:
          src = img.attrib.get("src")
          match = re.search(".*/(.+\.(png|gif))", src)
          imageName = match.groups()[0]
          cBuildState.append(self.build_status_from_image(imageName)) 
          cProgressState.append(self.progress_status_from_image(imageName)) 
        with self.lock:
          self.buildState = cBuildState
          self.progressState = cProgressState
      except Exception:
        pass
      time.sleep(5)

  def build_status_from_image(self, image):
    return self.green if image.startswith('blue') else\
           self.blue if image.startswith('grey') else\
           self.yellow if image.startswith('yellow') else\
           self.red if image.startswith('red') else\
           self.black  

  def progress_status_from_image(self, image):
    return True if image.find('anime') >= 0 else\
           False

def convert_colours_to_bytes(colours, stripLength):
  column = bytearray(stripLength * 3 + 1)
  index = 0
  colourIndex = 0 
  for colour in colours:
    column[index]     = colour.green()
    column[index + 1] = colour.red()
    column[index + 2] = colour.blue()
    index += 3
    colourIndex += 1
    if colourIndex >= stripLength:
      break 
  return column
 
def push_to_spi(raster):
  spidev.write(raster)
  spidev.flush()

def main():
  t = JenkinsJobFetcher()
  t.setDaemon(True)
  t.start()
  while True:
    raster = convert_colours_to_bytes(t.buildState, stripLength)
    push_to_spi(raster)
    time.sleep(1)

device = "/dev/spidev0.0"
stripLength = 32
spidev = file(device, "wb")

main()
