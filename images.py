import os, re, shutil

posts = "content/posts"
attach = os.environ["VAULT_ATTACH"]
static = "static/images"
os.makedirs(static, exist_ok=True)

pat = re.compile(r'!\[\[([^\]|]+\.(?:png|jpe?g|gif|webp))(?:\|[^\]]*)?\]\]', re.I)

for f in os.listdir(posts):
    if not f.endswith(".md"):
        continue
    p = os.path.join(posts, f)
    text = open(p, encoding="utf-8").read()

    def fix(m):
        img = m.group(1)
        src = os.path.join(attach, img)
        if os.path.exists(src):
            shutil.copy(src, static)
        return f"![{img}](/images/{img.replace(' ', '%20')})"

    open(p, "w", encoding="utf-8").write(pat.sub(fix, text))
print("images done")
