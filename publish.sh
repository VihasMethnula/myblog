#!/bin/bash
set -euo pipefail
cd "$(dirname "$0")"

export VAULT_POSTS="$HOME/Documents/Ideas/posts"
export VAULT_ATTACH="$HOME/Documents/Ideas/Attachments"

rsync -av --delete "$VAULT_POSTS/" content/posts/
python3 images.py
hugo --gc --minify

git add .
if git diff --cached --quiet; then
  echo "Nothing new to publish."
else
  git commit -m "post $(date +'%F %T')"
  git push
  echo "Pushed. Vercel is deploying."
fi
