# neoreset

_Neo's auto resetter for Minecraft speedrunning on Linux._

---

WORK IN PROGRESS...

- [x] 1.16
- [x] RSG
- [x] Linux
- [x] SSG
- [x] FSG
- [ ] 1.14
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

Activate venv:

```
python3 -m venv .venv
source .venv/bin/activate
```

Install requirements:

```
pip install -r requirements.txt
```

Run neoreset:

```
./neoreset.py
```

## Credits

Thanks to [@AndyNovo](https://github.com/andynovo) for the FSG goodies.
