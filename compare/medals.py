#!/usr/bin/env python2
import os, sys

def compute_medals(u, e):
  e.medal = None
  if e.cycles_rank != None and e.cycles_rank <= 10:
    e.medal = e.cycles_rank
    u.medals[e.medal - 1].append(e)

def process(users):
  for u in users:
    u.medals = [[] for i in xrange(10)]
    for e in u.entries:
      compute_medals(u, e)
    u.medals = sum(u.medals, [])
