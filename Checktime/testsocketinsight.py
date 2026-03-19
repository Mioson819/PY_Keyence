from CognexNativePy import NativeInterface

def main():
    try:
        # Tạo kết nối socket tới camera Cognex
        # Thay thế IP, username, password của bạn
        native_interface = NativeInterface('192.168.0.23', 'admin', '')
        
        # Lấy các đối tượng điều khiển cho từng nhóm chức năng
        execution = native_interface.execution_and_online
        file_job = native_interface.file_and_job
        image = native_interface.image
        settings = native_interface.settings_and_cells_values

        # Ví dụ 1: Tải một job (file cấu hình) lên camera
        job_name = "1.40.job"
        # Kiểm tra job hiện tại, nếu khác thì tải job mới
        # if file_job.get_file() != job_name:
        #     # Đưa camera offline trước khi tải job
        #     if execution.get_online() == 1:
        #         execution.set_online(0)
        #     file_job.load_file(job_name)
        #     print(f"Đã tải job: {job_name}")

        # Ví dụ 2: Đọc ảnh cuối cùng từ camera và lưu lại
        with open('captured_image.bmp', 'wb') as f:
            # Hàm read_image() trả về dict, dữ liệu ảnh nằm ở key "data"
            f.write(image.read_image()["data"])
        print("Đã lưu ảnh captured_image.bmp")

        # Ví dụ 3: Đọc và ghi giá trị từ ô trong bảng tính (spreadsheet)
        # Đọc giá trị ô B010
        # value_I1 = settings.get_value("I", 1)
        # print(f"Giá trị ô I1: {value_I1}")

        # Ghi giá trị 53 vào ô D019 (dạng số nguyên)
        #settings.set_integer_value("D", 19, 53)
        #print("Đã cập nhật ô D019")

        # Đóng kết nối socket
        native_interface.close()

    except Exception as e:
        print(f"Lỗi: {e}")

if __name__ == '__main__':
    main()