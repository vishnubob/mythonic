from time import time, sleep
from os import path, getcwd

start = time()
# launching pd
pd = Pd(nogui=False)
pd.Send(["test message", 1, 2, 3])

def Pd_hello(self, message):
    print "Pd called Pd_hello(%s)" % message

pd.Pd_hello = Pd_hello

sentexit = False
# running a bunch of stuff for up to 20 seconds
while time() - start < 20 and pd.Alive():
    if time() - start > 0.5 and not sentexit:
        pd.Send(["exit"])
        sentexit = True
    pd.Update()

