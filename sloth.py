#!/usr/bin/python

from lxml import  etree
import signal, time, re, threading

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

  def build_status_from_image(sel, image):
    return RgbColour('00ff00') if image.startswith('blue') else\
           RgbColour('0000ff') if image.startswith('grey') else\
           RgbColour('ffff00') if image.startswith('yellow') else\
           RgbColour('ff0000') if image.startswith('red') else\
           RgbColour('000000')  

  def progress_status_from_image(sel, image):
    return True if image.find('anime') >= 0 else\
           False

  def get_colours(pulseValue):
    colours = list()
    #if !self.progressState[i]:
    #  pulseValue = 1.0
  
def cubicPulse(x, c=1.5, w=1.5, b = 0.25):
  x = abs(x - c);
  if x > w:
    return 0.0
  x = (x / w)
    return 1.0 - x * x * (3.0 - 2.0 * x)     

def main():
  t = JenkinsJobFetcher()
  t.setDaemon(True)
  t.start()
  while True:
    print t.buildState
    time.sleep(5)

main()
