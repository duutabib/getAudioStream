from collections import deque
import threading
import queue
import soundfile 
import logging
import sounddevice
import tempfile
import os

# configure logger
logger = logging.getLogger(__name__)
logger.basicConfig(level=logging.DEBUG)


def audioCapture(
			mode='send',
			record=False,
			filename='recorded',
			typename='.wav',
			dirname='',
			samplerate=44100,
			channels=2,
			blocksize=1024,
	):
	""" Capture audio stream from default audio device

		Args:
			mode: 'send' or 'get'
			record: True or False
			filename: filename of the recorded audio
			typename: type of the recorded audio
			dirname: directory of the recorded audio
			samplerate: samplerate of the recorded audio
			channels: channels of the recorded audio
			blocksize: blocksize of the recorded audio
		"""

	# init queue
	dqueue = deque(maxlen=20)
	_, filename = tempfile.mkstemp(prefix=filename,suffix=typename, dir=dirname)
	os.close(_)
	frame = [0]
	audio = queue.Queue(maxsize=20)

	def getAudio():
		def callback(indata, outdata, frames, time, status):
			if status:
				logger.info(f"Current status: {status}...")

			if mode=='get':
				try:
					frame = audio.get()
					outdata[:] = frame
					dqueue.append(frame)
					
				except queue.Full:
					logger.info("Queue is full, discarding frame")
			else:
				audio.put(indata)
				dqueue.append(indata)
		if record:
			try:
				with soundfile.SoundFile(filename, mode='x', samplerate=samplerate, channels=channels) as file, \
					sounddevice.Stream(channels=channels, blocksize=blocksize, callback=callback) as stream:	
					logger.info("Recording...press Ctrl+C to stop the recording...")
					try:
						while True:
							file.write(audio.get())
					except KeyboardInterrupt:
						logger.info("Recording stopped...")
						raise SystemExit(0)
					finally:
						stream.close()
						file.close()
			except (OSError,sounddevice.PortAudioError) as e:
				logger.error(f"Audio device error: {e}")
				raise
				
		else:
			with sounddevice.Stream(channels=channels, blocksize=blocksize, callback=callback):
				logger.info("Press Ctrl+C to stop the recording...")
				try:
					input()
				except KeyboardInterrupt:
					logger.info("Recording stopped")
					raise SystemExit(0)
		
	# init thread		
	thread = threading.Thread(target=getAudio, args=(), daemon=True)
	thread.start()

	return audio,dqueue,filename,thread 