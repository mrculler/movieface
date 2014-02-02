# Movie Face
====

A simple web-based UI to rename and organize large collections of movie files.

Perfect for a home theater setup where a large storage server shares collections of DVDs backed upo to .iso, .mkv, .mp4 or any other file type via SAMBA or NFS over the local network to frontend boxes running XBMC or similar.

XBMC's scrapers do a good job of pulling down movie info based on filenames, but they aren't perfect, and for people ripping hundreds of DVDs it can be infeasible to perfectly name each file by hand.  This program searches TMDB (if you have an API key) for the movie that corresponds with the file, and allows users to rename the file with a simple click.

This is still a pretty rough cut, but the core functionality exists.
