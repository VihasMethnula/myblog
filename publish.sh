#!/bin/bash
set -euo pipefail
cd "$(dirname "$0")"

export VAULT_POSTS="$HOME/Documents/Ideas/posts"
export VAULT_ATTACH="$HOME/Documents/Ideas/Attachments"

rsync -av --delete "$VAULT_POSTS/" content/posts/
rm -f static/images/*
python3 images.py
python3 frontmatter.py
hugo --gc --minify

git add .
if git diff --cached --quiet; then
  git push; echo "Nothing new to commit. Pushed anything waiting."
else
  git commit -m "post $(date +'%F %T')"
  git push
  echo "Pushed. Vercel is deploying."
fi
