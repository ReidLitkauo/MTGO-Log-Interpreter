import os
import threading
import queue
import time

from ConfigKey import ConfigKey
from EventType import EventType
from WorkerThread import WorkerThread

class LogFileLineReaderThread(WorkerThread):
	
	__last_modified_ts: int
	__last_processed_line: int
			
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
		for line in log_lines[self.__last_processed_line:]:
			self.__process_one_line(line)
		self.__last_processed_line = len(log_lines)
		self._logger.debug(f'Last processed line: {self.__last_processed_line}')

	def __get_log_file_as_lines(self) -> list[str]:
		ret = []
		with open(self._config[ConfigKey.MTGO_LOG_FILE_LOCATION]) as f:
			while line := f.readline():
				ret.append(line)
		return ret

	def __process_one_line(self, line) -> None:
		self._comms.put(EventType.RAW_LINE, line)

