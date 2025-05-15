import cv2
import numpy as np
import onnxruntime

from utils.helpers import norm_crop_image

__all__ = ["ArcFace"]

class ArcFace:
 def __init__(self, model_path: str = None, session=None) -> None:  # Hàm khởi tạo
    # Tham số:
    # - model_path: Đường dẫn tới file mô hình ONNX (nếu không có session truyền vào).
    # - session: Một phiên ONNX Runtime đã được tạo sẵn (nếu có).

    self.session = session  # Gán phiên ONNX Runtime (session) vào thuộc tính của đối tượng.
    self.input_mean = 127.5  # Giá trị trung bình dùng để chuẩn hóa đầu vào (mean normalization).
    self.input_std = 127.5  # Giá trị độ lệch chuẩn dùng để chuẩn hóa đầu vào (standard deviation normalization).
    self.taskname = "recognition"  # Gán tên tác vụ (nhiệm vụ) là "recognition".

    # Nếu session chưa được cung cấp, tạo một phiên ONNX Runtime mới:
    if session is None:
        self.session = onnxruntime.InferenceSession(
            model_path,  # Đường dẫn tới file mô hình ONNX.
            providers=["CUDAExecutionProvider", "CPUExecutionProvider"],  # Sử dụng GPU (CUDA) nếu có, nếu không thì CPU.
        )

    # Lấy cấu hình đầu vào từ mô hình ONNX:
    input_cfg = self.session.get_inputs()[0]  # Lấy cấu hình đầu vào đầu tiên (nếu mô hình có nhiều đầu vào).
    input_shape = input_cfg.shape  # Lấy hình dạng (shape) của đầu vào.

    input_name = input_cfg.name  # Lấy tên của đầu vào.
    self.input_size = tuple(input_shape[2:4][::-1])  # Lấy kích thước đầu vào (width, height) từ shape.
    self.input_shape = input_shape  # Lưu lại hình dạng đầu vào đầy đủ.

    # Lấy danh sách đầu ra từ mô hình ONNX:
    outputs = self.session.get_outputs()  # Lấy danh sách các đầu ra của mô hình.
    output_names = []  # Khởi tạo danh sách để lưu tên các đầu ra.
    for output in outputs:  # Duyệt qua từng đầu ra:
        output_names.append(output.name)  # Lấy tên của đầu ra và thêm vào danh sách.

    self.input_name = input_name  # Lưu lại tên của đầu vào.
    self.output_names = output_names  # Lưu lại danh sách tên của các đầu ra.

    # Đảm bảo mô hình chỉ có một đầu ra:
    assert len(self.output_names) == 1  # Nếu số lượng đầu ra không phải 1, chương trình sẽ báo lỗi.

    self.output_shape = outputs[0].shape  # Lấy hình dạng của đầu ra đầu tiên và lưu lại.


 def get_feat(self, images: np.ndarray) -> np.ndarray:#trích xuất đặc trưng (features) từ hình ảnh thông qua mô hình ONNX.
        if not isinstance(images, list):
            images = [images]

        input_size = self.input_size
        blob = cv2.dnn.blobFromImages(
            images,
            1.0 / self.input_std,
            input_size,
            (self.input_mean, self.input_mean, self.input_mean),
            swapRB=True
        )
        outputs = self.session.run(self.output_names, {self.input_name: blob})[0]
        return outputs

 def __call__(self, image, kps):
    # Hàm `__call__` cho phép đối tượng có thể được gọi như một hàm.
    # Tham số:
    # - image: Ảnh đầu vào (numpy array hoặc định dạng ảnh phù hợp).
    # - kps: Các điểm đặc trưng (keypoints) dùng để căn chỉnh ảnh.
        aligned_image = norm_crop_image(image, landmark=kps)
        embedding = self.get_feat(aligned_image).flatten()
        return embedding
