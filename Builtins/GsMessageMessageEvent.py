import dataclasses

from .BaseEvent import BaseEvent

@dataclasses.dataclass
class GsMessageMessageEvent(BaseEvent):
	
	gs_message: list[int]

