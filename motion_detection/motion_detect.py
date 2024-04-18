import numpy as np
import av

def detect_motion(im, last_mean, threshold, QueueManager):
    # Normalize pixel
    im = im / 255

    frame_mean = np.sum(im) / float(im.shape[0] * im.shape[1] * im.shape[2])
    print(">>> ", frame_mean, last_mean)

    if last_mean != 0:
        if np.abs(frame_mean/last_mean - 1) > threshold:
            QueueManager.enqueue(['motion'])
        else:
            QueueManager.enqueue(['no_motion'])

    last_mean = frame_mean      # Store current mean to compare in next iteration.
    print(QueueManager.queues)
    return last_mean, QueueManager

def post_process(QueueManager, queue_threshold):
    result = QueueManager.post_process(queue_threshold)
    # print(QueueManager.queues, result)
    return result, QueueManager
