import re

from EventType import EventType
from LogLineProcessorThread import LogLineProcessorThread

class GameplayStatusUpdateProcessorThread(LogLineProcessorThread):
	
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs, event_type = EventType.RAW_LINE)
		self.__regex = re.compile('\\d\\d:\\d\\d:\\d\\d \\[INF\\] \\(Twitch Info\\|Game Play Status Update.*\\) (\\{.*\\})')

	def _can_process(self, message: str) -> bool:
		return bool(self.__regex.match(message))

	def _process_message(self, message: str) -> bool:
		self._logger.debug(f'Found GAMEPLAY_STATUS_UPDATE')

