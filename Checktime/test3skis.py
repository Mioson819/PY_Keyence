from CognexNativePy import NativeInterface
import datetime

timenow = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")


cxp_socket = NativeInterface('192.168.0.21', 'admin', '')

start_time = datetime.datetime.now()
img_cxp = cxp_socket.image.read_bmp()
end1_time = datetime.datetime.now()
elapsed1_time = (end1_time - start_time).total_seconds()
print(f"Elapsed time for reading image: {elapsed1_time} seconds")

with open(f'E:/Work/PY/imgcxp/img_cxp_{timenow}.bmp', 'wb') as f:
    f.write(img_cxp["data"])
    
end_time = datetime.datetime.now()
elapsed_time = (end_time - start_time).total_seconds()
print(f"Elapsed time: {elapsed_time} seconds")

cxp_socket.close()
