import logging
import threading

from .Config import Config
from .EventCommunicator import EventCommunicator

class WorkerThread(threading.Thread):

	_logger: logging.Logger
	_config: Config

	def __init__(self, logger: logging.Logger, config: Config, comms: EventCommunicator, *args, **kwargs):
		super().__init__(*args, **kwargs, daemon = True)
		self._logger = logger
		self._config = config
		self._comms = comms

