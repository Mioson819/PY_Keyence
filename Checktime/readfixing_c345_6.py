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

cu_ok_ng = 'DM858.L'
cu_pot = 'DM860.L'
cu_gap_min  = 'DM862.L'
cu_gap_max = 'DM864.L'
rq_trig_cu = 'MR46600'
cu_done = 'TM105'

number_set = 'DM1850'
number_input = 'DM1852'
timenow = datetime.datetime.now().strftime("%H-%M-%S-%d-%m-%y-")


with open(f'datafix_C345{timenow}.csv', 'a', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow([f"{datetime.datetime.now().strftime('%H-%M-%S-%d-%m-%y-')}: Start monitoring..."])
    writer.writerow(['Time','STT', 'CD X', 'CD Y', 'CD D', 'CXP X', 'CXP Y', 'CHP Z'])

with open(f'datafix_C6_{timenow}.csv', 'a', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow([f"{datetime.datetime.now().strftime('%H-%M-%S-%d-%m-%y-')}: Start monitoring..."])
    writer.writerow(['Time','STT', 'CU OK/NG', 'CU Pot', 'CU Gap Min', 'CU Gap Max'])

countc345 = 0
countc6 = 0
while True:
    rq = kv.read(rquld_p12)
    timecheck = kv.read(ul_p12_done)
    nb_set = kv.read(number_set)
    nb_ip = kv.read(number_input)
    #print(f"RQUld P12: {rq.decode(errors='ignore')}, UL P12 Done: {int(timecheck.decode(errors='ignore'))}")
    if int(rq.decode(errors='ignore')) == 1 and int(timecheck.decode(errors='ignore')) == 2 and countc345 < int(nb_set.decode(errors='ignore')):
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
        with open(f'datafix_C345{timenow}.csv', 'a', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([f"{datetime.datetime.now().strftime('%H-%M-%S-%d-%m-%y-')}",int(nb_ip.decode(errors='ignore')), int(cd_x_value), int(cd_y_value), int(cd_D_value), int(cxp_X_value), int(cxp_Y_value), int(chp_Z_value)])
        
        countc345 += 1
        
    rqcu =kv.read(rq_trig_cu)
    cu_done_value = kv.read(cu_done)
    if int(rqcu.decode(errors='ignore')) == 1:
        time.sleep(0.8)
        print(f"RQUld AFL4: {rqcu.decode(errors='ignore')}, CU Done: {int(cu_done_value.decode(errors='ignore'))}")
        cu_ok_ng_value = kv.read(cu_ok_ng).decode(errors='ignore')
        cu_pot_value = kv.read(cu_pot).decode(errors='ignore')
        cu_gap_min_value = kv.read(cu_gap_min).decode(errors='ignore')
        cu_gap_max_value = kv.read(cu_gap_max).decode(errors='ignore')
        print(f"CU OK/NG: {int(cu_ok_ng_value)}, CU Pot: {int(cu_pot_value)}, CU Gap Min: {int(cu_gap_min_value)}, CU Gap Max: {int(cu_gap_max_value)}")
        with open(f'datafix_C6_{timenow}.csv', 'a', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([f"{datetime.datetime.now().strftime('%H-%M-%S-%d-%m-%y-')}", countc6, int(cu_ok_ng_value), int(cu_pot_value), int(cu_gap_min_value), int(cu_gap_max_value)])
        countc6 += 1
        
            
     
         
       
    if countc6 == int(nb_set.decode(errors='ignore')):

        print("Conditions not met. Done...")
        time.sleep(1)
        break
