import string
import time
from socket import *
import struct
import datetime
import csv
from CognexNativePy import NativeInterface

#   https://qiita.com/OkitaSystemDesign/items/b8c19c313b7010e69ddf

BUFSIZE = 4096

class kvHostLink:
    addr = ()
    destfins = []
    srcfins = []
    port = 8501
    

    def __init__(self, host):
        self.addr = host, self.port

    def sendrecive(self, command):
        s = socket(AF_INET, SOCK_DGRAM)
        s.bind(('', self.port))
        s.settimeout(2)

        starttime = time.time()

        s.sendto(command, self.addr)
        #print("send:%r" % (command))
        rcvdata = s.recv(BUFSIZE)

        elapsedtime = time.time() - starttime
        #print ('receive: %r\t Length=%r\telapsedtime = %sms' % (rcvdata, len(rcvdata), str(elapsedtime * 1000)))
        #print()
        return rcvdata

    def mode(self, mode):
        senddata = 'M' + mode
        rcv = self.sendrecive((senddata + '\r').encode())
        return rcv

    def unittype(self):
        rcv = self.sendrecive("?k\r".encode())
        return rcv

    def errclr(self):
        senddata = 'ER'
        rcv = self.sendrecive((senddata + '\r').encode())
        return rcv

    def er(self):
        senddata = '?E'
        rcv = self.sendrecive((senddata + '\r').encode())
        return rcv

    def settime(self):
        dt_now = datetime.datetime.now()
        senddata = 'WRT ' + str(dt_now.year)[2:]
        senddata = senddata + ' ' + str(dt_now.month)
        senddata = senddata + ' ' + str(dt_now.day)
        senddata = senddata + ' ' + str(dt_now.hour)
        senddata = senddata + ' ' + str(dt_now.minute)
        senddata = senddata + ' ' + str(dt_now.second)
        senddata = senddata + ' ' + dt_now.strftime('%w')
        rcv = self.sendrecive((senddata + '\r').encode())
        return rcv
        
    def set(self, address):
        rcv = self.sendrecive(('ST ' + address + '\r').encode())
        return rcv

    def reset(self, address):
        rcv = self.sendrecive(('RS ' + address + '\r').encode())
        return rcv

    def sts(self, address, num):
        rcv = self.sendrecive(('STS ' + address + ' ' + str(num) + '\r').encode())
        return rcv

    def rss(self, address, num):
        rcv = self.sendrecive(('RSS ' + address + ' ' + str(num) + '\r').encode())
        
        return rcv

    def read(self, addresssuffix):
        rcv = self.sendrecive(('RD ' + addresssuffix + '\r').encode())
        
        return rcv

    def reads(self, addresssuffix, num):
        rcv = self.sendrecive(('RDS ' + addresssuffix + ' ' + str(num) + '\r').encode())
        
        return rcv

    def write(self, addresssuffix, data):
        rcv = self.sendrecive(('WR ' + addresssuffix + ' ' + data + '\r').encode())
        return rcv

    def writs(self, addresssuffix, num, data):
        rcv = self.sendrecive(('WRS ' + addresssuffix + ' ' + str(num) + ' ' + data + '\r').encode())
        
        return rcv


kv = kvHostLink('192.168.0.10')

cd_x = 'DM648'
cd_y = 'DM650'
cd_D = 'DM654'
cxp_X = 'DM718'
cxp_Y = 'DM720'
chp_Z = 'DM788'
rquld_p12 = 'MR13700'
ul_p12_done = 'TM134'
number_set = 'DM1850.U'
number_input = 'DM1852.U'
timenow = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
#cd_socket = NativeInterface('192.168.0.22', 'admin', '')
cxp_socket = NativeInterface('192.168.0.23', 'admin', '')
#chp_socket = NativeInterface('192.168.0.24', 'admin', '')

with open(f'datafix_{timenow}.csv', 'a', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow([f"{datetime.datetime.now()}: Start monitoring..."])
    writer.writerow(['Time', 'CD X', 'CD Y', 'CD D', 'CXP X', 'CXP Y', 'CHP Z'])
nb_set = kv.read(number_set)

while True:
    rq = kv.read(rquld_p12)
    timecheck = kv.read(ul_p12_done)
    nm_ip = kv.read(number_input)
    #print(f"RQUld P12: {rq.decode(errors='ignore')}, UL P12 Done: {int(timecheck.decode(errors='ignore'))}")
    if int(rq.decode(errors='ignore')) == 1 and int(timecheck.decode(errors='ignore')) == 2:
        print("RQUld P12 is 1 and UL P12 Done is 2")
        print(f"RQUld P12: {rq.decode(errors='ignore')}, UL P12 Done: {int(timecheck.decode(errors='ignore'))}")
        # Đọc giá trị từ DM648, DM650, DM654, DM718, DM720, DM788
        cd_x_value = kv.read(cd_x.L).decode(errors='ignore')
        cd_y_value = kv.read(cd_y.L).decode(errors='ignore')
        cd_D_value = kv.read(cd_D.L).decode(errors='ignore')
        cxp_X_value = kv.read(cxp_X.L).decode(errors='ignore')
        cxp_Y_value = kv.read(cxp_Y.L).decode(errors='ignore')
        chp_Z_value = kv.read(chp_Z.L).decode(errors='ignore')
        
        print(f"CD X: {cd_x_value}, CD Y: {cd_y_value}, CD D: {cd_D_value}, CXP X: {cxp_X_value}, CXP Y: {cxp_Y_value}, CHP Z: {chp_Z_value}")
        with open(f'datafix_{timenow}.csv', 'a', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([f"{datetime.datetime.now()}", int(cd_x_value), int(cd_y_value), int(cd_D_value), int(cxp_X_value), int(cxp_Y_value), int(chp_Z_value)])
        
        # img_cd = cd_socket.image.read_image()
        # with open(f'img_cd_{timenow}.bmp', 'wb') as f:
        #     f.write(img_cd["data"])
        img_cxp = cxp_socket.image.read_image()
        with open(f'E:\Work\PY\imgcxp\img_cxp_{timenow}.bmp', 'wb') as f:
            f.write(img_cxp["data"])
        # img_chp = chp_socket.image.read_image()
        # with open(f'img_chp_{timenow}.bmp', 'wb') as f:
        #     f.write(img_chp["data"])
        time.sleep(2)
        
    if int(nm_ip.decode(errors='ignore')) == int(nb_set.decode(errors='ignore')):
            #cd_socket.close()
            cxp_socket.close()
            #chp_socket.close()
            print("Conditions not met. Done...")
            time.sleep(1)
            break
