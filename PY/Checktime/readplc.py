import time
import pymcprotocol 
import csv
import datetime

PLC_IP = "192.168.0.10"
PLC_PORT = 5000
count = "D23"
trigack = "D300"
cdh = "D308"
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

# while True:
#     try:
#         eck = mc.batchread_wordunits(trigack, 1)
#         ack = bin(eck[0])
#         print(ack[12])
        
#     except Exception as e:
#         print(f"Error during reading: {e}")
#         time.sleep(0.5)
#         break

rs = mc.batchread_wordunits(count, 1)
print(rs)

mc.close()
print("close socket")
time.sleep(0.3)



