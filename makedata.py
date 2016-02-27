#!/usr/bin/env python2
import ast
import json
import os
import subprocess

levels = []

# Start with the levels dumped from SolutionNet's database.
if not os.path.exists('levels.sql'):
    url = 'https://raw.githubusercontent.com/' \
          'AndrewSav/SolutionNet/master/levels.sql'
    subprocess.check_call(['wget', url])
with open('levels.sql') as f:
    for line in f.readlines():
        if not line.startswith('INSERT INTO'):
            continue
        line = line[line.index('('):line.rindex(',')] + ')'
        data = ast.literal_eval(line)
        _, name, id, number, _, _, _, _ = data
        levels.append({'id': id, 'number': number, 'name': name})

# Add the missing ResearchNet level names.
from defunct.net.names import researchnet
for level in levels:
    if level['name'].startswith('ResearchNet Published'):
        level['name'] = researchnet(level['number'])

# Now sort by the "planet number".
from defunct.compare.planets import pnum_from_num
for level in levels:
    level['planet'] = pnum_from_num(level['number'])
levels.sort(key=lambda level: (level['planet'], level['number']))

# Get the cycle records from saved SolutionNet pages.
from defunct.net.entry import parse_page
for level in levels:
    with open('defunct/pages/cycles/%s.html' % level['number']) as f:
        entries = parse_page(f.read(), level_page='dummy')
        level['cycleTarget'] = entries[0].cycles

# Write out the data as JSON.
with open('offline/data.js', 'w') as f:
    data = json.dumps(levels, indent=4, sort_keys=True)
    data = data.replace(' \n', '\n')
    f.write('levelData = %s;\n' % data)
