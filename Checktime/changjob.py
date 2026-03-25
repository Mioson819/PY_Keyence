from CognexNativePy import NativeInterface
import datetime

cp = NativeInterface('192.168.0.20', 'admin', '')
cf = NativeInterface('192.168.0.21', 'admin', '')
cd = NativeInterface('192.168.0.22', 'admin', '')
cxp = NativeInterface('192.168.0.23', 'admin', '')
cu = NativeInterface('192.168.0.25', 'admin', '')

# Lấy các đối tượng điều khiển cho từng nhóm chức năng

ex_cp = cp.execution_and_online
ex_cf = cf.execution_and_online
ex_cd = cd.execution_and_online
ex_cxp = cxp.execution_and_online
ex_cu = cu.execution_and_online

file_job_cp = cp.file_and_job
file_job_cf = cf.file_and_job
file_job_cd = cd.file_and_job
file_job_cxp = cxp.file_and_job
file_job_cu = cu.file_and_job

start_time = datetime.datetime.now()

ex_cp.set_online(1)
ex_cf.set_online(1)
ex_cd.set_online(1)
ex_cxp.set_online(1)
ex_cu.set_online(1)


# Ví dụ 1: Tải một job (file cấu hình) lên camera
job_name = "1.45.job"
# Kiểm tra job hiện tại, nếu khác thì tải job mới
if file_job_cp.get_file() != job_name:
# Đưa camera offline trước khi tải job
    if ex_cp.get_online() == 1:
        ex_cp.set_online(0)
        file_job_cp.load_file(job_name)
        ex_cp.set_online(1)
        print(f"Đã tải job CP: {job_name}")

print(file_job_cp.get_file())

elapse_time = (datetime.datetime.now() - start_time).total_seconds()
print(f"Thời gian tải job CP: {elapse_time} giây")

if file_job_cf.get_file() != job_name:
    if ex_cf.get_online() == 1:
        ex_cf.set_online(0)
        file_job_cf.load_file(job_name)
        ex_cf.set_online(1)
        print(f"Đã tải job CF: {job_name}")
        
print(file_job_cf.get_file())
        
elapse_time = (datetime.datetime.now() - start_time).total_seconds()
print(f"Thời gian tải job CF: {elapse_time} giây")    

if file_job_cd.get_file() != job_name:
    if ex_cd.get_online() == 1:
        ex_cd.set_online(0)
        file_job_cd.load_file(job_name)
        ex_cd.set_online(1)
        print(f"Đã tải job CD: {job_name}")

print(file_job_cd.get_file())
    
elapse_time = (datetime.datetime.now() - start_time).total_seconds()
print(f"Thời gian tải job CD: {elapse_time} giây")

if file_job_cxp.get_file() != job_name:
    if ex_cxp.get_online() == 1:
        ex_cxp.set_online(0)
        file_job_cxp.load_file(job_name)
        ex_cxp.set_online(1)
        print(f"Đã tải job CXP: {job_name}")

print(file_job_cxp.get_file())
        
elapse_time = (datetime.datetime.now() - start_time).total_seconds()
print(f"Thời gian tải job CXP: {elapse_time} giây")        
   
if file_job_cu.get_file() != job_name:
    if ex_cu.get_online() == 1:
        ex_cu.set_online(0)
        file_job_cu.load_file(job_name)
        ex_cu.set_online(1)
        print(f"Đã tải job CU: {job_name}")

print(file_job_cu.get_file())
        
elapse_time = (datetime.datetime.now() - start_time).total_seconds()
print(f"Thời gian tải job CU: {elapse_time} giây")   

cp.close()
cf.close()
cd.close()
cxp.close()
cu.close()

