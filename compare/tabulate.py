#!/usr/bin/env python2
import os, sys
import net.gather
import collect
import excess
import find_best
import medals
import median_user
import planets

def go(usernames):
  levels, users = net.gather.levels_and_users(usernames)
  #users.append(median_user.quantile(levels, 'worst', 0))
  #users.append(median_user.quantile(levels, 'median', 50))
  #users.append(median_user.quantile(levels, '90th', 90))
  find_best.process(levels, users)
  excess.process(users)
  medals.process(users)
  root = planets.organize(levels)
  collect.process(root, users)
  return levels, users, root

########################################################################
if __name__ == '__main__':
  levels, users, root = go([os.getenv('USER')])
  for lv in levels:
    print lv.planet
