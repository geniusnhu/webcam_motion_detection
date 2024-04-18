import cv2
import numpy as np
from QueuePrediction import FIFOQueues
import yaml

from motion_detection import detect_motion, post_process


def main_run():

    config_file_path = 'config.yml'
    with open(config_file_path, 'r') as file:
        args = yaml.safe_load(file)

    cap = cv2.VideoCapture(0)
    fps = cap.get(cv2.CAP_PROP_FPS)

    # threshold to detect motion
    threshold = float(args['threshold'])

    # Analyze frame every N frame with N = 1/2 of FPS
    n_frame = int(fps / 2)

    last_mean = 0
    frame_count = 0

    # Max size of the Queue
    queue_size = int(args['queue_size'])
    
    # Initiate queue
    QueueManager = FIFOQueues(class_weight=None, maxsize=queue_size)

    while True:
        (rv, im) = cap.read()
        frame_count += 1
        if not rv:
            break

        # Display the resulting frame 
        # cv2.imshow('frame', im) 

        if frame_count == n_frame:
            last_mean = detect_motion(im, last_mean, threshold, QueueManager)
            prediction = post_process(QueueManager, args['queue_threshold'])
            frame_count = 0

            if prediction == 'motion':
                return True
            

        # the 'q' button is set as the quitting button you may use any desired button of your choice 
        # if cv2.waitKey(1) & 0xFF == ord('q'): 
        #     break

    cap.release()
    # cv2.destroyAllWindows() 


if __name__ == "__main__":
        
    main_run()
