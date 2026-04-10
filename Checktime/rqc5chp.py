from socket import *
import socketplc
from socketplc import kvHostLink
import time

kv = kvHostLink("192.168.0.10")

rqc5 = 'MR46300'
rspc5 = 'TM104'

while True:
    rq = kv.read(rqc5)
    rs = kv.read(rspc5)
    if int(rq.decode(errors='ignore')) == 0 :
        kv.set(rqc5)
    time.sleep(2)