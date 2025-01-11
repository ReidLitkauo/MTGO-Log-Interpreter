import re

from BaseEvent import BaseEvent
from GameLogProcessor import GameLogProcessor
from TurnStartEvent import TurnStartEvent

class TurnStartProcessor(GameLogProcessor):
	
	__regex: re.Match = re.compile('@PTurn (\\d*): (.*)')
	
	def process(self, raw_event: BaseEvent) -> TurnStartEvent:
		raw_event = super().process(raw_event)
		if not raw_event:
			return None
		match = self.__regex.match(raw_event.log_message)
		if not match:
			return None
		return TurnStartEvent( **raw_event.as_dict(),
			turn_number = int(match.group(1)),
			player_username = match.group(2),
		)

