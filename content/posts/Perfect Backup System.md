---
title: "Perfect Backup System"
date: 2026-10-03T22:02:01+05:30
draft: false
---

I run a little Homelab: Jellyfin for media, Pi-hole, Nextcloud, Glance as a dashboard, and Vaultwarden for passwords. Everything runs in Docker. For a long time my backup plan was "hope nothing breaks". Then I put my passwords on it, and hope stopped being good enough.

I wanted something simple enough that I'd actually use it. Here's what I ended up with.

### What gets backed up

- **Compose files and configs** for every service. These are small, and they're what I need to rebuild the setup from scratch.
- **Nextcloud's database**, exported properly with `mariadb-dump`.
- **Vaultwarden**, using its built-in backup command for a consistent database snapshot.

What I skip on purpose: movies and music (huge, and replaceable), Redis (just a cache), and the raw database folders of running containers.

How I made this, 

```Bash
#!/bin/bash
set -e
H=/home/youruser
BK=$H/backups
D=$(date +%F)
source $H/.nc-backup.cred
mkdir -p $BK

# Vaultwarden: consistent SQLite snapshot (saved inside its data folder)
docker exec vaultwarden /vaultwarden backup

# configs + compose files (live DB files excluded)
tar -czf $BK/homelab-$D.tar.gz --exclude='nextcloud/db' --exclude='vaultwarden/data/db.sqlite3*' $H/glance $H/pihole $H/nextcloud $H/docker/media-server $H/vaultwarden

# Nextcloud database dump
docker exec nextcloud-db sh -c 'mariadb-dump -u root -p"${MARIADB_ROOT_PASSWORD:-$MYSQL_ROOT_PASSWORD}" --all-databases' > $BK/nextcloud-db-$D.sql
tail -n 1 $BK/nextcloud-db-$D.sql | grep -q "Dump completed"

# upload to Nextcloud
for f in homelab-$D.tar.gz nextcloud-db-$D.sql; do
  curl -fsS -u "$NC_USER:$NC_PASS" -T $BK/$f "http://localhost:8082/remote.php/dav/files/$NC_USER/Backups/$f"
done

# cleanup: local copies older than 28 days
find $BK -name 'homelab-*.tar.gz' -mtime +28 -delete
find $BK -name 'nextcloud-db-*.sql' -mtime +28 -delete
find $H/vaultwarden/data -name "db_*.sqlite3" -mtime +28 -delete
chown -R youruser:youruser $BK
echo "Backup $D done"

```

If you make the above script exectable and you could just run `sudo ~/backup.sh` and your backup will be ready.
### Where the backups go

I already run Nextcloud, so I use it as the backup destination instead of setting up something new. Its data lives on an external SD card, so the uploaded copies sit on a different drive from the server's internal SSD. The script also keeps a local copy in `~/backups` for 28 days, so there are two copies on two different drives.

The script uploads to a `Backups` folder in Nextcloud over WebDAV with `curl`, using an app password. That way it never touches my real login and I can revoke it on its own.

Impressive Right?