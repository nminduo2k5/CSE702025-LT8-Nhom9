import cv2
import numpy as np
from models import SCRFD, ArcFace
from utils.helpers import compute_similarity, draw_bbox_info, draw_bbox

def frame_processor(
    frame: np.ndarray,
    detector: SCRFD,
    recognizer: ArcFace,
    targets: list,
    colors: dict,
    var,
    detected_faces=None
) -> np.ndarray:
    """Phát hiện và nhận diện khuôn mặt từ ảnh đầu vào."""
    
    # Phát hiện các bounding boxes và keypoints từ SCRFD (detector)
    bboxes, kpss = detector.detect(frame, var.max_num)
    
    for bbox, kps in zip(bboxes, kpss):
        *bbox, conf_score = bbox.astype(np.int32)

        # Trích xuất embedding (đặc trưng khuôn mặt) từ ArcFace (recognizer)
        embedding = recognizer(frame, kps)

        # Khởi tạo các giá trị tương tự và tên khuôn mặt tốt nhất
        max_similarity = 0
        best_match_name = "Unknown"

        # So sánh embedding với các đặc trưng đã biết để nhận diện khuôn mặt
        for target, name in targets:
            similarity = compute_similarity(target, embedding)
            
            if similarity > max_similarity and similarity > var.similarity_thresh:
                max_similarity = similarity
                best_match_name = name

        # Nếu có phát hiện khuôn mặt và nhận diện được, vẽ bounding box và tên khuôn mặt
        if best_match_name != "Unknown":
            color = colors[best_match_name]
            draw_bbox_info(frame, bbox, similarity=max_similarity, name=best_match_name, color=color)
            
            # Collect detected face information for statistics
            if detected_faces is not None:
                detected_faces.append({
                    "Name": best_match_name,
                    "Confidence": max_similarity
                })
    return frame
