import os
import pandas as pd
from datetime import datetime

def generate_csv_from_faces(detected_faces, output_directory, filename):
    if not detected_faces:
        print("No detected faces to save.")
        return

    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    faces_with_time = []
    for face in detected_faces:
        face_row = dict(face)
        face_row["Datetime"] = now_str
        face_row["Status"] = "Recognized" if face_row["Name"] != "Unknown" else "Unknown"
        faces_with_time.append(face_row)

    df_faces = pd.DataFrame(faces_with_time, columns=["Name", "Confidence", "Datetime", "Status"])

    total_faces = len(detected_faces)
    recognized_faces = sum(1 for face in detected_faces if face["Name"] != "Unknown")
    recognition_rate = (recognized_faces / total_faces) * 100 if total_faces > 0 else 0

    summary_row = {
        "Name": "SUMMARY",
        "Confidence": "",
        "Datetime": now_str,
        "Status": "",
        "Total Faces": total_faces,
        "Recognized Faces": recognized_faces,
        "Recognition Rate (%)": f"{recognition_rate:.2f}"
    }

    df_summary = pd.DataFrame([summary_row])

    df_result = pd.concat([df_faces, df_summary], ignore_index=True)
    df_result = df_result.fillna("")

    csv_path = os.path.join(output_directory, filename)
    df_result.to_csv(csv_path, index=False)
    print(f"Attendance saved to: {csv_path}")
