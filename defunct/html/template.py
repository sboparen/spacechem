#!/usr/bin/env python2
from datetime import *
from lxml import etree
from lxml.builder import E
def CLASS(*args): # class is a reserved word in Python
  return {"class":' '.join(args)}

### There should only be one copy of this object, so that we
### are consistent.
now = datetime.now()

def navigation(users):
  table = E.table()
  for user in users:
    row = E.tr()
    row.append(E.th(user.name))
    row.append(E.td(E.a('Least Cycles',
      href='%s.html' % user.name)))
    table.append(row)
  return table

def wrap(content, title, users):
  page_title = 'SpaceChem Comparison'
  if title != '':
    page_title = '%s - %s' % (title, page_title)
  style = E.link(rel='stylesheet', type='text/css',
    href='static/style.css')
  content_type = E.meta({'http-equiv' : 'Content-Type'},
    content='text/html;charset=utf-8')
  head = E.head(content_type, E.title(page_title), style)
  body = E.body()
  body.append(E.h1('SpaceChem Comparison'))
  body.append(navigation(users))
  body.append(content)
  body.append(E.p('This page was generated\n' +
    now.strftime('on %A, %d %B %Y at %I:%M:%S %p\n')))
  # TODO least cycles collection times
  page = E.html(head, body)
  doctype = '''
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN"
                      "http://www.w3.org/TR/html4/loose.dtd">
'''.strip()
  return etree.tostring(page, doctype=doctype, method='html',
    pretty_print=True)
