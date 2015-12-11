#!/usr/bin/python

import time, threading, ast, urllib
from rgb import *
from pulser import *
from ledstrip import *


class JenkinsJobFetcher(threading.Thread):
  
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
        tree = ast.literal_eval(urllib.urlopen(self.fetchUrl).read());
        for job in tree["jobs"]:
          jobColor = job["color"];
          buildStatus = self.build_status_from_job_color(jobColor)
          cBuildState.append(buildStatus) 
          cProgressState.append(self.progress_status_from_job_color(jobColor)) 
        with self.lock:
          self.buildState = cBuildState
          self.progressState = cProgressState
      except Exception:
        pass
      time.sleep(5)

  def build_status_from_job_color(self, jobColor):
    return GREEN if jobColor.startswith('blue') else\
           BLUE if jobColor.startswith('notbuilt') else\
           YELLOW if jobColor.startswith('yellow') else\
           RED if jobColor.startswith('red') else\
           BLACK  

  def progress_status_from_job_color(self, jobColor):
    return True if jobColor.find('anime') >= 0 else\
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

  def is_active(self):
    t = time.localtime()
    return t.tm_hour >= 8 and t.tm_hour <= 19

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

