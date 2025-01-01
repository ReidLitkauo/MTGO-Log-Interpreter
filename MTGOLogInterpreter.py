import logging
import os
import yaml

from LogFileLineReaderThread import LogFileLineReaderThread
from LoggingFormatter import LoggingFormatter

class MTGOLogInterpreter:
	
	_logger: logging.Logger
	_config: dict
	
	DEFAULT_CONFIG_FILE = './config.yaml'
	
	DEFAULT_CONFIG_DATA = {
		'MTGO Log File Location': None,
		'Port': 62559,
		'Logging Level': 'WARNING',
	}
	
	def __init__(self, config: dict | str = DEFAULT_CONFIG_FILE):
		self._logger = self.__setup_logger()
		self._config = self.__setup_config(config)
		self.__update_logging_level()

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
		if type(config) is str:
			config = self.__get_config_from_file(config)
		ret = {}
		for k in config:
			ret[k] = config.get(k, self.DEFAULT_CONFIG_DATA[k])
		self._logger.info(f'Using configuration: {ret}')
		return ret

	def __get_config_from_file(self, config_file: str) -> dict:
		try:
			with open(config_file) as f:
				return yaml.safe_load(f.read())
		except FileNotFoundError:
			self._logger.warn(f'Specified config file "{config_file}" not found, using defaults.')
			return self.DEFAULT_CONFIG_DATA\
	
	def __update_logging_level(self):
		if self._config['Logging Level'] not in list(logging.getLevelNamesMapping()):
			self._logger.fatal(f'Invalid logging level provided: {self._config['Logging Level']}')
			exit()
		self._logger.setLevel(getattr(logging, self._config['Logging Level']))

	def run(self) -> None:
		self.__start_daemon_threads()
		self._logger.debug('DEBUG')
		self._logger.info('INFO')
		self._logger.warning('WARNING')
		self._logger.error('ERROR')
		self._logger.critical('CRITICAL')

	def __start_daemon_threads(self) -> None:
		LogFileLineReaderThread(logger = self._logger, log_file_location = self._config['MTGO Log File Location']).start()

