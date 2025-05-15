import threading
import queue
import time
import os
import cv2
import random
import torch
import pandas as pd 
import matplotlib.pyplot as plt
from pymongo import MongoClient
from load_model import load_model
from c.cConst import Const
from service.processing import build_targets
from service.frame_processor import frame_processor

from utils.save_log import Logger_Days, Logger_maxBytes
from utils.utils import count_directories_and_files
from utils.process_db import connect_to_mongo
# from c.bot_telegram import TelegramNotificationBot  # Uncomment if needed
import asyncio
import msvcrt  # For detecting keypresses on Windows

# Initialize constants and logging
var = Const()

def monitor_directory(directory, queue_embeddings, stop_event, logger):
    """
    Monitors directory for changes in number of files/folders using threading.
    """
    path_logs = "./logs/directory_monitor"
    os.makedirs(path_logs, exist_ok=True)
    file_name = os.path.join(path_logs, "logs_directory_changes.log")  # Ensure '.log' extension

    initial_folders, initial_files = count_directories_and_files(directory)
    logger.info(f"Initial state - Folders: {initial_folders}, Files: {initial_files}")

    while not stop_event.is_set():
        current_folders, current_files = count_directories_and_files(directory)
        
        if initial_folders != current_folders or initial_files != current_files:
            logger.info("Directory change detected!")
            logger.info(f"Previous state - Folders: {initial_folders}, Files: {initial_files}")
            logger.info(f"Current state - Folders: {current_folders}, Files: {current_files}")

            try:
                logger.info("Starting model reload and target building process...")
                
                detector, recognizer = load_model()
                logger.info("Model loaded successfully")
                
                targets = build_targets(detector, recognizer, directory)
                logger.info(f"Built targets successfully. Total targets: {len(targets)}")
                
                # Add new targets to queue
                queue_embeddings.put(targets)
                logger.info("New targets added to queue")

                # Release memory
                del detector, recognizer
                torch.cuda.empty_cache()
                logger.info("GPU memory cleared")

            except Exception as e:
                logger.error(f"Error in embedding update process: {str(e)}")
            
            # Update initial state
            initial_folders, initial_files = current_folders, current_files
        
        # Sleep to prevent high CPU usage
        time.sleep(5)

def monitor_images(input_directory, queue_images, stop_event, logger):
    """
    Monitors the input directory for new images and enqueues their paths for processing.
    """
    logger.info(f"Starting image monitor for directory: {input_directory}")
    path_logs = "./logs/image_monitor"
    os.makedirs(path_logs, exist_ok=True)
    file_name = os.path.join(path_logs, "logs_image_monitor.log")  # Ensure '.log' extension

    processed_files = set()

    while not stop_event.is_set():
        try:
            # List all files in the input directory
            for filename in os.listdir(input_directory):
                filepath = os.path.join(input_directory, filename)
                if filepath not in processed_files and os.path.isfile(filepath):
                    # Optionally, filter for specific image extensions
                    if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
                        logger.info(f"New image detected: {filename}")
                        queue_images.put(filepath)
                        processed_files.add(filepath)
        except Exception as e:
            logger.error(f"Error in image monitor: {str(e)}")
        
        # Sleep before next scan
        time.sleep(5)

def process_images(queue_embeddings, queue_images, output_directory, logger, stop_event):
    """
    Processes images from the queue: performs face recognition and saves processed images,
    then creates a results table.
    """
    logger.info("Starting image processing thread...")
    
    # Initialize MongoDB collection
    collection = connect_to_mongo(logger)
    
    # Load models initially
    detector, recognizer = load_model()
    targets = build_targets(detector, recognizer, var.faces_dir)
    colors = {name: (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)) 
              for _, name in targets}

    while not stop_event.is_set():
        try:
            # Update targets if there are updates in the embeddings queue
            if not queue_embeddings.empty():
                logger.info("Updating targets from embeddings queue")
                new_targets = queue_embeddings.get_nowait()
                targets = new_targets
                colors = {name: (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)) 
                          for _, name in targets}
                logger.info(f"Updated targets. Total targets: {len(targets)}")
                
                # Optionally, release and reload models
                del detector, recognizer
                torch.cuda.empty_cache()
                logger.info("Released previous models and cleared GPU memory")
                
                detector, recognizer = load_model()
                logger.info("Reloaded models successfully")

            # Process images from queue
            if not queue_images.empty():
                image_path = queue_images.get_nowait()
                logger.info(f"Processing image: {image_path}")
                
                # Read image
                img = cv2.imread(image_path)
                if img is None:
                    logger.error(f"Failed to read image: {image_path}")
                    continue
                
                # Detect faces in the image to get the total number of faces
                total_faces_bboxes, _ = detector.detect(img, var.max_num)
                total_faces = len(total_faces_bboxes)  # Total faces in the image

                # Process image and collect results
                detected_faces = []  # List to store detection results
                try:
                    processed_img = frame_processor(
                        img, detector, recognizer, targets, 
                        colors, collection, var, "image_processor", logger, output_directory, queue_images,
                        detected_faces=detected_faces  # Pass detected_faces to collect results
                    )
                    # Save processed image
                    if processed_img is not None:
                        filename = os.path.basename(image_path)
                        output_path = os.path.join(output_directory, f"processed_{filename}")
                        cv2.imwrite(output_path, processed_img)
                        logger.info(f"Processed image saved to: {output_path}")

                        # Calculate and log recognition statistics
                        detected_faces_count = len(detected_faces)  # Detected faces
                        recognized_faces = sum(1 for face in detected_faces if face["Name"] != "Unknown")
                        recognition_rate = (recognized_faces / detected_faces_count) * 100 if detected_faces_count > 0 else 0

                        # Calculate average recognition score for recognized faces
                        if recognized_faces > 0:
                            avg_recognition_score = sum(face["Confidence"] for face in detected_faces if face["Name"] != "Unknown") / recognized_faces
                        else:
                            avg_recognition_score = 0

                        # Generate statistics table from detected_faces
                        if detected_faces:
                            df_faces = pd.DataFrame(detected_faces, columns=["Name", "Confidence"])

                            summary_data = {
                                "Name": ["Summary"],
                                "Confidence": [""],
                                "Total Faces": [total_faces],
                                "Detected Faces": [detected_faces_count],
                                "Recognized Faces": [recognized_faces],
                                "Recognition Rate (%)": [recognition_rate],
                                "Average Recognition Score": [avg_recognition_score]
                            }
                            df_summary = pd.DataFrame(summary_data)

                            df_faces = pd.concat([df_faces, df_summary], ignore_index=True)

                            csv_path = os.path.join(output_directory, f"statistics_{filename}.csv")
                            df_faces.to_csv(csv_path, index=False)
                            logger.info(f"Statistics saved to: {csv_path}")
                            print(df_faces)  # Optional: Display the table in the console

                            # Plot detailed recognition rate chart
                            plt.figure(figsize=(12, 8))
                            names = df_faces["Name"].value_counts().index.tolist()
                            counts = df_faces["Name"].value_counts().values.tolist()

                            # Exclude the summary row from the chart
                            names.pop(-1)
                            counts.pop(-1)

                            plt.bar(names, counts, color=['green' if name != "Unknown" else 'red' for name in names])
                            plt.xlabel('Names')
                            plt.ylabel('Number of Recognitions')
                            plt.title('Detailed Face Recognition Rate')
                            plt.xticks(rotation=45)
                            plt.tight_layout()
                            plt.savefig(os.path.join(output_directory, f"detailed_recognition_rate_{filename}.png"))
                            plt.close()

                        logger.info(f"Số mặt nhận diện: {recognized_faces}, Tổng số mặt: {total_faces}, Tỉ lệ nhận diện: {recognition_rate:.2f}%, Điểm nhận diện trung bình: {avg_recognition_score:.2f}")
                        print(f"Số mặt nhận diện: {recognized_faces}, Tổng số mặt: {total_faces}, Tỉ lệ nhận diện: {recognition_rate:.2f}%, Điểm nhận diện trung bình: {avg_recognition_score:.2f}")
                except Exception as e:
                    logger.error(f"Error processing image {image_path}: {str(e)}")
            
            # Small sleep to prevent high CPU usage
            time.sleep(0.1)
        
        except queue.Empty:
            pass
        except Exception as e:
            logger.error(f"Unexpected error in image processing thread: {str(e)}")
    
    # Cleanup
    del detector, recognizer
    torch.cuda.empty_cache()
    logger.info("Image processing thread stopped and models released.")
    
def image_keyboard_listener(stop_event):
    """
    Listens for the 'q' keypress to signal threads to stop.
    """
    print("Press 'q' to exit the application.")
    while not stop_event.is_set():
        if msvcrt.kbhit():
            key = msvcrt.getch()
            if key.lower() == b'q':
                print("Exit signal received. Shutting down...")
                stop_event.set()
        time.sleep(0.1)  # Slight delay to prevent high CPU usage

# def run_telegram_bot(queue_faces):
#     """
#     Telegram bot running in a separate thread
#     """
#     # ... existing Telegram bot code ...
#     pass

def main():
    # Setup centralized logging
    log_file = os.path.join("./logs", "app.log")
    logger = Logger_Days(log_file)  # Initialize Logger_Days with UTF-8 encoding
    
    # Define directories
    embedding_directory = var.faces_dir  # Directory to monitor for embedding updates
    input_image_directory = var.input_images_dir  # Define this in Const
    output_image_directory = var.output_images_dir  # Define this in Const
    
    # Ensure input and output directories exist
    os.makedirs(input_image_directory, exist_ok=True)
    os.makedirs(output_image_directory, exist_ok=True)
    
    # Create queues for inter-thread communication
    queue_embeddings = queue.Queue()
    queue_images = queue.Queue()

    # Create a stop event for graceful shutdown
    stop_event = threading.Event()

    # Create and start threads
    monitor_embedding_thread = threading.Thread(
        target=monitor_directory, 
        args=(embedding_directory, queue_embeddings, stop_event, logger), 
        daemon=True,
        name='MonitorEmbeddingThread'  # Optional: Assign a name for easier debugging
    )
    
    monitor_image_thread = threading.Thread(
        target=monitor_images, 
        args=(input_image_directory, queue_images, stop_event, logger), 
        daemon=True,
        name='MonitorImageThread'  # Optional: Assign a name for easier debugging
    )
    
    image_processing_thread = threading.Thread(
        target=process_images, 
        args=(queue_embeddings, queue_images, output_image_directory, logger, stop_event), 
        daemon=True,
        name='ImageProcessingThread'  # Optional: Assign a name for easier debugging
    )
    
    keyboard_thread = threading.Thread(
        target=image_keyboard_listener, 
        args=(stop_event,), 
        daemon=True,
        name='KeyboardListenerThread'
    )
    
    # If you decide to use the Telegram bot in the future, uncomment and adjust accordingly
    # telegram_thread = threading.Thread(
    #     target=run_telegram_bot, 
    #     args=(queue_faces,), 
    #     daemon=True,
    #     name='TelegramBotThread'  # Optional: Assign a name for easier debugging
    # )

    # Start the threads
    monitor_embedding_thread.start()
    monitor_image_thread.start()
    image_processing_thread.start()
    keyboard_thread.start()
    # telegram_thread.start()

    logger.info("Application started. Press 'q' to exit.")
    print("Application started. Press 'q' to exit.")

    # Keep the main program running until stop_event is set
    try:
        while not stop_event.is_set():
            time.sleep(1)
    except KeyboardInterrupt:
        logger.info("KeyboardInterrupt received. Stopping threads...")
        stop_event.set()
    
    # Wait for threads to finish
    monitor_embedding_thread.join()
    monitor_image_thread.join()
    image_processing_thread.join()
    keyboard_thread.join()
    # telegram_thread.join()

    logger.info("Application has been terminated gracefully.")
    print("Application has been terminated gracefully.")

if __name__ == "__main__":
    main()
