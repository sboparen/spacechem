#!/usr/bin/env python2
import os, sys
import history, names
from lxml import etree

def make_ascii(name):
  ret = name
  ret = ret.replace('\xc3\xa9', 'e')
  ret = ret.replace('\xc3\xb6', 'o')
  ret = ret.replace('\xce\xa3', 'Sigma')
  ret = ret.replace('\xce\xa9', 'Omega')
  ret.decode('ascii') ### This will fail if we missed something.
  return ret

class level:
  def __init__(self, num, title, linkname):
    self.num = num
    self.title = title
    self.ascii_title = make_ascii(title)
    self.unicode_title = unicode(title, 'UTF-8')
    self.linkname = linkname
  def __str__(self):
    return '<level %s>' % self.num

def parse(data):
  levels = []
  root = etree.HTML(data)
  els = root.xpath("//tr")
  for el in els:
    name, cycles, symbols = el.getchildren()
    name = name.text
    if type(name) == unicode:
      name = name.encode('utf8')
    idx = name.index(' - ')
    num, title = name[:idx], name[idx+3:]
    if title.startswith('ResearchNet Published '):
      title = names.researchnet(num)
    link, = cycles.getchildren()
    url = link.get('href')
    linkname = url.split('/')[2]
    lv = level(num, title, linkname)
    assert num not in levels
    levels.append(lv)
  return levels

in_order = None
by_num = {}
def get():
  global in_order
  if in_order != None:
    return
  in_order = parse(history.get('levels.html'))
  for lv in in_order:
    by_num[lv.num] = lv

########################################################################
if __name__ == '__main__':
  get()
  for lv in in_order:
    print lv
