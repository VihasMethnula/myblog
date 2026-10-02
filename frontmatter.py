import os, datetime

posts = "content/posts"
for f in os.listdir(posts):
    if not f.endswith(".md"):
        continue
    p = os.path.join(posts, f)
    text = open(p, encoding="utf-8").read()
    if text.lstrip().startswith("---"):
        continue
    title = os.path.splitext(f)[0].replace('"', "'")
    date = datetime.date.fromtimestamp(os.path.getmtime(p))
    header = f'---\ntitle: "{title}"\ndate: {date}\ndraft: false\n---\n\n'
    open(p, "w", encoding="utf-8").write(header + text)
print("frontmatter done")
