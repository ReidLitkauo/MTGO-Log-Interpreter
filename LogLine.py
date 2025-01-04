import dataclasses
import json

from EventType import EventType

@dataclasses.dataclass
class LogLine:

	line_number: int
	contents: str
	event_type: EventType = EventType.RAW_LINE

	def json(self):
		return json.dumps({
			'line_number': self.line_number,
			'contents': self.contents,
			'event_type': self.event_type.name,
		})
