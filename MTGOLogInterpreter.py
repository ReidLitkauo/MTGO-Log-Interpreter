import logging
import os
import queue
import yaml

from Config import Config
from ConfigKey import ConfigKey
from EventCommunicator import EventCommunicator
from EventType import EventType
from GameplayStatusUpdateProcessorThread import GameplayStatusUpdateProcessorThread
from LogFileLineReaderThread import LogFileLineReaderThread
from LoggingFormatter import LoggingFormatter
from WebsocketServerThread import WebsocketServerThread

class MTGOLogInterpreter:
	
	_logger: logging.Logger
	_config: Config
	_comms: EventCommunicator
	
	def __init__(self, config: dict | str | None = None):
		self._logger = self.__setup_logger()
		self._config = self.__setup_config(config)
		self._comms = self.__setup_comms()

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

	def subscribe(self, event_type: EventType) -> queue.SimpleQueue:
		return self._comms.subscribe(event_type)

	def run(self) -> None:
		self.__start_daemon_threads()
		self._logger.debug('DEBUG')
		self._logger.info('INFO')
		self._logger.warning('WARNING')
		self._logger.error('ERROR')
		self._logger.critical('CRITICAL')

	def __start_daemon_threads(self) -> None:
		for daemon_thread in (
			WebsocketServerThread,
			LogFileLineReaderThread,
			GameplayStatusUpdateProcessorThread,
		):
			daemon_thread(logger = self._logger, config = self._config, comms = self._comms).start()

