#!/usr/bin/env python2
import excess

class stats:
  def __init__(self, user, planet):
    self.user = user
    self.planet = planet
  def __str__(self):
    return '<stats %s/%s>' % (self.user.name, self.planet.pnum)

def process(planet, users):
  if 'children' in planet.__dict__:
    for ch in planet.children:
      process(ch, users)
  planet.user_stats = {}
  for u in users:
    s = stats(u, planet)
    s.excess = []
    s.inhabited = False
    s.complete = True
    if 'children' not in planet.__dict__:
      user_best = planet.best_cycles_by_user.get(u, None)
      if user_best == None:
        s.complete = False
      else:
        s.inhabited = True
        s.excess.append(user_best.excess)
    else:
      for ch in planet.children:
        ch_s = ch.user_stats[u]
        if ch_s.inhabited:
          s.inhabited = True
        if ch_s.complete:
          s.excess.append(ch_s.excess)
        else:
          s.complete = False
    if s.complete:
      s.excess = max(s.excess)
      s.grade = excess.grade(s.excess)
    else:
      s.excess = None
      s.grade = None
    planet.user_stats[u] = s
