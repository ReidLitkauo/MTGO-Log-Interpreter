import logging
import typing

from EventType import EventType
from LogLine import LogLine

class LogLineProcessor:
	
	_logger: logging.Logger
	
	def __init__(self, logger: logging.Logger):
		self._logger = logger
	
	def get_event_type():
		return EventType.RAW_LINE
	
	def can_process(self, line: LogLine) -> typing.Any:
		return True
	
	def process_line(self, line: LogLine) -> LogLine:
		return line

