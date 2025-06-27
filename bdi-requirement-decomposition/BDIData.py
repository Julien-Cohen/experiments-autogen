from asyncio import InvalidStateError

from dataclasses import dataclass

@dataclass
class BDIData:
    belief : list[str]
    desire : list[str]
    intention : str

    def __init__(self):
        self.belief = list()
        self.desire = list()
        self.reset_intention()



    def add_belief(self, data : str, tag : str):
        self.belief.insert(0, (data, tag)) # insert at head

    def update_belief(self, data:str, tag: str):
        found = False
        for i in range(len(self.belief)):
            (d,t) = self.belief[i]
            if t == tag :
                self.belief[i] = (data, t)
                found = True
        if not found:
            self.belief.append((data, tag))

    def get_belief_by_tag(self, tag):
        for (a,b) in self.belief:
            if tag == b :
                return a
        raise InvalidStateError

    def set_intention(self, i:str):
        self.intention = i


    def __str__(self):
        return (
                "BELIEF= " + str(self.belief) + "\n"
                "DESIRE= " + str(self.desire) + "\n"
                "INTENTION= " + str(self.intention) + "\n")

    def reset_intention(self):
        self.intention = ""