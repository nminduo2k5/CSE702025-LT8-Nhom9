import os
import cv2
import numpy as np
from typing import Union, List, Tuple

def build_targets(detector, recognizer, faces_dir) -> List[Tuple[np.ndarray, str]]:
    targets = []
    for foldername in os.listdir(faces_dir):
        name = foldername
        folder_path = os.path.join(faces_dir, foldername)
        
        for filename in os.listdir(folder_path):
            image_path = os.path.join(folder_path, filename)

            image = cv2.imread(image_path)
            if image is None:
                print(f"Failed to load image: {image_path}")
                continue

            bboxes, kpss = detector.detect(image, max_num=1)

            if len(kpss) == 0:
                # logging.warning(f"No face detected in {image_path}. Skipping...")
                continue

            embedding = recognizer(image, kpss[0])
            targets.append((embedding, name))

    return targets
