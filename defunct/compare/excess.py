#!/usr/bin/env python2
import os, sys

### Round positive values up, so that we are pessimistic.
### But round negaive values down, so that zero really means zero.
def rounded_percentage(num, den):
  assert den > 0
  num *= 100
  if num < 0:
    return num / den
  else:
    return (num + den - 1) / den

def grade(percent):
  inf = float('inf')
  tiers = [
    (inf, 'D'),
    (400, 'C'),
    (200, 'B'),
    (100, 'A'),
    ( 50, 'S'),
    ( 25, '1star'),
    ( 12, '2star'),
    (  6, '3star'),
    (  0, '4star'),
    ( -1, '5star'),
  ]
  for p, g in sorted(tiers):
    if percent <= p:
      return g
  assert False

def compute_excess(e):
  best = e.level.best_cycles
  e.excess = None
  e.grade = None
  if best != None:
    e.excess = rounded_percentage(e.cycles - best.cycles, best.cycles)
    e.grade = grade(e.excess)

def process(users):
  for u in users:
    for e in u.entries:
      compute_excess(e)
