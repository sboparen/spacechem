#!/usr/bin/env python2
import os, sys, datetime
import history, levels, exclude
from lxml import etree

### Solution entry, either from a user's page, or from a leaderboard.
class entry:
  def __init__(self, level, user, cycles, symbols, reactors,
               uploaded,
               solution_id, cycles_rank):
    self.level = level
    self.user = user
    self.cycles = cycles
    self.symbols = symbols
    self.reactors = reactors
    self.uploaded = uploaded
    self.solution_id = solution_id
    self.cycles_rank = cycles_rank
  def __str__(self):
    return '<entry %d by %s for %s>' % \
      (self.solution_id, self.user, self.level)

### Parse a user's page or leaderboard page, returning a list of
### solution entries.
def parse_page(data, user_page=None, level_page=None):
  root = etree.HTML(data)
  els = root.xpath("//tr")
  ret = []
  for el in els:
    user = user_page
    level = level_page
    children = el.getchildren()
    td_rank = None
    if len(children) == 6:
      td_rank = children[0]
      children = children[1:]
    td_level, td_cycles, td_symbols, td_reactors, td_uploaded = \
      children
    if td_level.tag == 'th': continue ### Ignore header rows.
    ### Rank column.
    rank = None
    if td_rank != None:
      rank = int(td_rank.text)
    ### Level/User column.
    ### There might be more than one child element, because sometimes
    ### there is a comment.
    a = td_level.getchildren()[0]
    if level == None:
      num = a.text.encode('utf8').split()[0]
      level = levels.by_num[num]
      sid = int(a.get('href').split('/')[-1])
    elif user == None:
      user = a.text
      sid = int(a.get('href').split('/')[-1])
    assert user != None and level != None
    ### Cycles column.
    cycles = int(td_cycles.text)
    if len(td_cycles.getchildren()) > 0:
      assert rank == None
      br, div = td_cycles.getchildren()
      a_ranks = div.getchildren()
      if len(a_ranks) > 0:
        rank = a_ranks[0].text
        if 'R)' in rank:
          rank = None ### I only want the main leaderboard.
        else:
          for suffix in ['st', 'nd', 'rd', 'th']:
            rank = rank.rstrip(suffix)
          rank = int(rank)
    ### Symbols column.
    symbols = int(td_symbols.text)
    ### Reactors column.
    reactors = int(td_reactors.text)
    ### Uploaded column.
    uploaded = td_uploaded.text
    ### SolutionNet has the year now, yay!
    uploaded = datetime.datetime.strptime(uploaded, '%Y-%m-%d, %H:%M')
    ### Make the entry object.
    e = entry(level, user, cycles, symbols, reactors,
      uploaded, sid, rank)
    if e.solution_id not in exclude.sids:
      ret.append(e)
  return ret

def get_user_entries(username):
  data = history.get('user/%s.html' % username)
  return parse_page(data, user_page=username)

def get_least_cycles(level):
  try:
    data = history.get('cycles/%s.html' % level.num)
    return parse_page(data, level_page=level)
  except KeyError:
    return []

########################################################################
if __name__ == '__main__':
  levels.get()
  for e in get_user_entries(os.getenv('USER')):
    print e
  for e in get_least_cycles(levels.by_num['2-1']):
    print e
