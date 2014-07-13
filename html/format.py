#!/usr/bin/env python2
import template
from lxml import etree
from lxml.builder import E
def CLASS(*args): # class is a reserved word in Python
  return {"class":' '.join(args)}

def excess(excess, grade):
  return E.span(CLASS('grade_%s' % grade), '%d%%' % excess)

def grade(grade):
  text = grade
  if grade.endswith('star'):
    unicodestar = unicode('\xe2\x98\x85', 'UTF-8')
    text = unicodestar * int(grade[0])
  return E.span(CLASS('grade_%s' % grade),
    E.img(alt=text, src='static/grade_%s.gif' % grade))

def how_long_ago(dt):
  days = (template.now - dt).days
  if days < 1:
    return '< 1 day ago'
  elif days == 1:
    return '1 day ago'
  else:
    return '%d days ago' % days

def medal(medal):
  suffixes = ['st', 'nd', 'rd', 'th']
  text = '%d%s Place' % (medal, suffixes[min(medal, 4) - 1])
  return E.span(CLASS('medal_%s' % medal),
    E.img(alt=text, title=text, src='static/medal_%02d.gif' % medal))

def symbols(n):
  return '%d %s' % (n, 'symbols' if n != 1 else 'symbol')

########################################################################
if __name__ == '__main__':
  from datetime import *
  print how_long_ago(datetime(2012, 1, 1))
