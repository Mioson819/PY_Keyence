from CognexNativePy import NativeInterface
import datetime

c1 = NativeInterface('192.168.0.101', 'admin', '')
c2 = NativeInterface('192.168.0.102', 'admin', '')


# Lấy các đối tượng điều khiển cho từng nhóm chức năng

ex_c1 = c1.execution_and_online
ex_c2 = c2.execution_and_online


file_job_c1 = c1.file_and_job
file_job_c2 = c2.file_and_job

start_time = datetime.datetime.now()

ex_c1.set_online(1)
ex_c2.set_online(1)


# Ví dụ 1: Tải một job (file cấu hình) lên camera
job_name_c1 = "2.80.job"
job_name_c2 = "2.80.job"
# Kiểm tra job hiện tại, nếu khác thì tải job mới
if file_job_c1.get_file() != job_name_c1:
# Đưa camera offline trước khi tải job
    if ex_c1.get_online() == 1:
        ex_c1.set_online(0)
        file_job_c1.load_file(job_name_c1)
        ex_c1.set_online(1)
        print(f"Đã tải job C1: {job_name_c1}")

print(file_job_c1.get_file())

elapse_time = (datetime.datetime.now() - start_time).total_seconds()
print(f"Thời gian tải job C1: {elapse_time} giây")

if file_job_c2.get_file() != job_name_c2:
    if ex_c2.get_online() == 1:
        ex_c2.set_online(0)
        file_job_c2.load_file(job_name_c2)
        ex_c2.set_online(1)
        print(f"Đã tải job C2: {job_name_c2}")

print(file_job_c2.get_file())

elapse_time = (datetime.datetime.now() - start_time).total_seconds()
print(f"Thời gian tải job C2: {elapse_time} giây")    


c1.close()
c2.close()


