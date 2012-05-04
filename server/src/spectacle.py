from schedule import Schedule


class Spectacle(list):
    "Something spectacular, relayed via a timed sequence of function calls"

class Repeat(Spectacle):
    "Repeat at even intravals based on duration and reps"

    __slots__ = ["duration", "repetitions", "display_func"]

    def __init__(self, display_func, duration, repetitions):
        "Inserts tuples of time offsets and function calls"
        plan = []
        t = 0
        for i in range(repetitions):
            plan.append(tuple([t, display_func]))
            t = t + duration/float(repetitions)
        super(Spectacle, self).__init__(plan)


class SpectacleSchedule(Schedule):
    "Schedular but with call supporting the scheduling of spectacle"

    def append_spectacle(self, spectacle):
        for offset, f in spectacle:
            self.schedule(f, self.insertion_point + offset)
