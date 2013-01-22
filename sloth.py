#!/usr/bin/python

from lxml import  etree
import signal, time, re, threading

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
        print self.buildState
        print self.progressState
      except Exception:
        pass
      time.sleep(5)

  def build_status_from_image(sel, image):
    return 'S' if image.startswith('blue') else\
           'D' if image.startswith('grey') else\
           'U' if image.startswith('yellow') else\
           'F' if image.startswith('red') else\
           'X'  

  def progress_status_from_image(sel, image):
    return True if image.find('anime') >= 0 else\
           False

def main():
  t = JenkinsJobFetcher()
  t.setDaemon(True)
  t.start()
  while True:
    time.sleep(0.1)

main()
