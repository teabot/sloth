#!/usr/bin/python

from lxml import  etree
import time, re, threading
from rgb import *
from pulser import *
from ledstrip import *

class JenkinsJobFetcher(threading.Thread):
  
  parser = etree.HTMLParser()
  buildState = list()
  progressState = list()
  lock = threading.Lock()
  fetchUrl = None
  
  def __init__(self, fetchUrl):
    threading.Thread.__init__(self)
    self.fetchUrl = fetchUrl

  def run(self):
    while True:
      try:
        cBuildState = list()
        cProgressState = list()
        tree = etree.parse(self.fetchUrl, self.parser)
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
    return GREEN if image.startswith('blue') else\
           BLUE if image.startswith('grey') else\
           YELLOW if image.startswith('yellow') else\
           RED if image.startswith('red') else\
           BLACK  

  def progress_status_from_image(self, image):
    return True if image.find('anime') >= 0 else\
           False

class JenkinsBuildStatus():
 
  fetcher = None
  fetchUrl = None
  pulser = Pulser()
  
  def __init__(self, fetchUrl):
    self.fetchUrl = fetchUrl

  def start(self, ledStrip):
    self.fetcher = JenkinsJobFetcher(self.fetchUrl)
    self.fetcher.setDaemon(True)
    self.fetcher.start()
  
  def update(self, ledStrip):
    colours = self.prepare_colours(self.fetcher.buildState, self.fetcher.progressState)
    ledStrip.push_colours(colours)
    return 0.015 

  def prepare_colours(self, currentColours, pulseStates):
    intensity = self.pulser.get_update()
    colours = list()
    for i in range(len(currentColours)):
      sourceColour = currentColours[i]
      isPulsing = pulseStates[i]
      if isPulsing:
        colours.append(sourceColour.atIntensity(intensity))
      else:
        colours.append(sourceColour.atIntensity(0.7))
    return colours

