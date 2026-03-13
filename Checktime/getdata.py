import time
import pymcprotocol 
import csv
import datetime

PLC_IP = "192.168.0.10"
PLC_PORT = 8501
CDH = "D718"
stt = "T90"
# auto-py-to-exe

mc = pymcprotocol.Type3E()
while True:
    try:
        mc.connect(PLC_IP, PLC_PORT)
        print("Connected to PLC")
        break  # Exit the loop if connection is successful
    except Exception as e:
        print(f"Connection failed: {e}. Retrying...")
        time.sleep(0.3)  # Wait before retrying
        

time.sleep(0.1)
# Nhập thủ công các giá trị cho data_ng (mặc định 6 word units)
d1 = 0
d2 = 0
counter = 0
# while True:
#     data = mc.batchread_wordunits(CDH, 4)
#     if data[0] != d1 and data[2] != d2:
#         d1 = data[0]
#         d2 = data[2]
#         counter += 1
#         print(f"Current data at {CDH}: {data[0]}, {data[2]}")
#     if counter >= 20:
#         break
sttplc = mc.batchread_wordunits(stt, 1)
print(f"Current data at {stt}: {sttplc[0]}")

mc.close()
print("close socket")
time.sleep(0.3)



