from asyncio import InvalidStateError

from dataclasses import dataclass


@dataclass
class Beliefs:
    _store: list[tuple[str, str]]

    def __init__(self):
        self._store = list()

    def add_belief(self, data: str, tag: str):
        self._store.insert(0, (data, tag))  # insert at head

    def update_belief(self, data: str, tag: str):
        found = False
        for i in range(len(self._store)):
            (d, t) = self._store[i]
            if t == tag:
                self._store[i] = (data, t)
                found = True
        if not found:
            self._store.append((data, tag))

    def get_belief_by_tag(self, tag):
        for a, b in self._store:
            if tag == b:
                return a
        raise InvalidStateError

    def __str__(self):
        return "BELIEF= " + str(self._store)


@dataclass
class Intention:
    intention: tuple[str, str]

    def __init__(self):
        self.clear()

    def set(self, action: str, data: str):
        self.intention = (action, data)

    def get_action(self):
        (a, b) = self.intention
        return a

    def get_data(self):
        (a, b) = self.intention
        return b

    def clear(self):
        self.intention = None

    def __str__(self):
        if self.intention is not None:
            (a, b) = self.intention
            return "INTENTION= " + a + " :: " + b
        else:
            return "INTENTION= _"


@dataclass
class Desires:
    _store: list[str]

    def __init__(self):
        self._store = list()

    def __str__(self):
        return "DESIRE= " + str(self._store)

    def add(self, d):
        self._store.append(d)
