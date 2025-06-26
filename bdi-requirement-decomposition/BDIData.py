from asyncio import InvalidStateError


class BDIData:
    context_belief = []
    desire = None
    intention = None

    def add_belief(self, data : str, tag : str):
        self.context_belief.insert(0, (data,tag) ) # insert at head

    def get_belief_by_tag(self, tag):
        for (a,b) in self.context_belief:
            if tag == b :
                return a
        raise InvalidStateError