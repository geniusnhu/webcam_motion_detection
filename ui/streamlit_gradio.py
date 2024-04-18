import sys, os
parent_dir = os.getcwd() # find the path to module a
path = os.path.dirname(parent_dir) # Go up one level to the common parent directory
sys.path.append(path) # Add the parent to sys.path

import streamlit as st
from streamlit_webrtc import WebRtcMode, webrtc_streamer
import numpy as np
import av
import queue

from utils import get_base64_encoded_audio
from motion_detection import load_config

html_string = """ <!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>Display Webcam Stream</title>

<style>
#container {
	margin: 0px auto;
	width: 500px;
	height: 375px;
	border: 10px #333 solid;
}
#videoElement {
	width: 500px;
	height: 375px;
	background-color: #666;
}
</style>
</head>

<body>
<div id="container">
	<video autoplay="true" id="videoElement">

	</video>
</div>
<script>
	var video = document.querySelector("#videoElement");

	if (navigator.mediaDevices.getUserMedia) {
	  navigator.mediaDevices.getUserMedia({ audio: true, video: true })
	    .then(function (stream) {
	      video.srcObject = stream;
	    })
	    .catch(function (err0r) {
	      console.log("Something went wrong!");
	    });
	}
</script>
</body>
</html>
"""

# st.components.v1.html(html_string, height=450)

args = load_config()

# threshold to detect motion
threshold = float(args['threshold'])

last_mean = queue.Queue()
last_mean.put(0)

QueueManager = queue.Queue(int(args['queue_size']))
result_queue = queue.Queue()

# Count number of frames to process
n_frames_queue = queue.Queue()
n_frames_queue.put(0)

# >>> MOTION DETECTION ENGINE
def video_frame_callback(frame: av.VideoFrame) -> av.VideoFrame:
	image = frame.to_ndarray(format="bgr24")
	count = n_frames_queue.get()

	if count == 0 or count+1 >= args['n_frames']:
		# Reset n_frames_queue
		n_frames_queue.put(1)
		# Normalize pixel
		norm_image = image / 255
		frame_mean = np.sum(norm_image) / float(norm_image.shape[0] * norm_image.shape[1] * norm_image.shape[2])

		# Detect movement
		prev_mean = last_mean.get()
		if prev_mean != 0:
			if QueueManager.full():
				_ = QueueManager.get()
			if np.abs(frame_mean/prev_mean - 1) > threshold:
				QueueManager.put('motion')
			else:
				QueueManager.put('no_motion')

		# Store current mean to compare in next iteration
		last_mean.put(frame_mean)

		# Post process
		if not result_queue.empty():
			_ = result_queue.get()
		if QueueManager.full() and QueueManager.queue.count('motion') > args['queue_threshold']:
			result_queue.put(True)
		else:
			result_queue.put(False)

		# print(last_mean.queue, QueueManager.queue, result_queue.queue)

	else:
		n_frames_queue.put(count + 1)

	return av.VideoFrame.from_ndarray(image, format="bgr24")

webrtc_ctx = webrtc_streamer(
    key="object-detection",
    mode=WebRtcMode.SENDRECV,
    rtc_configuration={"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]},
    video_frame_callback=video_frame_callback,
    media_stream_constraints={"video": True, "audio": True},
    async_processing=True,
	sendback_video=True,
)

if 'run' not in st.session_state:
    st.session_state['run'] = True

audio_path = "sound/ting_alert.mp3"
audio_base64 = get_base64_encoded_audio(audio_path)

if st.checkbox("Show the detected labels", value=True):
	if webrtc_ctx.state.playing:
		labels_placeholder = st.empty()

		while True:
			result = result_queue.get()
			labels_placeholder.table([result])

			# Alert
			if result:
				if st.session_state['run']:
					audio_html = f"""
					<audio id="alertAudio" autoplay>
						<source src="{audio_base64}" type="audio/mpeg">
						Your browser does not support the audio element.
					</audio>
					"""
					st.markdown(audio_html, unsafe_allow_html=True)
					st.session_state['run'] = False  # Prevent re-triggering until reset

			else:
				st.session_state['run'] = True # Reset to True when no_motion is detected

