import os
import torch
import onnxruntime
from c.cConst import Const
from models.arcface import ArcFace
from models.scrfd import SCRFD
var = Const()

def load_model():
    # Sử dụng GPU với ONNX Runtime
    detector_session = onnxruntime.InferenceSession(var.det_weight, providers=['CUDAExecutionProvider'])
    recognizer_session = onnxruntime.InferenceSession(var.rec_weight, providers=['CUDAExecutionProvider'])
    
    detector = SCRFD(session=detector_session, model_path=var.det_weight, input_size=(640, 640), conf_thres=var.confidence_thresh)
    recognizer = ArcFace(session=recognizer_session)
    return detector, recognizer