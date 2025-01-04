import json
import re
import typing

from EventType import EventType
from LogLine import LogLine
from LogLineProcessor import LogLineProcessor

class GameplayStatusUpdateProcessor(LogLineProcessor):
	
	__regex: re.Pattern = re.compile('\\d\\d:\\d\\d:\\d\\d \\[INF\\] \\(Twitch Info\\|Game Play Status Update.*\\) (\\{.*\\})')
	
	def get_event_type(self):
		return EventType.GAMEPLAY_STATUS_UPDATE

	def can_process(self, line: LogLine) -> re.Match:
		return super().can_process(line) and self.__regex.match(line.contents)

	def process_line(self, line: LogLine) -> LogLine:
		line = super().process_line(line)
		return LogLine(
			line_number = line.line_number,
			contents = self.__regex.match(line.contents).group(1),
			event_type = self.get_event_type(),
		)

