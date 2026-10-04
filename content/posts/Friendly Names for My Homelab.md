---
title: "Friendly Names for My Homelab"
date: 2026-10-04T19:14:35+05:30
draft: false
---

My homelab has been a pile of port numbers for a while. Jellyfin is `8096`, Nextcloud is `8082`, Glance is `8080`, and Pi-hole is `8081`. I knew where everything was, but only because I'd typed those numbers so many times.

I wanted to type `jellyfin.home` and get Jellyfin. Here's how that went.
### What I used

- **Nginx Proxy Manager** takes a hostname like `jellyfin.home` and sends it to the right container. It runs in Docker with a web UI
- **Pi-hole's Local DNS** makes the name resolve in the first place. NPM can only route a request once it arrives. Something else has to tell the laptop that `jellyfin.home` means "this machine".

![Pasted image 20261004191423.png](/images/Pasted%20image%2020261004191423.png)

### How it fits together

1. Pi-hole gets a record: `jellyfin.home` → `127.0.0.1`.
2. The request lands on NPM, which listens on ports 80 and 443.
3. NPM forwards it to Jellyfin on port `8096`.

I used `127.0.0.1` because I only use these services from this laptop. It works on any Wi-Fi and never breaks when the router hands out a new IP.

NPM is part of the stack now,
![Pasted image 20261004191353.png](/images/Pasted%20image%2020261004191353.png)