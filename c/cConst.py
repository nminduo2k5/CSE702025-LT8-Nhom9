# c/cConst.py

import os

class Const:
    det_weight = './weights/det_10g.onnx'   #đường  link dẫn tới mô hình detec đã chuyển sang onnx
    rec_weight = "./weights/w600k_r50.onnx"  #đường  link dẫn tới mô hình rec
    similarity_thresh = 0.3 # ngưỡng nhận diện độ tương đồng >0.47 thì coi là giống
    confidence_thresh = 0.5  # ngưỡng phát hiện khuân mặt >0.7 coi như đấy là khuân mặt không có thì bỏ qua
    faces_dir = "./faces5/"  # tệp lưu trữ mặt đã đc xử lý
    input_images_dir = "./input_images/"   # ảnh đầu vào
    output_images_dir = "./output_images/"  # ảnh đầu ra
    max_num = 0  #số khuân mặt tối thiểu
    max_frame = 100
   