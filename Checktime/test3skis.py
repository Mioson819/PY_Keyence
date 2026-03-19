from CognexNativePy import NativeInterface
import datetime

timenow = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")


cxp_socket = NativeInterface('192.168.0.23', 'admin', '')


img_cxp = cxp_socket.image.read_image()

with open(f'E:\Work\PY\imgcxp\img_cxp_{timenow}.bmp', 'wb') as f:
    f.write(img_cxp["data"])
    

cxp_socket.close()
