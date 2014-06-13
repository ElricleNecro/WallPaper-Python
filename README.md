WallPaper-Python
================

Change dynamically the wallpaper

## Dependences
==============

- feh: to set the wallpaper
- python 3.1 or later

Extra configuration
-------------------

If you want to run the daemon as a service for user in systemctl, simply
copy the `wallpaper.service` to `~/.config/systemd/user/`. For a service for
the system, put it in `/etc/systemd/system/`

The systemctl service example file was wrong for its first version to use it
as a simple user. The `WantedBy` target is not `multi-user.target` for user
services but must be linked to `default.target`.

If you have already installed and used it, simply disable the previous
service:

```bash
systemctl --user disable wallpaper.service # no more linked to multi-user.target
```

then re-enable it to `default.target`:

```bash
systemctl --user enable wallpaper.service
```
and start it if not already done:

```bash
systemctl --user start wallpaper.service
```

If you want to run the service not as an user, keep the `multi-user.target`
in the `WantedBy` field.

That's all!
