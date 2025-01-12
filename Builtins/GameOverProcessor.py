import re

from .BaseEvent import BaseEvent
from .GameLogProcessor import GameLogProcessor
from .GameOverEvent import GameOverEvent

	__regex: re.Match = re.compile('@P([^ ]+) wins the game.')
	
	def process(self, raw_event: BaseEvent) -> GameOverEvent | None:
		raw_event = super().process(raw_event)
		if not raw_event:
			return None
		match = self.__regex.match(raw_event.log_message)
		if not match:
			return None
		return GameOverEvent( **raw_event.as_dict(),
			winner = match.group(1),
		)

