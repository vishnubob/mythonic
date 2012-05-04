class Schedule(object):

    def __init__(self, initial_insertion_point=0):
        self._entries = {}
        self.initial_insertion_point = initial_insertion_point

    def get_insertion_point(self):
        "When append will schedule events"
        if len(self._entries.keys()) > 0:
            return max(self._entries.keys())
        else:
            return self.initial_insertion_point
    insertion_point = property(get_insertion_point)

    def schedule(self, f, when):
        #print "schedule(self, {0} {1})".format(f, when)
        entries = self._entries
        if when not in entries:
            entries[when] = []
        entries[when].append(f)

    def append(self, f, offset=0):
        entries = self._entries
        self.schedule(f, self.insertion_point + offset)

    def pop_due(self, n, when):
        entries = self._entries
        due = []

        for i in range(n):
            if len(entries.keys()) == 0:
                return due

            soonest = min(entries.keys())
            if soonest <= when:
                due.append(entries[soonest].pop())

                if len(entries[soonest]) == 0:
                    del entries[soonest]

        return due
