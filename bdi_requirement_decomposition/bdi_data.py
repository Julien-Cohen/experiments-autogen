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
        return None

    def __str__(self):
        return "BELIEF= " + str(self._store)


@dataclass
class Intentions:
    _store: list[tuple[str, str]]

    def __init__(self):
        self._store = list()

    def add(self, action: str, data: str):
        self._store.append((action, data))

    def has_intention(self, tag):
        # exists
        for a, b in self._store:
            if a is tag:
                return True
        return False

    def get_intention_data(self, tag):
        for a, b in self._store:
            if a is tag:
                return b
        return None

    def remove_intention(self, a, d):
        self._store.remove((a, d))

    def remove_first_intention(self, a):
        self.remove_intention(a, self.get_intention_data(a))

    def __str__(self):
        if self._store is not None:
            return "INTENTIONS= " + str(self._store)
        else:
            return "INTENTIONS= _"


@dataclass
class Desires:
    _store: list[str]

    def __init__(self):
        self._store = list()

    def __str__(self):
        return "DESIRE= " + str(self._store)

    def add(self, d):
        self._store.append(d)
