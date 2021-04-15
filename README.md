# neoreset

_Neo's auto resetter for Minecraft speedrunning on Linux._

---

WORK IN PROGRESS...

- [x] 1.16
- [ ] 1.14
- [x] RSG
- [x] SSG
- [x] FSG
- [x] Linux
- [ ] macOS
- [ ] Windows

## Features

- RSG/SSG/FSG
- Global and per session counter in world name
- Included filters
    - filteredseed
    - filteredvillage
    - filteredshipwreck
    - ruined-portal-loot
    - fsg-power-village-looting-sword

## Usage

Activate python virtual environment.

```
python3 -m venv .venv
source .venv/bin/activate
```

Install dependencies.

```
pip install -r requirements.txt
```

Run neoreset…

```
./neoreset.py
```

Press your hotkey and reset away!

## Config

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

## Credits

Thanks to [@AndyNovo](https://github.com/andynovo) for the FSG goodies.
