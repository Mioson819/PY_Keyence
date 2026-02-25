import time
import pymcprotocol 
import csv
import datetime

PLC_IP = "192.168.0.10"
PLC_PORT = 5000
CDH = "D308"

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

while True:
    # Chọn PL theo loại nhập và gán vào NG (được dùng phía dưới)
    while True:
        loai = input("Nhap Phan loai da (NG/B/I/J): ").strip().upper()
        if loai == 'NG':
            PL = "D620"
            expected_len = 4
            break
        elif loai == 'B':
            PL = "D624"
            expected_len = 8
            break
        elif loai == 'I':
            PL = "D632"
            expected_len = 8
            break
        elif loai == 'J':
            PL = "D640"
            expected_len = 4
            break
        else:
            print("Không hợp lệ. Vui lòng nhập NG, B, I hoặc J.")
    NG = PL
    s = input(f"Nhap {expected_len} gia tri cho data (cach nhau bang dau phay): ")
    parts = [p.strip() for p in s.split(',') if p.strip()]

    data_ng = []
    for p in parts:
        try:
            # hỗ trợ số nguyên thập phân và hex (ví dụ 0x1A)
            val = int(p, 0)
        except ValueError:
            try:
                val = int(float(p))
            except ValueError:
                val = 0
        data_ng.append(val)

    # Đảm bảo đúng độ dài (cắt bớt hoặc điền 0 nếu cần)
    if len(data_ng) < expected_len:
        data_ng += [0] * (expected_len - len(data_ng))
    elif len(data_ng) > expected_len:
        data_ng = data_ng[:expected_len]

    #print("data_ng nhap tay =", data_ng)
    time.sleep(0.1)
    
    data_c = mc.batchread_wordunits(CDH, 6)
    #data_ng_plc = mc.batchread_wordunits(NG, expected_len) 
    #print("data_ng_plc: ", data_ng_plc)

    mc.batchwrite_wordunits(NG, data_ng)

    data_ng_plc = mc.batchread_wordunits(NG, expected_len)
    print("C:", data_c)
    data_c[0] = round(data_c[0] / 1000, 3)
    data_c[2] = round(data_c[2] / 1000, 3)
    data_c[4] = round(data_c[4] / 1000, 3)
    print("data_ng: ", data_ng_plc)
    time.sleep(0.1)

    #current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
    #print("Time:", current_time)
    
    with open('data.csv', 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([data_c[0], data_c[2], data_c[4]])  # Write data
    # Quit loop when 'q' is pressed (works on Windows)
    #print("Time:", current_time)
    cmd = input("Nhập 'q' + Enter để thoát, Enter để tiếp tục: ").strip().lower()
    if cmd == 'q':
        print("Exiting loop.")
        break

mc.close()
print("close socket")
time.sleep(0.3)



