import logging
import typing

from .BaseEvent import BaseEvent

class BaseProcessor:
	
	_logger: logging.Logger
	
	def __init__(self, logger: logging.Logger):
		self._logger = logger
	
	def process(self, raw_event: BaseEvent) -> BaseEvent | None:
		return raw_event

