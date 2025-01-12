import dataclasses

from .GsMessageMessageEvent import GsMessageMessageEvent

@dataclasses.dataclass
class GameLogEvent(GsMessageMessageEvent):

	log_message: str

