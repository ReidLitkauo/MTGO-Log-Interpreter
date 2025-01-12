

from .BaseEvent import BaseEvent
from .GsMessageMessageProcessor import GsMessageMessageProcessor
from .GameLogEvent import GameLogEvent

class GameLogProcessor(GsMessageMessageProcessor):
	
	__GAMELOG_SIGNATURE_CONTENT = [0x67, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]
	__GAMELOG_SIGNATURE_OFFSET  = 12
	__MESSAGE_CONTENT_OFFSET = 24

	def process(self, raw_event: BaseEvent) -> GameLogEvent | None:
		raw_event = super().process(raw_event)
		if not raw_event:
			return None
		signature = raw_event.gs_message[ self.__GAMELOG_SIGNATURE_OFFSET : self.__GAMELOG_SIGNATURE_OFFSET + len(self.__GAMELOG_SIGNATURE_CONTENT) ]
		if signature != self.__GAMELOG_SIGNATURE_CONTENT:
			return None
		game_log_message = bytes(raw_event.gs_message[self.__MESSAGE_CONTENT_OFFSET:]).decode('cp1252')
		return GameLogEvent( **raw_event.as_dict(), log_message = game_log_message )

