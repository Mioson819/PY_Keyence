import time
import pymcprotocol 
import csv
import datetime
import time

PLC_IP = "192.168.0.10"
PLC_PORT = 5000
rqtrig = "D350"
cdh = "D308"
first = "M0"

# auto-py-to-exee 

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


def read_plc_data_cdh(mc, rqtrig, cdh):

    while True:
        try:
            mc.batchwrite_wordunits(rqtrig, [3])
            time.sleep(0.2)
            cdhdata = mc.batchread_wordunits(cdh,8)
            c1=cdhdata[0]
            c2=cdhdata[2]
            d = cdhdata[4]
            h = cdhdata[6]
            #print(f"CDH:  {c1},{c2},{d},{h}")
            mc.batchwrite_wordunits(rqtrig, [1])
            time.sleep(0.1)
            return c1, c2, d, h
            
        except Exception as e:
            print(f"Read error: {e}")
            time.sleep(0.1)
count = 0
number_check = 0
number_check_sum= 0
numbertrig_pertime = 0

# Bật đèn bakclight bit MR512

while True:
    try:
        x = 6*16
        m5 = mc.batchread_bitunits(first,x)
        y=5*16+12
        print(m5[y])
        #break
        if m5[y]==0:
            m5[y]=1
            print("Light OFF")
            mc.batchwrite_bitunits(first,m5)
            print("Waiting for light to turn ON...")
            break
        else:
            print("Light ON")
            break
        
    except Exception as e:
        print(f"Error during reading M5: {e}")
        time.sleep(0.5)
        break
print("Nhập số lần Trigger cần thực hiện mỗi lần Check: ")
numbertrig_pertime = int(input())
print("Nhập số lần Check cần thực hiện")
number_check_sum = int(input())
print(f"Sẽ thực hiện {number_check_sum} lần Check, mỗi Check Trigger {numbertrig_pertime} lần")


with open('datacdh3.csv', 'a', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["STT","C1","C2","D","H","C1/D","C2/D","H/D"])
            
            
while True:
    try:
        resultcdh = read_plc_data_cdh(mc, rqtrig, cdh)
        with open('datacdh3.csv', 'a', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([count, resultcdh[0], resultcdh[1], resultcdh[2], resultcdh[3], resultcdh[0]/resultcdh[2] if resultcdh[2] != 0 else 0, resultcdh[1]/resultcdh[2] if resultcdh[2] != 0 else 0, resultcdh[3]/resultcdh[2] if resultcdh[2] != 0 else 0])
        print([count, resultcdh[0], resultcdh[1], resultcdh[2], resultcdh[3], resultcdh[0]/resultcdh[2] if resultcdh[2] != 0 else 0, resultcdh[1]/resultcdh[2] if resultcdh[2] != 0 else 0, resultcdh[3]/resultcdh[2] if resultcdh[2] != 0 else 0])
        count += 1
        #print(f"Recorded {count} entries")
        if count >= numbertrig_pertime:
            with open('datacdh3.csv', 'a', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow([f"Checkpoint {number_check} completed"])
            print(f"Check {number_check} Completed")
            count = 0
            number_check += 1
        if number_check >= number_check_sum:
            break
        time.sleep(0.1)      
    except Exception as e:
        print(f"Error during reading: {e}")
        time.sleep(0.5)
        

mc.close()
print("close socket")
time.sleep(0.3)
