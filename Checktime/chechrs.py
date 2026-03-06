import time
import pymcprotocol 
import csv
import datetime
import time

PLC_IP = "192.168.0.10"
PLC_PORT = 5000
pc= "D180"
pd = "D160"
ph = "D170"
ctrig = "D23"


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
while True:
    try:
        trig = mc.batchread_wordunits(ctrig, 1)
        if trig[0] == 62:
            c = mc.batchread_wordunits(pc, 1)

            d = mc.batchread_wordunits(pd, 1)

            h = mc.batchread_wordunits(ph, 1)

            r1 = float(c[0])*100/float(d[0]) if d[0] != 0 else 'undefined'
            r2 = float(h[0])*100/float(d[0]) if d[0] != 0 else 'undefined'


            #print(f"C: {c[0]}, D: {d[0]}, H: {h[0]}, C/D: {c[0]/d[0] if d[0] != 0 else 'undefined'}, H/D: {h[0]/d[0] if d[0] != 0 else 'undefined'}")  
            print(f"C: {c[0]}, D: {d[0]}, H: {h[0]}, C/D: {r1 if d[0] != 0 else 'undefined'}, H/D: {r2 if d[0] != 0 else 'undefined'}")

            with open('datacdh4.csv', 'a', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow([c[0], d[0], h[0], r1 if d[0] != 0 else 'undefined', r2 if d[0] != 0 else 'undefined'])
            time.sleep(0.5)    
    except ValueError:
        print("Invalid input. Please enter integers separated by commas.")
        break  # Exit the loop if input is invalid

# with open('datacdh4.csv', 'a', newline='') as csvfile:
#             writer = csv.writer(csvfile)
#             writer.writerow(["C","D","H","C/D","H/D"])
            
            

mc.close()
print("close socket")
time.sleep(0.3)
