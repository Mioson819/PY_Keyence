import string
import time
from socket import *
import struct
import datetime
import csv
from CognexNativePy import NativeInterface

from socketplc import kvHostLink

kv = kvHostLink('192.168.0.10')

cd_x = 'DM648.L'
cd_y = 'DM650.L'
cd_D = 'DM654.L'
cxp_X = 'DM718.L'
cxp_Y = 'DM720.L'
chp_Z = 'DM788.L'
rquld_p12 = 'MR13700'
ul_p12_done = 'TM134'
number_set = 'DM1850'
number_input = 'DM1852'
timenow = datetime.datetime.now().strftime("%H-%M-%S-%d-%m-%y-")
#cd_socket = NativeInterface('192.168.0.22', 'admin', '')
#cxp_socket = NativeInterface('192.168.0.23', 'admin', '')
#chp_socket = NativeInterface('192.168.0.24', 'admin', '')


with open(f'datafix_{timenow}.csv', 'a', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow([f"{datetime.datetime.now().strftime('%H-%M-%S-%d-%m-%y-')}: Start monitoring..."])
    writer.writerow(['Time','STT', 'CD X', 'CD Y', 'CD D', 'CXP X', 'CXP Y', 'CHP Z'])


while True:
    rq = kv.read(rquld_p12)
    timecheck = kv.read(ul_p12_done)
    nb_set = kv.read(number_set)
    nm_ip = kv.read(number_input)
    #print(f"RQUld P12: {rq.decode(errors='ignore')}, UL P12 Done: {int(timecheck.decode(errors='ignore'))}")
    if int(rq.decode(errors='ignore')) == 1 and int(timecheck.decode(errors='ignore')) == 2:
    #if True:
        print(f"RQUld P12: {rq.decode(errors='ignore')}, UL P12 Done: {int(timecheck.decode(errors='ignore'))}")
        # Đọc giá trị từ DM648, DM650, DM654, DM718, DM720, DM788
        cd_x_value = kv.read(cd_x).decode(errors='ignore')
        cd_y_value = kv.read(cd_y).decode(errors='ignore')
        cd_D_value = kv.read(cd_D).decode(errors='ignore')
        cxp_X_value = kv.read(cxp_X).decode(errors='ignore')
        cxp_Y_value = kv.read(cxp_Y).decode(errors='ignore')
        chp_Z_value = kv.read(chp_Z).decode(errors='ignore')
        
        print(f"CD X: {int(cd_x_value)}, CD Y: {int(cd_y_value)}, CD D: {int(cd_D_value)}, CXP X: {int(cxp_X_value)}, CXP Y: {int(cxp_Y_value)}, CHP Z: {int(chp_Z_value)}")
        with open(f'datafix_{timenow}.csv', 'a', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([f"{datetime.datetime.now().strftime('%H-%M-%S-%d-%m-%y-')}",int(nm_ip.decode(errors='ignore')), int(cd_x_value), int(cd_y_value), int(cd_D_value), int(cxp_X_value), int(cxp_Y_value), int(chp_Z_value)])
        
        # img_cd = cd_socket.image.read_image()
        # with open(f'img_cd_{timenow}.bmp', 'wb') as f:
        #     f.write(img_cd["data"])
        # img_cxp = cxp_socket.image.read_image()
        # with open(f'E:/Work/PY/imgcxp/img_cxp_{timenow}.bmp', 'wb') as f:
        #     f.write(img_cxp["data"])
        # img_chp = chp_socket.image.read_image()
        # with open(f'img_chp_{timenow}.bmp', 'wb') as f:
        #     f.write(img_chp["data"])
        time.sleep(2)
        
    if int(nm_ip.decode(errors='ignore')) == int(nb_set.decode(errors='ignore')):
            #cd_socket.close()
            #cxp_socket.close()
            #chp_socket.close()
            print("Conditions not met. Done...")
            time.sleep(1)
            break
