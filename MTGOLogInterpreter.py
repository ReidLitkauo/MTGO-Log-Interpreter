import logging
import os
import queue
import yaml

from Config import Config
from ConfigKey import ConfigKey
from EventCommunicator import EventCommunicator
from EventType import EventType
from GameplayStatusUpdateProcessor import GameplayStatusUpdateProcessor
from LogFileLineReaderThread import LogFileLineReaderThread
from LogLineProcessor import LogLineProcessor
from LoggingFormatter import LoggingFormatter
from WebsocketServerThread import WebsocketServerThread
from WorkerThread import WorkerThread

class MTGOLogInterpreter:
	
	_logger: logging.Logger
	_config: Config
	_comms: EventCommunicator
	__thread_log_file_line_reader: LogFileLineReaderThread
	__thread_websocket_server: WebsocketServerThread
	
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

	def subscribe_to_events(self, event_type: EventType) -> queue.SimpleQueue:
		return self._comms.subscribe(event_type)
	
	def register_log_processor(self, processor: LogLineProcessor) -> None:
		self.__thread_log_file_line_reader.register_processor(processor)

	def run(self) -> None:
		self.__start_daemon_threads()
		self._logger.debug('DEBUG')
		self._logger.info('INFO')
		self._logger.warning('WARNING')
		self._logger.error('ERROR')
		self._logger.critical('CRITICAL')

	def __start_daemon_threads(self) -> None:
		for thread in (
			WebsocketServerThread,
			LogFileLineReaderThread,
		):
			thread( logger = self._logger, config = self._config, comms = self._comms ).start()
	
