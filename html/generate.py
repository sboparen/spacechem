#!/usr/bin/env python2
import sys
from compare import tabulate
import makepage
levels, users, root = tabulate.go(sys.argv[1:])
with open('output/index.html', 'w') as fh:
  fh.write(makepage.index_page(levels, users, root))
for u in users:
  with open('output/%s.html' % u.name, 'w') as fh:
    fh.write(makepage.personal_page(levels, users, root, u))
