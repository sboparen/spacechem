#!/usr/bin/env python2
import os, sys, datetime
import download, history, levels

### Download the level list.
### It hasn't changed since December 2011,
### so only download it if we don't already have it.
if history.last_update('levels.html') == None:
  download.download_level_list()
levels.get()

### Download user pages.
users = sys.argv[1:]
for u in users:
  download.download_user(u)

### Download solution pages for any solutions involved
### in one of the special challenges.
# TODO

### Download the most out of date leaderboard.
### I run this script every hour, so this way they'll all be
### reasonably up to date without hammering the SolutionNet server.
for lv in levels.in_order:
  lv.last_update = history.last_update('cycles/%s.html' % lv.num)
  if lv.last_update == None:
    lv.last_update = datetime.datetime(2000, 1, 1)
k = 1
for lv in sorted(levels.in_order, key=lambda lv: lv.last_update)[:k]:
  download.download_least_cycles(lv)
