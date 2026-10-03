import os, datetime

posts = os.environ["VAULT_POSTS"]
for f in os.listdir(posts):
    if not f.endswith(".md"):
        continue
    p = os.path.join(posts, f)
    text = open(p, encoding="utf-8").read()
    if text.lstrip().startswith("---"):
        continue
    title = os.path.splitext(f)[0].replace('"', "'")
    when = datetime.datetime.fromtimestamp(os.path.getmtime(p)).astimezone().isoformat(timespec="seconds")
    header = f'---\ntitle: "{title}"\ndate: {when}\ndraft: false\n---\n\n'
    open(p, "w", encoding="utf-8").write(header + text)
    print("added front matter to", f)
