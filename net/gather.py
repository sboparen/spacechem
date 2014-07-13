#!/usr/bin/env python2
import os, sys, datetime
import entry, levels

class user:
  def __init__(self, username):
    self.name = username
  def __str__(self):
    return '<user %s>' % self.name

def levels_and_users(usernames):
  ### Levels.
  levels.get()
  for lv in levels.in_order:
    lv.least_cycles = entry.get_least_cycles(lv)
  ### Users.
  users = []
  for username in usernames:
    u = user(username)
    u.entries = entry.get_user_entries(username)
    users.append(u)
  ### Done!
  return (levels.in_order, users)

########################################################################
if __name__ == '__main__':
  levels, users = levels_and_users([os.getenv('USER')])
  print users[0].entries[0]
