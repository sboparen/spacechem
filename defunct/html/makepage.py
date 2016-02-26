#!/usr/bin/env python2
import format, template
from lxml import etree
from lxml.builder import E
def CLASS(*args): # class is a reserved word in Python
  return {"class":' '.join(args)}

### Removes any columns which are empty for every row.
### Doesn't pay attention to colspan.
def remove_empty_columns(table):
  for idx, col in enumerate(table[0]):
    empty = True
    for row in table[1:]:
      if idx < len(row):
        if len(row[idx]) > 0 or row[idx].text != None:
          empty = False
    if empty:
      for row in table:
        if idx < len(row):
          del row[idx]
      return remove_empty_columns(table)
      break

def personal_planet_table(levels, users, pl, u):
  heading = E.h1(pl.title)
  table = E.table(E.tr(
    E.th('Level'),
    E.th('Best Known'),
    E.th(u.name),
    E.th('Award'),
    E.th('Excess'),
    E.th('Grade'),
    ))
  for lv in pl.children:
    level = '%s: %s' % (lv.num, lv.unicode_title)
    url = 'http://spacechem.net/leaderboards/%s/cycles' % lv.linkname
    level = E.a(level, href=url)
    level = E.td(level, style='text-align:left')
    best_known = E.td('%d' % lv.best_cycles.cycles)
    user_best = lv.best_cycles_by_user.get(u, None)
    cycles = E.td('unsolved', colspan='99')
    medal = None
    excess = None
    grade = None
    if user_best != None:
      medal = E.td()
      cycles = E.td('%d' % user_best.cycles)
      excess = E.td(format.excess(user_best.excess, user_best.grade))
      grade = E.td(format.grade(user_best.grade))
      ### Medal
      if user_best.medal != None:
        medal = E.td(format.medal(user_best.medal))
      ### Symbol count if we're at optimal cycles.
      if user_best.cycles == lv.best_cycles.cycles:
        best_known.append(E.br())
        best_known.append(E.span('(%s)' % \
          format.symbols(lv.best_cycles.symbols)))
        cycles.append(E.br())
        cycles.append(E.span('(%s)' % \
          format.symbols(user_best.symbols)))
        extra = user_best.symbols - lv.best_cycles.symbols
        if extra > 0:
          excess.append(E.br())
          excess.append(E.span('+%s' % format.symbols(extra)))
    row = E.tr()
    for col in level, best_known, cycles, medal, excess, grade:
      if col != None:
        row.append(col)
    table.append(row)
  remove_empty_columns(table)
  row = E.tr(
    E.th('Overall', colspan=str(len(table[0])-2)),
    E.td('TODO'),
    E.td('TODO'),
    )
  # TODO
  #table.append(row)
  heading.text += ' '
  heading.append(E.a('[back]', href='#top', style='font-size:small'))
  return E.div(E.a(name='planet_%s' % pl.pnum), heading, table)

def personal_planet_recurse(levels, users, pl, u):
  if pl.meta:
    ret = []
    for ch in pl.children:
      ret += personal_planet_recurse(levels, users, ch, u)
    return ret
  else:
    return [personal_planet_table(levels, users, pl, u)]

def summary(levels, users, planets, u):
  heading = E.h1('Summary')
  table = E.table(E.tr(
    E.th('Planet'),
    E.th('Excess'),
    E.th('Grade'),
    ))
  for pl in planets:
    row = E.tr()
    row.append(E.th(E.a(pl.title, href='#planet_%s' % pl.pnum)))
    s = pl.user_stats[u]
    if s.complete:
      row.append(E.td(format.excess(s.excess, s.grade)))
      row.append(E.td(format.grade(s.grade)))
    else:
      row.append(E.td('incomplete', colspan='2'))
    table.append(row)
  return E.div(E.a(name='top'), heading, table)

def personal_page(levels, users, root, u):
  content = E.div()
  content.append(summary(levels, users, root.planets(), u))
  for div in personal_planet_recurse(levels, users, root, u):
    content.append(div)
  return template.wrap(content, '%s - Least Cycles' % u.name, users)

def index_page(levels, users, root):
  content = E.div()
  return template.wrap(content, '', users)
