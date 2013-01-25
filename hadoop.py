#!/usr/bin/python

from lxml import  etree
import time, re, threading
from rgb import *
from ledstrip import *

class HadoopLoadFetcher(threading.Thread):
  
  parser = etree.HTMLParser()
  nodes = list()
  lock = threading.Lock()
  fetchUrl = None
  
  def __init__(self, fetchUrl):
    threading.Thread.__init__(self)
    self.fetchUrl = fetchUrl

  def run(self):
    while True:
      try:
        tree = etree.parse(self.fetchUrl, self.parser)
        elems = tree.xpath(".//tr")
        cNodes = list()
        for tr in elems:
	  try:
	    tds         = tr.iterchildren('td')
	    url         = tds.next()
	    name        = int(re.match('.*?(?P<order>[0-9]+)', tds.next().text).groups()[0])
	    tasks       = int(tds.next().text)
	    maxMaps     = int(tds.next().text)
	    maxReducers = int(tds.next().text)
	    node = name, float(tasks) / (maxMaps + maxReducers)
	    cNodes.append(node)
	  except StopIteration:
	    pass
	cNodes.sort(key=lambda n: n[0])
        with self.lock:
          self.nodes = cNodes
      except Exception:
        pass
      time.sleep(5)

class HadoopLoad():
 
  fetcher = None
  fetchUrl = None
  
  def __init__(self, fetchUrl):
    self.fetchUrl = fetchUrl

  def start(self, ledStrip):
    self.fetcher = HadoopLoadFetcher(self.fetchUrl)
    self.fetcher.setDaemon(True)
    self.fetcher.start()
  
  def update(self, ledStrip):
    colours = self.prepare_colours(self.fetcher.nodes)
    ledStrip.push_colours(colours)
    return 0.015 

  def prepare_colours(self, nodes):
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

