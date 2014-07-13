#!/usr/bin/env python2
import os, sys
import net.gather

def quantile(levels, name='median', p=50):
  u = net.gather.user(name)
  u.entries = []
  for lv in levels:
    arr = lv.least_cycles
    k = (len(arr) - 1) * (100 - p) / 100
    assert 0 <= k < len(arr)
    u.entries.append(arr[k])
  return u
