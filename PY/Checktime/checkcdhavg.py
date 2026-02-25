import time
import pymcprotocol 

import csv
import datetime

PLC_IP = "192.168.0.10"
PLC_PORT = 5000
count = "D23"
resultcdh = "D308"
numbertrigger = "D550"
pointbreak = "D4002"

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

number = mc.batchread_wordunits(numbertrigger, 1)[0]
print(f"Number trigger: {number}")

start_time = None
rsc12  = []
rsd = []
rsh = []
avg_c12=0
avg_d=0
avg_h=0
i=0
countprd = 0
while True:
        try:
            #print("Reading PLC data...")
            counttrig = mc.batchread_wordunits(count, 1)
            cdh = mc.batchread_wordunits(resultcdh, 8)
            #print(f"Count: {result[0]}")
            current_value = counttrig[0] 
            # print(f"Current Value: {current_value}")
            
            if current_value == 1 and start_time is None:
                start_time = time.time()
                i+=1
                c1=cdh[0]
                c2=cdh[2]
                d = cdh[4]
                h = cdh[6]
                print(f"CDH: {c1},{c2},{d},{h}")
                rsc12.append(c1)
                rsc12.append(c2)
                rsd.append(d)
                rsh.append(h)
                with open('cdh_data.csv', mode='a', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow([current_value, c1, c2, d, h])

            if current_value > i:    
                c1=cdh[0]
                c2=cdh[2]
                d = cdh[4]
                h = cdh[6]
                print(f"CDH: {c1},{c2},{d},{h}")
                rsc12.append(c1)
                rsc12.append(c2)
                rsd.append(d)
                rsh.append(h)
                with open('cdh_data.csv', mode='a', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow([current_value, c1, c2, d, h])
                i+=1    
            if current_value == number:
                elapsed_time = time.time() - start_time
                print(f"Current value reached: {current_value}")
                countprd += 1
                print(f"countprd: {countprd})")
                print(f"Time elapsed: {elapsed_time:.2f} seconds")
                avg_c12 = sum(sorted(rsc12)[:10]) / 10 if len(rsc12) >= 10 else sum(rsc12) / len(rsc12)
                print(f"Average of 10 minimum values in rsc1: {avg_c12:.2f}")
                avg_d = sum(rsd) / len(rsd)
                print(f"Average of all values in rsd: {avg_d:.2f}")
                avg_h = sum(rsh) / len(rsh)
                print(f"Average of all values in rsh: {avg_h:.2f}")
                print(f"Ratios: {avg_c12*100/avg_d:.2f}, {avg_h*100/avg_d:.2f}")
                with open('cdh_data.csv', mode='a', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow([f"Time elapsed: {elapsed_time:.2f} seconds", f"Average of 10 minimum values in C: {avg_c12:.2f}", f"Average of all values in D: {avg_d:.2f}", f"Average of all values in H: {avg_h:.2f}", f"C/D,H/D: {avg_c12*100/avg_d:.2f}, {avg_h*100/avg_d:.2f}"])
                    writer.writerow("Next PRD")
            pointbreak_value = mc.batchread_wordunits(pointbreak, 1)
            if pointbreak_value[0] == 0:
                break  
                
            
            
        except Exception as e:
            print(f"Read error: {e}")
            time.sleep(0.1)
            break

               


mc.close()
print("close socket")
time.sleep(0.3)
