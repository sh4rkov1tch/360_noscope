# 360 Noscope
It's pretty straightforward: It's a download helper from the ROMs Megathread 4.0

# Usage
When you launch it for the first time, it takes a while before showing anything, that's expected because it is caching all the links (and trust me there are an awful lot of games and DLC you can download..)

```bash
$ python3 main.py -h
usage: 360 NoScope [-h] [-o OUTPUT] [--force-refresh | --no-force-refresh] search_string

Download helper for original Xbox and Xbox 360 games

positional arguments:
  search_string         The name of the game you want

options:
  -h, --help            show this help message and exit
  -o OUTPUT, --output OUTPUT
                        The output folder you want to download your game to, defaults to the current dir.
  --force-refresh, --no-force-refresh
                        Force a games.json refresh
```

# Caveats
The downloads are kinda slow but eh you're not in a hurry right ?