import os
import cv2
import random
import torch
from load_model import load_model
from c.cConst import Const
from service.processing import build_targets
from service.frame_processor import frame_processor

# Khởi tạo các hằng số
var = Const()

def process_single_image(image_path, output_directory):
    """
    Xử lý một ảnh đơn lẻ để nhận dạng khuôn mặt và lưu ảnh đã xử lý.
    """
    print(f"Đang bắt đầu xử lý ảnh: {image_path}")
    
    # Tải mô hình
    detector, recognizer = load_model()
    targets = build_targets(detector, recognizer, var.faces_dir)
    colors = {name: (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)) 
              for _, name in targets}

    # Đọc ảnh
    img = cv2.imread(image_path)
    
    processed_img = frame_processor(
            img, detector, recognizer, targets, 
            colors, var, output_directory
        )
        # Lưu ảnh đã xử lý
    if processed_img is not None:
            filename = os.path.basename(image_path)
            output_path = os.path.join(output_directory, f"processed_{filename}")
            cv2.imwrite(output_path, processed_img)
            print(f"Ảnh đã xử lý đã được lưu tại: {output_path}")

def main():
    
    # Định nghĩa thư mục
    input_image_directory = var.input_images_dir  # Định nghĩa thư mục ảnh đầu vào trong Const
    output_image_directory = var.output_images_dir  # Định nghĩa thư mục ảnh đầu ra trong Const
    
    # Đảm bảo các thư mục tồn tại
    os.makedirs(input_image_directory, exist_ok=True)
    os.makedirs(output_image_directory, exist_ok=True)
    
    # Định nghĩa đường dẫn ảnh đầu vào (có thể là một tham số hoặc đường dẫn file đầu vào)
    input_image_path = os.path.join(input_image_directory, r"C:\Users\duong\OneDrive_duong\Desktop\Thi_giac_mt\Thi_giac_mt\input_images\class.jpg")  # Ví dụ ảnh

    # Xử lý ảnh
    process_single_image(input_image_path, output_image_directory)
    print("Chương trình đã kết thúc thành công.")

if __name__ == "__main__":
    main()
