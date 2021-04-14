#!/usr/bin/env python
##
## neoreset - Neo's auto resetter for Minecraft speedrunning on Linux
##
## Author: Younis Bensalah (neoprene1337)
##

import os
import sys
import json
import random
from time import time, sleep
from shutil import copyfile
from pynput.keyboard import Key, Controller, Listener
from boombox import BoomBox

class Neoreset:
    class Voice:
        GREETINGS = [ 'hello', 'hi', 'pog', 'lfg', 'wb' ]
        RESETS = [ 'reset', 'again', 'donged', 'godspeed', 'block' ]

        def __init__(self, path):
            self._path = path

        def _play(self, line):
            BoomBox(os.path.join(self._path, 'assets', line + '.ogg')).play()

        def play_random_greeting(self):
            self._play(random.choice(self.GREETINGS))

        def play_rsg(self):
            self._play('rsg')

        def play_ssg(self):
            self._play('ssg')

        def play_fsg(self):
            self._play('fsg')

        def play_reset(self):
            self._play('reset')

    def __init__(self, path):
        file = os.path.join(path, 'neoreset.json')
        if not (os.path.exists(file) and os.path.isfile(file)) or os.stat(file).st_size == 0:
            template = os.path.join(path, 'neoreset.empty.json')
            copyfile(template, file)
        with open(file) as f:
            self._config = json.load(f)
        self._file = file

        self._voice = self._voice = self.Voice(path) if self._config['static']['sound'] else None

        self._hotkey = getattr(Key, self._config['static']['hotkey'])
        self._hotkey2 = getattr(Key, self._config['static']['hotkey2'])
        self._version = self._config['static']['version']
        self._category = self._config['static']['category']
        self._delay = self._config['static']['delay']
        self._session_thresh = self._config['static']['session_thresh']
        self._world_name = self._config['static']['world_name']
        self._ssg_seed = self._config['static']['ssg']['seed']
        self._fsg_filter = self._config['static']['fsg']['filter']
        self._global_count = self._config['volatile'][self._version][self._category]['counter']['global']
        self._session_count = self._config['volatile'][self._version][self._category]['counter']['session']
        self._last_timestamp = self._config['volatile'][self._version][self._category]['last_run']['timestamp']

    def start(self):
        def on_press(key):
            pass

        def on_release(key):
            if key == self._hotkey:
                return self._on_reset()
            if key == self._hotkey2:
                return self._on_cycle()

        print("ready.")

        if self._voice:
            self._voice.play_random_greeting()

        with Listener(
                on_press=on_press,
                on_release=on_release) as listener:
            listener.join()

    def _on_reset(self):
        current_timestamp = int(time())
        if current_timestamp - self._last_timestamp > self._session_thresh:
            self._session_count = 0
        self._global_count += 1
        self._session_count += 1
        self._last_timestamp = current_timestamp

        world_name = self._world_name.format(
                c=self._category,
                v=self._version,
                s=self._session_count,
                g=self._global_count)

        if self._version == "1.14":
            resetter = FourteenResetter(
                    delay=self._delay,
                    world_name=world_name)
        elif self._version == "1.16":
            resetter = SixteenResetter(
                    delay=self._delay,
                    world_name=world_name)
        else:
            raise ValueError("Unknown version!")

        if self._category == "ssg":
            resetter = SetSeedDecorator(resetter, seed=ssg_seed)
        elif self._category == "fsg":
            resetter = FilteredSeedDecorator(SetSeedDecorator(resetter), filter=fsg_filter)
        elif self._category == "rsg":
            pass
        else:
            raise ValueError("Unknown category!")

        if self._voice:
            self._voice.play_reset()

        resetter.reset()

        self._write_back()

    def _on_cycle(self):
        if self._category == "rsg":
            self._category = "ssg"
        elif self._category == "ssg":
            self._category = "fsg"
        elif self._category == "fsg":
            self._category = "rsg"
        else:
            raise ValueError("Unknown category!")

        if self._voice:
            getattr(self._voice, 'play_' + self._category)()

    def _write_back(self):
        self._config['volatile'][self._version][self._category]['counter']['global'] = self._global_count
        self._config['volatile'][self._version][self._category]['counter']['session'] = self._session_count
        self._config['volatile'][self._version][self._category]['last_run']['timestamp'] = self._last_timestamp
        with open(self._file, 'w') as f:
            json.dump(self._config, f, indent=4)

class Resetter:
    def __init__(self, delay=0.07, world_name=None):
        self._keyboard = Controller()
        self._delay = delay
        self._world_name = world_name

    def reset(self):
        raise NotImplementedError

    def _tap(self, sequence: list):
        for key in sequence:
            self._keyboard.tap(key)
            sleep(self._delay)

class SixteenResetter(Resetter):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._version = "1.16"
        self._category = "rsg"

    def reset(self):
        self._new_world()
        self._enter_name()
        self._set_difficulty()
        self._create()

    def _new_world(self):
        self._tap([ Key.tab, Key.enter, Key.tab, Key.tab, Key.tab, Key.enter ])

    def _enter_name(self):
        self._keyboard.press(Key.ctrl_l)
        sleep(self._delay)
        self._tap([ Key.backspace, Key.backspace ])
        self._keyboard.release(Key.ctrl_l)
        sleep(self._delay)
        self._keyboard.type(self._world_name)
        sleep(self._delay)

    def _set_difficulty(self):
        # TODO difficulty option
        self._tap([ Key.tab, Key.tab, Key.enter, Key.enter, Key.enter ])

    def _create(self):
        self._tap([ Key.tab, Key.tab, Key.tab, Key.tab, Key.tab, Key.enter ])

class FourteenResetter(Resetter):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._version = "1.14"
        self._category = "rsg"

    def reset(self):
        # TODO 1.14
        raise NotImplementedError

class ResetterDecorator(Resetter):
    def __init__(self, resetter: Resetter):
        self._resetter = resetter

    def reset(self):
        self._resetter.reset()

class SetSeedDecorator(ResetterDecorator):
    def __init__(self, resetter: Resetter, seed='2483313382402348964'):
        super().__init__(resetter)
        self._seed = seed
        self._category = "ssg"

    def reset(self):
        self._resetter._new_world()
        self._resetter._enter_name()
        self._resetter._set_difficulty()

        self._tap([ Key.tab, Key.tab, Key.tab, Key.tab, Key.enter, Key.tab, Key.tab, Key.tab ])
        self._keyboard.type(self._seed)
        self._tap([ Key.tab, Key.tab, Key.tab, Key.tab, Key.tab, Key.tab, Key.enter ])

class FilteredSeedDecorator(ResetterDecorator):
    class Filter:
        SEED        = 'filteredseed',
        VILLAGE     = 'filteredvillage'
        SHIPWRECK   = 'filteredshipwreck'
        LOOTING     = 'fsg-power-village-looting-sword'
        PORTAL      = 'ruined-portal-loot'

    def __init__(self, resetter: Resetter, filter=Filter.SEED):
        super().__init__(resetter)
        self._filter = filter
        self._category = "fsg"

    def reset(self):
        # TODO fsg
        raise NotImplementedError

def main():
    path = os.path.dirname(os.path.abspath(__file__))
    Neoreset(path).start()

if __name__ == '__main__':
    main()
