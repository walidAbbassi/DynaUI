# -*- coding: utf-8 -*-

import os
import json

__all__ = ["Singleton", "BaseDict", "Do", "DoNothing"]


class Singleton(type):
    _instance = None

    def __call__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__call__(*args, **kwargs)
        return cls._instance


class BaseDict(object):
    def __init__(self):
        self.dict = {}
        self.filename = None

    def __setitem__(self, key, value):
        self.dict[key] = value

    def __getitem__(self, key):
        return self.dict[key]

    def __iter__(self):
        return self.dict.__iter__()

    def get(self, item):
        return self.dict.get(item)

    def Get(self, item, prefix="", suffix=""):
        try:
            return self.dict[prefix + item + suffix]
        except Exception:
            return item

    def Load(self, filename):
        if not os.path.exists(filename):
            with open(filename, "wb") as f:
                f.write(b"\x7b\x7d")
        with open(filename, "r", encoding="utf-8") as f:
            for key, value in json.load(f).items():
                if key in self.dict:
                    self.dict[key] = value
        self.filename = filename

    def Save(self):
        if self.filename is not None:
            with open(self.filename, "w", encoding="utf-8") as f:
                json.dump(self.dict, f)


def Do(func):
    if func:
        if isinstance(func, tuple):
            if isinstance(func[0], tuple):
                return [Do(f) for f in func]
            else:
                return func[0](*func[1:])
        return func()


def DoNothing(*args, **kwargs):
    pass
