#!/usr/bin/env python2
import os, sys, datetime
import pygit2

### Assume we're somewhere in the spacechem-scripts git repository.
### Also assume the pages git repository has already been made,
### and has at least one commit.
our_git = pygit2.discover_repository('.')
pages_git = os.path.join(our_git, '../defunct/pages/.git')
repo = pygit2.Repository(pages_git)
dummy = repo.head

### Well, one downside to pygit2 is that it seems to be quite
### low level.
def split_fully(path):
  if path == '':
    return []
  head, tail = os.path.split(path)
  return split_fully(head) + [tail]
def add_file(tree, path, data):
  if type(path) == str:
    path = split_fully(path)
  if len(path) == 1:
    filename, = path
    tb = repo.TreeBuilder(tree)
    oid = repo.create_blob(data)
    tb.insert(filename, oid, pygit2.GIT_FILEMODE_BLOB)
    return tb.write()
  else:
    dirname, subpath = path[0], path[1:]
    tb = repo.TreeBuilder(tree)
    subtree = tb.get(dirname)
    if subtree == None:
      subtree = repo.TreeBuilder().write()
    else:
      subtree = repo.get(subtree.oid)
    oid = add_file(subtree, subpath, data)
    tb.insert(dirname, oid, pygit2.GIT_FILEMODE_TREE)
    return tb.write()

### Get the contents of a file.
### I might eventually support looking back in time,
### but this seems to be less important than I thought.
def get(path):
  e = repo.get(repo.head.target).tree[path]
  return repo.get(e.oid).data

timefmt = '%Y-%m-%d %H:%M:%S\n'
def last_update(path):
  try:
    return datetime.datetime.strptime(get(path+'.stamp'), timefmt)
  except KeyError:
    return None
  print e
  return 'dunno'

### Save a new version of a file.
### I'm okay with empty commits because they're a record that the
### file was downloaded again and hasn't changed.
### The .stamp file stores a timestamp of when the page
### was last downloaded.
def save(path, data):
  timestamp = datetime.datetime.utcnow().strftime(timefmt)
  sig = pygit2.Signature('SpaceChem Bot', 'noreply@example.com')
  msg = '%s\n' % path
  tree = repo.get(repo.head.target).tree
  tree = add_file(tree, path, data)
  tree = add_file(tree, path+'.stamp', timestamp)
  parent = repo.head.target
  repo.create_commit('refs/heads/master', sig, sig, msg, tree, [parent])
  repo.checkout('HEAD', pygit2.GIT_CHECKOUT_FORCE)

########################################################################
if __name__ == '__main__':
  print repo.head.target.hex
  for e in repo.get(repo.head.target).tree:
    print e.hex, e.name
  print repr(get('testing/test1.txt').data)
