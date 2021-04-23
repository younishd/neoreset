# neoreset

![](https://github.com/younishd/neoreset/actions/workflows/main.yml/badge.svg?branch=v1.1.1)
![GitHub release (latest by date)](https://img.shields.io/github/v/release/younishd/neoreset?color=ff69b4)

_Neo's auto resetter for Minecraft speedrunning on Linux._

---

![](screen.png)

## TL;DR

Download the latest release from [**here**](https://github.com/younishd/neoreset/releases/latest).

Run the executable (e.g. from a terminal) and press…
- **F7** to reset (from title screen)
- **F8** to switch category

## Features

- **RSG/SSG/FSG**
- Global and per session counter in world name
- Included filters
    - filteredseed
    - filteredvillage
    - filteredshipwreck
    - ruined-portal-loot
    - fsg-power-village-looting-sword

## Options

```
usage: neoreset [-h] [-v] [-c CONFIG_PATH]

optional arguments:
  -h, --help            show this help message and exit
  -v, --version         show program's version number and exit
  -c CONFIG_PATH, --config CONFIG_PATH
                        custom path to neoreset.json config file
```

### Examples

Pass a custom path to where the `neoreset.json` config file shall be:

```
neoreset --config /path/to/somewhere
```

This defaults to your `.minecraft` folder.

## Settings

Check out the file called `neoreset.json` in your `.minecraft` folder.

- `hotkey` - reset hotkey
- `hotkey2` - switch category hotkey
- `delay` - delay in seconds between simulated keyboard inputs
- `session_thresh` - threshold when to wrap a session (in seconds)
- `sound` - voice on/off
- `world_name` - world name format string with placeholders
    - `{c}` - category
    - `{v}` - version
    - `{s}` - per session counter
    - `{g}` - global counter
- `ssg.seed` - seed to be used for SSG category
- `fsg.filter` - filter to be used for FSG category
    - `filteredseed`
    - `filteredvillage`
    - `filteredshipwreck`
    - `ruined-portal-loot`
    - `fsg-power-village-looting-sword`

## Work in progress

- [x] 1.16
- [ ] 1.14
- [x] RSG
- [x] SSG
- [x] FSG
- [x] Linux
- [ ] macOS
- [ ] Windows

(PRs are welcome.)

## Dev

Clone the repository and set up a virtual environment as follows.

```
git clone https://github.com/younishd/neoreset.git
cd neoreset
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Run the script like this:

```
./neoreset.py
```

### PyInstaller

We're using [PyInstaller](https://pyinstaller.readthedocs.io) to bundle everything into a single binary.

Install the `pyinstaller` package as follows.

```
pip install pyinstaller
```

Then run the following command to build the binary:

```
pyinstaller neoreset.py \
        --onefile \
        --add-data assets:assets \
        --add-data VERSION:. \
        --add-data README.md:. \
        --add-data LICENSE:. \
        --add-data neoreset.json:. \
        --add-binary bin:bin \
        --add-binary lib:lib \
        --hidden-import=pynput.keyboard._xorg \
        --hidden-import=pynput.mouse._xorg
```

Run the new binary (outside the venv) like this

```
dist/neoreset
```

## Bugs

Feel free to report any issues [here](https://github.com/younishd/neoreset/issues) or DM me (`neo#0495`) on discord.

## Credits

Thanks to [@AndyNovo](https://github.com/andynovo) for the FSG goodies.
