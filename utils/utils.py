import os
import json
import time

# Hàm để xóa các tên đã quá hạn 1 phút trong file JSON
def remove_expired_names(path_logs):
    json_file = path_logs + "/face_logs.json"
    if not os.path.exists(json_file):
        return

    with open(json_file, "r") as f:
        data = json.load(f)

    current_time = time.time()
    # Lọc ra những tên đã lưu quá 1 phút
    data = {k: v for k, v in data.items() if current_time - v["added_time"] <= 60}

    # Ghi lại dữ liệu đã cập nhật vào file JSON
    with open(json_file, "w") as f:
        json.dump(data, f)

def count_directories_and_files(directory):
    num_subdirs = 0
    num_files = 0
    for root, dirs, files in os.walk(directory):
        num_subdirs += len(dirs)
        num_files += len(files)
    return num_subdirs, num_files