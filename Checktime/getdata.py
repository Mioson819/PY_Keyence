import time
from socket import *
import csv  
import datetime
from socketplc import kvHostLink

kv = kvHostLink('192.168.0.10')

con_trig = 'DM650'
count_trig = 'DM23'

c = 'D180.D'
d = 'D160.D'
h = 'D170.D'
time_now = datetime.datetime.now().strftime('%H-%M-%S-%d-%m-%y')
with open(f'CDH_Bottom_{time_now}.csv', 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([f"{time_now}"])    
        writer.writerow(['Time', 'C', 'D', 'H','C/D','H/D'])

con_trig_value = kv.read(con_trig).decode(errors='ignore')       

while True:

    count_trig_value = kv.read(count_trig).decode(errors='ignore')
    #print(f"Con Trig: {int(con_trig_value)}, Count Trig: {int(count_trig_value)}")
    if int(con_trig_value) == int(count_trig_value):
        time.sleep(0.15)  # Delay để đảm bảo giá trị đã được cập nhật
        c_value = kv.read(c).decode(errors='ignore')
        d_value = kv.read(d).decode(errors='ignore')
        h_value = kv.read(h).decode(errors='ignore')
        print(f"Con Trig: {int(con_trig_value)}, Count Trig: {int(count_trig_value)}, C: {float(c_value)}, D: {float(d_value)}, H: {float(h_value)}")
        with open(f'CDH_Bottom_{time_now}.csv', 'a', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([f"{datetime.datetime.now().strftime('%H-%M-%S-%d-%m-%y')}", float(c_value), float(d_value), float(h_value), float(c_value)/float(d_value)*100, float(h_value)/float(d_value)*100])
        time.sleep(1)  # Delay để tránh ghi quá nhanh vào file CSV
