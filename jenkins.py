#!/usr/bin/python

from lxml import  etree
import time, re, threading
from rgb import *

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

  def build_status_from_image(self, image):
    return GREEN if image.startswith('blue') else\
           BLUE if image.startswith('grey') else\
           YELLOW if image.startswith('yellow') else\
           RED if image.startswith('red') else\
           BLACK  

  def progress_status_from_image(self, image):
    return True if image.find('anime') >= 0 else\
           False

