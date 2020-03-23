import requests as rq
import sys
import os
import cchardet
from bs4 import BeautifulSoup as soup

TOKEN_FILE_PATH = "/data/token.txt"

#------------------------------

class JClusterInfoClass:
  def __init__(self, date, time, callsign, freq, qth, qth_name, comment):
    self.date     = date
    self.time     = time
    self.callsign = callsign
    self.freq     = freq
    self.qth      = qth
    self.qth_name = qth_name
    self.comment  = comment

  def getDateTime(self):
    return self.date + " " + self.time

#------------------------------

class JClusterClass:
  JCLUSTER_BAND_URL = "http://qrv.jp/html"

  def requestHistories(self):
    r = rq.get(self.getBandURL())
    r.encoding = cchardet.detect(r.content)["encoding"]
    bs = soup(r.text, "html.parser")

    dates     = bs.html.body.table.table.find_all("date")
    times     = bs.html.body.table.table.find_all("time")
    callsigns = bs.html.body.table.table.find_all("callsignto")
    freqs     = bs.html.body.table.table.find_all("freq")
    qths      = bs.html.body.table.table.find_all("qth")
    qth_names = bs.html.body.table.table.find_all("qthname")
    comments  = bs.html.body.table.table.find_all("comments")

    histories = list()
    for d, t, cs, f, q, qn, c in zip(dates, times, callsigns, freqs, qths, qth_names, comments):
      histories.append(JClusterInfoClass(d.string, t.string, cs.string, f.string, q.string, qn.string, c.string))

    return histories

  def getBandURL(self):
    return self.JCLUSTER_BAND_URL + "/SSB.html"

#------------------------------

class CallsignFilterClass:
  CALLSIGN_FILTER_LIST_FILE_PATH = "/data/callsign_filter_list.txt"

  callsign_filter_list = list()

  def __init__(self):
    if os.path.exists(self.CALLSIGN_FILTER_LIST_FILE_PATH):
      with open(self.CALLSIGN_FILTER_LIST_FILE_PATH) as f:
        self.callsign_filter_list = f.readlines()

  def filter(self, callsign):
    for sign in self.callsign_filter_list:
      if 0 == callsign.find(sign[:-1]):
        return True

    return False

#------------------------------

class LINEApiClass:
  API_NOTIFY_URI = "https://notify-api.line.me/api/notify"

  def __init__(self, token_file_path):
    if os.path.exists(token_file_path):
      with open(token_file_path) as f:
        self.token = f.read()[:-1]

  def postNotify(self, message):
    payload = {"message": message}
    headers = {"Authorization": "Bearer " + self.token}
    rq.post(self.API_NOTIFY_URI, data=payload, headers=headers)

#------------------------------

class LatestDateClass:
  FILE_PATH = "/data/latest_date.log"

  latest_date = ""
  next_latest_date = ""

  def __init__(self):
    if os.path.exists(self.FILE_PATH):
      with open(self.FILE_PATH) as f:
        self.latest_date = f.read()

  def isNewRecord(self, date_time):
    return self.latest_date == "" or self.latest_date < date_time

  def update(self, date_time):
    if self.next_latest_date == "" or self.next_latest_date < date_time:
      self.next_latest_date = date_time

  def isUpdate(self):
    if "" != self.next_latest_date:
      with open(self.FILE_PATH, mode = "w") as f:
        f.write(self.next_latest_date)
      return True
    return False

#------------------------------

def main():

  args = sys.argv

  jCluster = JClusterClass()
  jInfos = jCluster.requestHistories()

  filter = CallsignFilterClass()

  latest = LatestDateClass()

  message = "\n"
  for jInfo in jInfos:
    date_time = jInfo.getDateTime()
    if latest.isNewRecord(date_time):
      if filter.filter(jInfo.callsign):
        message += jInfo.time + " - " + jInfo.callsign + " : " + jInfo.freq + "\n"
        if jInfo.qth:
          message += " " + jInfo.qth + " : " + jInfo.qth_name + "\n"
        if jInfo.comment:
          message += " " + jInfo.comment + "\n\n"
        latest.update(date_time)

  message += jCluster.getBandURL()

  if latest.isUpdate():
    api = LINEApiClass(TOKEN_FILE_PATH)
    api.postNotify(message)

#------------------------------

if __name__ == "__main__":
  main()

