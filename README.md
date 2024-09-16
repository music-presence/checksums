# Checksums and signatures

This repository contains a mirror of checksum and signature files
of each Music Presence release, which is hosted on GitHub Pages.
Music Presence downloads these files from here
instead of from the release attachments,
such that the download counter on GitHub is not artifically inflated
and keeps showing the real download count
(one increment per automatic or in-app update).

This separation is necessary,
otherwise the download counter would increase by 3 instead of 1
for each update.
Unfortunately the badge in the
[README](https://github.com/ungive/discord-music-presence/blob/master/README.md)
can't filter out specific files:

- https://shields.io/badges/git-hub-downloads-all-assets-latest-release

## Verifying checksums

```
pip install invoke
invoke verify
```

This verifies the *live* (online, pushed) checksums and signatures.
It does *not* verify the local files.
Push to the remote and wait for the GitHub pages deployment to finish
before running this command.
