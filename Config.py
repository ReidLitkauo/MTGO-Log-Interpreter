import logging
import yaml

from .ConfigKey import ConfigKey

class Config:
	
	DEFAULT_CONFIG_FILE = './config.yaml'
	
	DEFAULT_CONFIG_DATA = {
		ConfigKey.MTGO_LOG_FILE_LOCATION: None,
		ConfigKey.PORT:                   62559,
		ConfigKey.LOGGING_LEVEL:          'WARNING',
		ConfigKey.DELAY_BETWEEN_CHECKS:   0.5,
	}
	
	_config: dict
	
	def __init__(self, logger: logging.Logger, config: dict | str | None = None):
		self._logger = logger
		config = config or self.DEFAULT_CONFIG_FILE
		if type(config) is str:
			config = self.__get_config_from_file(config)
		self._config = self.__setup_config_from_dict(config)
		self.__update_logger_level()
		self._logger.info(f'Using configuration: {self._config}')

	def __get_config_from_file(self, config_file: str) -> dict:
		try:
			with open(config_file) as f:
				return yaml.safe_load(f.read())
		except FileNotFoundError:
			self._logger.warn(f'Specified config file "{config_file}" not found, using defaults.')
			return self.DEFAULT_CONFIG_DATA

	def __setup_config_from_dict(self, config: dict) -> dict:
		ret = {}
		for k in config:
			try:
				ret[ ConfigKey(k) ] = config.get(k, self.DEFAULT_CONFIG_DATA[ ConfigKey(k) ])
			except ValueError:
				self._logger.warning(f'Discarding invalid config key: {k}')
		return ret

	def __update_logger_level(self):
		if self._config[ConfigKey.LOGGING_LEVEL] not in list(logging.getLevelNamesMapping()):
			self._logger.fatal(f'Invalid logging level provided: {self._config[ConfigKey.LOGGING_LEVEL]}')
			exit()
		self._logger.setLevel(getattr(logging, self._config[ConfigKey.LOGGING_LEVEL]))

	def __getitem__(self, key: ConfigKey):
		return self._config[key]

