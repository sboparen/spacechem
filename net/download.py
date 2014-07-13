#!/usr/bin/env python2
import os, sys
import pycurl, cStringIO, urllib
import history

def curl(url):
  sys.stderr.write("Downloading '%s'...\n" % url)
  fh = cStringIO.StringIO()
  c = pycurl.Curl()
  c.setopt(c.URL, url)
  c.setopt(c.WRITEFUNCTION, fh.write)
  c.perform()
  ret = fh.getvalue()
  fh.close()
  return ret

def download_level_list():
  url = 'http://spacechem.net/leaderboards'
  data = curl(url)
  history.save('levels.html', data)

def download_user(user):
  url = 'http://spacechem.net/user/%s' % urllib.quote(user)
  data = curl(url)
  history.save('user/%s.html' % user, data)

def download_least_cycles(lv):
  url = 'http://spacechem.net/leaderboards/%s/cycles' % lv.linkname
  data = curl(url)
  history.save('cycles/%s.html' % lv.num, data)

def download_solution(e):
  url = 'http://spacechem.net/solution/%s/%d' % \
    (e.level.linkname, e.solution_id)
  data = curl(url)
  filename = 'solution/%s.%s.%d.html' % \
    (e.user, e.level.num, e.solution_id)
  history.save(filename, data)

########################################################################
if __name__ == '__main__':
  import levels
  levels.get()
  #download_least_cycles(levels.by_num['2-1'])
  #download_solution((levels.by_num['1-4-1'], 78571))
  #download_level_list()
  download_user(os.getenv('USER'))
