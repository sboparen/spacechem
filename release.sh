#!/bin/bash
set -e
test $# -eq 1
VERSION="$1"
sed -i README.md -e 's!\(cdn.rawgit.com/[^/]*/[^/]*/\)[^/]*!\1'"$VERSION!"
git add README.md
git commit -m "Tag version $VERSION."
git tag "$VERSION"
git push --tags
