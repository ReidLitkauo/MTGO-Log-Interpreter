import os
import threading
import queue

from LoggingDaemonThread import LoggingDaemonThread

class LogFileLineReaderThread(LoggingDaemonThread):
	
	__queue_list: list[queue.SimpleQueue] = []
	__log_file_location: str
	
	def __init__(self, log_file_location, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.__log_file_location = log_file_location
		if not self.__verify_logging_file_exists():
			exit()
		

	def __verify_logging_file_exists(self):
		if self.__log_file_location is None:
			self._logger.critical('MTGO log file location not set. Please update configuration file.')
			return False
		if not os.path.exists(self.__log_file_location):
			self._logger.critical(f'Could not locate MTGO log file: {self.__log_file_location}')
			return False
		self._logger.info(f'Using log file at {self.__log_file_location}')
		return True
	
	def run(self) -> None:
		pass

