import copy
import os
import threading
import queue
import time

from ConfigKey import ConfigKey
from WorkerThread import WorkerThread

from Builtins.BaseEvent import BaseEvent
from Builtins.BaseProcessor import BaseProcessor
from Builtins.GameLogProcessor import GameLogProcessor
from Builtins.GameplayStatusUpdateProcessor import GameplayStatusUpdateProcessor
from Builtins.GsMessageMessageProcessor import GsMessageMessageProcessor
from Builtins.TurnStartProcessor import TurnStartProcessor

class LogFileLineReaderThread(WorkerThread):
	
	__registered_processors: list[BaseProcessor]
	__registered_processors_mutex: threading.Lock
	
	__last_modified_ts: int
	__last_processed_line: int
	
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.__registered_processors = []
		self.__registered_processors_mutex = threading.Lock()
		self.__register_default_procesors()
	
	def __register_default_procesors(self) -> None:
		for processor in (
			GameplayStatusUpdateProcessor,
			GsMessageMessageProcessor,
			GameLogProcessor,
			TurnStartProcessor,
		):
			self.register_processor(processor(self._logger))
	
	def register_processor(self, processor: BaseProcessor):
		with self.__registered_processors_mutex:
			self.__registered_processors.append(processor)
			
	def run(self) -> None:
		self.__initialize()
		self.__monitor_mtgo_log()

	def __initialize(self) -> None:
		if not self.__verify_logging_file_exists():
			exit()
		self.__last_modified_ts = self.__get_initial_modified_ts()
		self.__last_processed_line = self.__get_initial_line_count()

	def __verify_logging_file_exists(self) -> bool:
		if self._config[ConfigKey.MTGO_LOG_FILE_LOCATION] is None:
			self._logger.critical('MTGO log file location not set. Please update configuration file.')
			return False
		if not os.path.exists(self._config[ConfigKey.MTGO_LOG_FILE_LOCATION]):
			self._logger.critical(f'Could not locate MTGO log file: {self._config[ConfigKey.MTGO_LOG_FILE_LOCATION]}')
			return False
		self._logger.info(f'Using log file at {self._config[ConfigKey.MTGO_LOG_FILE_LOCATION]}')
		return True

	def __get_initial_modified_ts(self) -> int:
		return 0
	
	def __get_initial_line_count(self) -> int:
		with open(self._config[ConfigKey.MTGO_LOG_FILE_LOCATION]) as f:
			return len(f.readlines())
	
	def __monitor_mtgo_log(self) -> None:
		while True:
			time.sleep(self._config[ConfigKey.DELAY_BETWEEN_CHECKS])
			modified_ts = os.path.getmtime(self._config[ConfigKey.MTGO_LOG_FILE_LOCATION])
			if modified_ts > self.__last_modified_ts:
				self.__last_modified_ts = modified_ts
				self.__process_new_lines()
	
	def __process_new_lines(self) -> None:
		log_lines = self.__get_log_file_as_lines()
		for line_number, line_contents in enumerate(log_lines[self.__last_processed_line:]):
			event = BaseEvent( raw_contents = line_contents, line_number = line_number + self.__last_processed_line )
			self.__process_event(event)
		self.__last_processed_line = len(log_lines)
		self._logger.debug(f'Last processed line: {self.__last_processed_line}')

	def __get_log_file_as_lines(self) -> list[str]:
		ret = []
		with open(self._config[ConfigKey.MTGO_LOG_FILE_LOCATION]) as f:
			while line := f.readline():
				ret.append(line)
		return ret

	def __process_event(self, raw_event: BaseEvent) -> None:
		self._comms.put(raw_event)
		with self.__registered_processors_mutex:
			registered_processors = copy.deepcopy(self.__registered_processors)
		for processor in registered_processors:
			try:
				if processed_event := processor.process(raw_event):
					self._comms.put(processed_event)
			except Exception as e:
				self._logger.exception(e)

