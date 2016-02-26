#!/usr/bin/env python2
import os, sys

planet_title = {
'1':'Sernimir II',
'2':'Sernimir IV',
'3':'Danopth',
'4':'Alkonost',
'5':'Sikutar',
'6':'Hephaestus IV',
'7':'Atropos Station',
'8':'Fildais',
'9':'Unknown System',
'TF2':'Moustachium',
'63':'63 Corvi',
}

class planet:
  def __init__(self, pnum, title, meta=False):
    self.pnum = pnum
    self.title = title
    self.meta = meta
    ### If meta is True, then the children are planets.
    ### Otherwise, the children are levels.
    self.children = []
  def __str__(self):
    return '<planet %s>' % self.pnum
  def planets(self):
    if self.meta:
      return sum([ch.planets() for ch in self.children], [])
    else:
      return [self]

def pnum_from_num(num):
  if '-' not in num:
    ### 63 Corvi.
    return '63'
  else:
    num = num.split('-')
    if len(num) == 3 or (num[0].isdigit() and int(num[0]) >= 28):
      ### ResearchNet.
      if len(num) == 3:
        issue_0 = 12 * (int(num[0]) - 1) + (int(num[1]) - 1)
      else:
        issue_0 = (int(num[0])  - 1)
      quarter_0 = issue_0 / 3
      volume  = 1 + quarter_0 / 4
      quarter = 1 + quarter_0 % 4
      return 'R%dQ%d' % (volume, quarter)
    else:
      ### Ordinary level, just take the first part.
      assert len(num) == 2
      return num[0]

def organize(levels):
  ### Main Game.
  main_game = []
  for pnum in [str(x) for x in xrange(1, 9+1)]:
    main_game.append(planet(pnum, planet_title[pnum]))
  ### Bonus Content.
  bonus_content = []
  for pnum in ['TF2', '63']:
    bonus_content.append(planet(pnum, planet_title[pnum]))
  ### ResearchNet.
  researchnet = []
  for volume in xrange(1, 4+1):
    for quarter in xrange(1, 4+1):
      pnum = 'R%dQ%d' % (volume, quarter)
      roman = [None, 'I', 'II', 'III', 'IV']
      title = 'Volume %s Quarter %d' % (roman[volume], quarter)
      researchnet.append(planet(pnum, title))
  ### Create the meta-planets.
  mg = planet('MG', 'Main Game', meta=True)
  mg.children = main_game
  bc = planet('BC', 'Bonus Content', meta=True)
  bc.children = bonus_content
  rn = planet('RN', 'ResearchNet', meta=True)
  rn.children = researchnet
  root = planet('X', 'Literally Everything', meta=True)
  root.children = [mg, bc, rn]
  ### Add the levels to the planets.
  planet_by_pnum = dict([(pl.pnum, pl) for pl in root.planets()])
  for lv in levels:
    pnum = pnum_from_num(lv.num)
    pl = planet_by_pnum.get(pnum, None)
    lv.planet = pl
    pl.children.append(lv)
  ### Done!
  return root
