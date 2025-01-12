import logging
import os
import queue
import yaml

from Config import Config
from ConfigKey import ConfigKey
from EventCommunicator import EventCommunicator
from LogFileLineReaderThread import LogFileLineReaderThread
from LoggingFormatter import LoggingFormatter
from WebsocketServerThread import WebsocketServerThread
from WorkerThread import WorkerThread

from Builtins.BaseEvent import BaseEvent
from Builtins.BaseProcessor import BaseProcessor

class MTGOLogInterpreter:
	
	_logger: logging.Logger
	_config: Config
	_comms: EventCommunicator
	
	def __init__(self, config: dict | str | None = None):
		self._logger = self.__setup_logger()
		self._config = self.__setup_config(config)
		self._comms = self.__setup_comms()
		self._threads = []

	def __setup_logger(self) -> logging.Logger:
		self.__enable_console_colors()
		handler = logging.StreamHandler()
		handler.setFormatter(LoggingFormatter())
		logger = logging.getLogger('MTGO Log Interpreter')
		logger.addHandler(handler)
		logger.setLevel(logging.DEBUG)
		return logger
	
	def __enable_console_colors(self) -> None:
		os.system('')

	def __setup_config(self, config: dict | str) -> dict:
		return Config(self._logger, config)

	def __get_config_from_file(self, config_file: str) -> dict:
		try:
			with open(config_file) as f:
				return yaml.safe_load(f.read())
		except FileNotFoundError:
			self._logger.warn(f'Specified config file "{config_file}" not found, using defaults.')
			return self.DEFAULT_CONFIG_DATA
	
	def __setup_comms(self) -> EventCommunicator:
		return EventCommunicator()

	def subscribe(self, event_type: type[BaseEvent] | None = None) -> queue.SimpleQueue:
		return self._comms.subscribe(event_type)
	
	def unsubscribe(self, old_queue: queue.SimpleQueue) -> bool:
		return self._comms.unsubscribe(old_queue)
	
	def register_log_processor(self, processor: BaseProcessor) -> None:
		self.__thread_log_file_line_reader.register_processor(processor)

	def run(self) -> None:
		self.__start_daemon_threads()

	def __start_daemon_threads(self) -> None:
		for thread in (
			WebsocketServerThread,
			LogFileLineReaderThread,
		):
			thread( logger = self._logger, config = self._config, comms = self._comms ).start()
	
