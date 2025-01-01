import logging
import threading

class LoggingDaemonThread(threading.Thread):

	_logger: logging.Logger

	def __init__(self, logger: logging.Logger, *args, **kwargs):
		super().__init__(*args, **kwargs, daemon = True)
		self._logger = logger

