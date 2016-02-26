#!/usr/bin/env python2
import os, sys

### Find the best solutions for each level,
### both overall, and from each participating user.
def process(levels, users):
  for lv in levels:
    lv.best = None
    if len(lv.least_cycles) > 0:
      lv.best_cycles = lv.least_cycles[0]
    lv.best_cycles_by_user = {}
    for u in users:
      best = None
      for e in u.entries:
        if e.level == lv and e.cycles_rank != None:
          best = e
      if best != None:
        lv.best_cycles_by_user[u] = best
        for e in u.entries:
          if e.level == lv:
            assert best.cycles <= e.cycles
