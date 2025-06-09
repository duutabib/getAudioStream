from src.script import audioCapture
import logging 


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


if __name__ == '__main__':
	audio,dqueue,filename,thread = audioCapture(mode='get',record=True)
	try:
		while True:
			print(dqueue)
	except KeyboardInterrupt:
		logger.info("Recording stopped...")
		raise SystemExit(0)